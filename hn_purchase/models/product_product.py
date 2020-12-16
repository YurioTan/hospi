from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    external_ref = fields.Char('External Reference')

    def name_get(self):
        res = []
        for rec in self:
            if rec.external_ref:
                res.append((rec.id, '[%s] %s' % (rec.external_ref, rec.name)))
            else:
                res.append((rec.id, '%s' % rec.name))
        return res
