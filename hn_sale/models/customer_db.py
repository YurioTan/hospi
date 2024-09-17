from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CustomerDB(models.Model):

  _name = 'sale.customer.db'
  _description = 'Customer Database'
  _inherit = ['mail.thread']

  input_date = fields.Date('Input Date', tracking=True)
  sale_order_id = fields.Many2one('sale.order', 'SO', ondelete="cascade", tracking=True)
  partner_id = fields.Many2one('res.partner', 'Contact', required=True, tracking=True)
  distributor_id = fields.Many2one('res.partner', 'Distributor', domain=[('customer_type','=','distributor')], tracking=True)
  partner_phone = fields.Char('Phone', related="partner_id.phone")
  partner_mobile = fields.Char('Mobile', related="partner_id.mobile")
  partner_email = fields.Char('Email', related="partner_id.email")
  partner_location_id = fields.Many2one('partner.location', 'Pulau', related="partner_id.partner_location_id")
  partner_category_id = fields.Many2one('partner.category', 'Wilayah', related="partner_id.partner_category_id")
  partner_class_id = fields.Many2one('partner.class', 'Kelas RS', related="partner_id.partner_class_id")
  partner_area_map_id = fields.Many2one('partner.area.map', 'Peta Area', related="partner_id.partner_area_map_id")
  partner_level_id = fields.Many2one('partner.level', 'Level', related="partner_id.partner_level_id")
  brand_id = fields.Many2one('product.brand', 'Brand', tracking=True)
  product_id = fields.Many2one('product.product', 'Product', tracking=True)
  serial_number = fields.Many2one('stock.production.lot', 'Serial Number', tracking=True)
  install_date = fields.Date('Install Date', tracking=True)
  tracking_number = fields.Char('Tracking Number', tracking=True)

  def name_get(self):
    result = []
    for row in self:
      components = []
      if row.input_date:
        components.append("%s" % row.input_date)
      if row.partner_id:
        if row.input_date:
          components.append("(%s)" % row.partner_id.alias_name and row.partner_id.alias_name or row.partner_id.name)
        else:
          components.append("%s" % row.partner_id.alias_name and row.partner_id.alias_name or row.partner_id.name)
      result.append((row.id," ".join(components)))
    return result
  
  @api.onchange('sale_order_id')
  def onchange_sale_order_id(self):
    if self.sale_order_id:
      self.input_date = self.sale_order_id.date_order
      self.partner_id = self.sale_order_id.partner_id.id
      self.distributor_id = self.sale_order_id.distributor_id.id
  
  @api.constrains('partner_id')
  def check_partner_id(self):
    if self.sale_order_id:
      if self.sale_order_id.partner_id.id != self.partner_id.id:
        raise ValidationError('Contact must match one on Sale Order.')


