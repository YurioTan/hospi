from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CustomerDB(models.Model):

  _name = 'sale.customer.db'
  _description = 'Customer Database'

  partner_id = fields.Many2one('res.partner', 'Contact', required=True)