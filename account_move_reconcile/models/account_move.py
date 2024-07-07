from odoo import api, models, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    facturas_conciliacion_id = fields.Many2one(comodel_name='mp.facturas.conciliacion', readonly=True)
    show_btn_reconcile_button = fields.Boolean(compute="show_btn_reconcile")

    def show_btn_reconcile(self):
        if self.partner_id and self.partner_id.responsability_id.id == 2 and\
                self.partner_id.l10n_cl_sii_taxpayer_type == '1':
            self.show_btn_reconcile_button = True
        else:
            self.show_btn_reconcile_button = False

    def action_post(self):
        if self.move_type == 'in_invoice' and \
                (not self.facturas_conciliacion_id and
                 (self.partner_id and self.partner_id.responsability_id.id == 2 and
                  self.partner_id.l10n_cl_sii_taxpayer_type == '1')
        ):
            raise UserError("El documento debe tener un Numero de SII asignado")
        res = super(AccountMove, self).action_post()
        return res

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        for move_id in self:
            if not move_id.facturas_conciliacion_id and move_id.l10n_latam_document_number and\
                    move_id.l10n_latam_document_number.isdigit():
                move_id.sudo().sii_document_number = move_id.l10n_latam_document_number
                move_id.sudo().l10n_latam_document_number = move_id.sii_document_number
            else:
                move_id.sudo().sii_document_number = 0
                move_id.sudo().l10n_latam_document_number = 0

    @api.onchange('l10n_latam_document_number')
    def _onchange_document_number(self):
        for move_id in self:
            if move_id.id or move_id.id.origin:
                if move_id.l10n_latam_document_number and not move_id.l10n_latam_document_number.isdigit():
                    raise UserError("El numero de documento debe ser de tipo numerico")
                if not move_id.facturas_conciliacion_id and move_id.l10n_latam_document_number and move_id.l10n_latam_document_number.isdigit():
                    move_id.sudo().sii_document_number = move_id.l10n_latam_document_number
                    move_id.sudo().l10n_latam_document_number = move_id.sii_document_number

    def button_reconcile_custom(self):
        tree_view = self.env.ref("account_move_reconcile.account_facturacion_conciliacion_wizard_tree")
        self.with_context(default_move_id=self.id)
        facturas_conciliacion_ids = self.env['mp.facturas.conciliacion'].search([
            ('rut_emisor', '=', self.partner_id.vat),
            ('monto_total', '=', self.amount_total),
            ('estado', '=', False),
        ])
        self.env['account.facturacion.conciliacion.wizard'].search([]).unlink()
        for facturas_conciliacion_id in facturas_conciliacion_ids:
            self.env['account.facturacion.conciliacion.wizard'].create({
                'move_id': self.id,
                'factura_conciliacion_id': facturas_conciliacion_id.id
            })

        return {
            'name': _('Conciliar Documento'),
            'view_id': tree_view.id,
            'view_mode': 'tree',
            'res_model': 'account.facturacion.conciliacion.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'flags': {'hasSelectors': False, 'initial_mode': 'view'},
            'context': {
                'default_move_id': self.id,
            }
        }
