from odoo import api, fields, models


class SaleOder(models.Model):
    _inherit = 'sale.order'

    co_sale = fields.Boolean('CO', default=False)

    @api.model
    def create(self, vals):
        if vals.get('co_sale'):
            vals['name'] = self.env['ir.sequence'].next_by_code('co.sale.sequence')
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order')

        res = super(SaleOder, self).create(vals)
        return res
