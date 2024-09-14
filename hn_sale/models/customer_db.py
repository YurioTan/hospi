from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CustomerDB(models.Model):

  _name = 'sale.customer.db'
  _description = 'Customer Database'

  input_date = fields.Date('Input Date')
  sale_order_id = fields.Many2one('sale.order', 'SO')
  partner_id = fields.Many2one('res.partner', 'Contact', required=True)
  distributor_id = fields.Many2one('res.partner', 'Distributor', domain=[('customer_type','=','distributor')])
  partner_phone = fields.Char('Phone', related="partner_id.phone")
  partner_mobile = fields.Char('Mobile', related="partner_id.mobile")
  partner_email = fields.Char('Email', related="partner_id.email")
  partner_location_id = fields.Many2one('partner.location', 'Pulau', related="partner_id.partner_location_id")
  partner_category_id = fields.Many2one('partner.category', 'Wilayah', related="partner_id.partner_category_id")
  partner_class_id = fields.Many2one('partner.class', 'Kelas RS', related="partner_id.partner_class_id")
  partner_area_map_id = fields.Many2one('partner.area.map', 'Peta Area', related="partner_id.partner_area_map_id")
  partner_level_id = fields.Many2one('partner.level', 'Level', related="partner_id.partner_level_id")
  brand_id = fields.Many2one('product.brand', 'Brand')
  product_id = fields.Many2one('product.product', 'Product')
  product_alias = fields.Char('Product Alias', related='product_id.alias_name')
  serial_number = fields.Many2one('stock.production.lot', 'Serial Number')
  install_date = fields.Date('Install Date')
  tracking_number = fields.Char('Tracking Number')

  @api.multi
  def name_get(self):
    result = []
    for row in self:
      components = []
      if row.input_date:
        components.append("%s" % row.input_date)
      if row.partner_id:
        components.append("(%s)" % row.partner_id.alias_name and row.partner_id.alias_name or row.partner_id.name)
      result.append((row.id," ".join(components)))
    return result


