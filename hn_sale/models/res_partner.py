from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
  _inherit = 'res.partner'

  customer_db_ids = fields.One2many('sale.customer.db', 'partner_id', 'Customer DB')
  customer_db_count = fields.Integer('Customer DB Count', compute="_compute_customer_db")

  def _compute_customer_db(self):
    for row in self:
      row.customer_db_count = len(row.customer_db_ids)

  def action_view_customer_db(self):
    xmlid = "hn_sale.action_sale_customer_db"
    action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
    customer_dbs = self.env['sale.customer.db'].search([('partner_id','=',self.id)])
    if len(customer_dbs) > 1:
      action['domain'] = [('partner_id','=',self.id)]
    elif len(customer_dbs) == 1:
      action["views"] = [(self.env.ref("hn_sale.sale_customer_db_view_form").id, "form")]
      action['res_id'] = customer_dbs.id
    else:
      raise ValidationError('No customer database created for this customer yet.')
    return action
  


