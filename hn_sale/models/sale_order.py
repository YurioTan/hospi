from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SaleOder(models.Model):
  _inherit = 'sale.order'

  # deprecated as end of 202312, replaced by order_type
  co_sale = fields.Boolean('CO', default=False)

  order_type = fields.Selection([
    ('oem', 'OEM'),
    ('service', 'Service'),
    ('distributor', 'Distributor'),
    ('swasta', 'Swasta'),
    ('institusi', 'Institusi'),
    ('reguler', 'Reguler'),
  ], string='Order Type', required=True, default="reguler")
  distributor_id = fields.Many2one('res.partner', 'Distributor', domain=[('customer_type','=','distributor')])

  @api.model
  def create(self, vals):
    order_type = vals.get('order_type')
    if order_type == 'oem':
      vals['name'] = self.env['ir.sequence'].next_by_code('co.sale.sequence')
    elif order_type == 'service':
      vals['name'] = self.env['ir.sequence'].next_by_code('service.sale.sequence')
    elif order_type == 'distributor':
      vals['name'] = self.env['ir.sequence'].next_by_code('distributor.sale.sequence')
    elif order_type == 'swasta':
      vals['name'] = self.env['ir.sequence'].next_by_code('swasta.sale.sequence')
    elif order_type == 'institusi':
      vals['name'] = self.env['ir.sequence'].next_by_code('institusi.sale.sequence')
    elif order_type == 'reguler':
      vals['name'] = self.env['ir.sequence'].next_by_code('sale.order')
    else:
      raise ValidationError(_("Invalid order type. Please make sure to create/edit orders from their corresponding menus."))

    res = super(SaleOder, self).create(vals)
    return res

  def action_create_customer_db(self):
    for row in self:
      return True

  def action_view_customer_db(self):
    xmlid = "hn_sale.action_sale_customer_db"
    action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
    action['domain'] = [('sale_order_id','=',self.id)]
    return action
