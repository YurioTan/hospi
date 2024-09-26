from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    amount_taxes = fields.Float('Amount Taxes', compute="compute_amount_taxes")

    @api.onchange('tax_ids')
    def compute_amount_taxes(self):
        for rec in self:
            if rec.tax_ids:
                base_amount = rec.quantity * rec.price_unit
                for tax in rec.tax_ids:
                    amount_tax = tax._compute_amount(base_amount, price_unit=rec.price_unit, quantity=rec.quantity,
                                                     product=rec.product_id)
                    rec.amount_taxes = amount_tax
            else:
                rec.amount_taxes = 0
