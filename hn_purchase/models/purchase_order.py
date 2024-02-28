from odoo import api, fields, models
from odoo.exceptions import ValidationError,UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def convert_month_to_roman(self, number):
        int_roman = {
            1: 'I',
            2: 'II',
            3: 'III',
            4: 'IV',
            5: 'V',
            6: 'VI',
            7: 'VII',
            8: 'VII',
            9: 'XI',
            10: 'X',
            11: 'XI',
            12: 'XII'
        }
        return int_roman.get(number)

    @api.model
    def create(self, vals):
        odoo_seq = self.env['ir.sequence'].next_by_code('purchase.order')
        new_seq = odoo_seq.split('/')
        new_seq[-2] = self.convert_month_to_roman(int(new_seq[-2]))
        new_seq = '/'.join(new_seq)
        vals['name'] = new_seq
        res = super(PurchaseOrder, self).create(vals)
        return res

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