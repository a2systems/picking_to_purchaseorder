from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date,datetime

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def btn_link_purchase_order(self):
        self.ensure_one()
        if self.state != 'done' or self.picking_type_code != 'incoming':
            raise ValidationError('Transferencia incorrecta')
        vals = {
            'picking_id': self.id,
            }
        wizard_id = self.env['picking.po.wizard'].create(vals)
        res = {
            'name': _('Picking to PO Wizard'),
            'res_model': 'picking.po.wizard',
            'view_mode': 'form',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return res

