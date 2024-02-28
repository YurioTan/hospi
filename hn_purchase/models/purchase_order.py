from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        # force PO line's description as picking line's description
        res = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        res['description_picking'] = self.name
        return res