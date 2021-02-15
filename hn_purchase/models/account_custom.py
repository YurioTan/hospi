from odoo import api, fields, models


class VatResPartner(models.Model):
    _inherit = 'account.move'
    # _description = 'New Description'

    vat_child = fields.Char(string='VAT', help ='VAT child')

    @api.model
    def create(self,vals):
        ret=super(VatResPartner,self).create(vals)
        if not ret.vat_child:
            ret.vat_child=ret.partner_id.vat
        return ret