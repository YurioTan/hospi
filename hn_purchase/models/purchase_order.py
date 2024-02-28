from odoo import api, fields, models
from odoo.exceptions import ValidationError,UserError

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        debug = ""
        for record in res:
            debug += "%s" % record
            # if record['purchase_line_id']:
            #     purchase_line = self.env['purchase.order.line'].browse(record['purchase_line_id'])
            #     record['']
        raise ValidationError(debug)
        return res