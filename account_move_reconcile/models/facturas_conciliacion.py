from odoo import models, fields


class FacturasConciliacion(models.Model):
    _name = 'mp.facturas.conciliacion'
    _description = 'Facturas de Conciliación'
    _rec_name = 'folio'

    rzn_soc_emisor = fields.Char(string='Razón Social Emisor', size=128, index=True)
    rut_emisor = fields.Char(string='RUT Emisor', size=13, required=True, index=True)
    folio = fields.Integer(string='Folio', required=True, index=True)
    monto_total = fields.Float(string='Monto Total', required=True)
    fecha_emision = fields.Datetime(string='Fecha de Emisión', required=True)
    fecha_vencimiento = fields.Datetime(string='Fecha de Vencimiento')
    orden_compra = fields.Char(string='Orden de Compra', size=255, index=True)
    fecha_sii = fields.Datetime(string='Fecha SII')
    estado = fields.Boolean(string='Estado')
