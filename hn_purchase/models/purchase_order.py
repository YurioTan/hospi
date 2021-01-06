from odoo import api, fields, models


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
        odoo_seq = self.env['ir.sequence'].next_by_code('po.hospi.sequence')
        new_seq = odoo_seq.split('/')
        new_seq[-2] = self.convert_month_to_roman(int(new_seq[-2]))
        new_seq = '/'.join(new_seq)
        vals['name'] = new_seq
        res = super(PurchaseOrder, self).create(vals)
        return res
