from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountFacturacionConciliacion(models.TransientModel):
    _name = "account.facturacion.conciliacion.wizard"

    move_id = fields.Many2one(comodel_name="account.move", ondelete="set null", readonly=True)
    factura_conciliacion_id = fields.Many2one(
        string="Factura de Conciliación",
        ondelete="set null",
        readonly=True,
        comodel_name="mp.facturas.conciliacion"
    )
    rzn_soc_emisor = fields.Char(related='factura_conciliacion_id.rzn_soc_emisor')
    rut_emisor = fields.Char(related='factura_conciliacion_id.rut_emisor')
    fecha_emision = fields.Datetime(related='factura_conciliacion_id.fecha_emision')
    fecha_vencimiento = fields.Datetime(related='factura_conciliacion_id.fecha_vencimiento')
    orden_compra = fields.Char(related='factura_conciliacion_id.orden_compra')
    fecha_sii = fields.Datetime(related='factura_conciliacion_id.fecha_sii')
    amount_total = fields.Float(related='factura_conciliacion_id.monto_total')

    def button_select_reconcile(self):
        tree_view = self.env.ref("account_move_reconcile.account_facturacion_conciliacion_wizard_confirmation_form")

        return {
            'name': _('Documento conciliacion: ') + str(self.factura_conciliacion_id.folio),
            'view_id': tree_view.id,
            'view_mode': 'form',
            'res_model': 'account.facturacion.conciliacion.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'flags': {'hasSelectors': False, 'initial_mode': 'view'},
            'context': {
                'move_id': self.move_id.id,
                'factura_conciliacion_id': self.factura_conciliacion_id.id,
            }
        }

    def button_add_reconcile(self):
        factura_conciliacion_id = self.env['mp.facturas.conciliacion'].\
            search([('id', '=', self._context.get('factura_conciliacion_id'))])
        move_id = self.env['account.move'].\
            search([('id', '=', self._context.get('move_id'))])

        move_id.sii_document_number = factura_conciliacion_id.folio
        move_id.facturas_conciliacion_id = factura_conciliacion_id
        factura_conciliacion_id.estado = True
