from odoo import fields,models, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import date

_logger = logging.getLogger(__name__)

class PickingPOWizard(models.TransientModel):
    _name = 'picking.po.wizard'
    _description = 'picking.po.wizard'

    picking_id = fields.Many2one('stock.picking','Transferencia')
    partner_id = fields.Many2one('res.partner','Proveedor',related='picking_id.partner_id')
    purchase_order_id = fields.Many2one('purchase.order','Orden de Compra')

    def btn_confirm(self):
        if not self.purchase_order_id:
            raise ValidationError(_('Seleccione PO'))
        for move in self.picking_id.move_ids_without_package:
            pol = self.purchase_order_id.order_line.filtered(lambda l: l.product_id.id == move.product_id.id)
            if not pol:
                raise ValidationError(_('Producto %s no se encuentra en PO'%(move.product_id.display_name)))
            move.purchase_line_id = pol[0].id
