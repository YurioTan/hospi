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
  delivery_partner_id = fields.Many2one('res.partner', 'Deliver To')

  customer_db_ids = fields.One2many('sale.customer.db', 'sale_order_id', 'Customer DB')
  customer_db_count = fields.Integer('Customer DB Count', compute="_compute_customer_db")

  def _compute_customer_db(self):
    for row in self:
      row.customer_db_count = len(row.customer_db_ids)

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
  
  def action_cancel(self):
    result = super(SaleOder, self).action_cancel()
    for row in self:
      row.customer_db_ids.unlink()
    return result

  def action_create_customer_db(self):
    self.ensure_one()
    from_cron = self.env.context.get('from_cron', False)
    # cek sudah ada belum, kecuali dilewat
    customer_dbs = self.env['sale.customer.db'].search([('sale_order_id','=',self.id)])
    if not from_cron:
      if len(customer_dbs) > 0:
        raise ValidationError('Customer database already exists for this SO. Please delete first if you want to recreate it.')  
    else:
      if len(customer_dbs) > 0:
        return True
    if not self.partner_id.alias_name:
        raise ValidationError('Please set alias name for the customer of this order.')  
    create_count = 0
    for line in self.order_line:
      product_category_name = line.product_id.categ_id.name.lower()
      if not product_category_name.startswith('finished good'): continue
      new_customer_db = self.env['sale.customer.db'].create({
        'input_date': self.date_order,
        'sale_order_id': self.id,
        'partner_id': self.partner_id.id,
        'delivery_partner_id': self.delivery_partner_id.id,
        'brand_id': line.product_id.brand_id.id,
        'product_id': line.product_id.id,
        # 'serial_number': None,
        # 'install_date': None,
        'tracking_number': self.client_order_ref,
      })
      if new_customer_db: create_count += 1
    if not from_cron:
      if create_count > 0:
        return self.action_view_customer_db()
      else:
        raise ValidationError('No customer database created, all items in this SO is non-finished good.')

  def action_view_customer_db(self):
    xmlid = "hn_sale.action_sale_customer_db"
    action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
    customer_dbs = self.env['sale.customer.db'].search([('sale_order_id','=',self.id)])
    if len(customer_dbs) > 1:
      action['domain'] = [('sale_order_id','=',self.id)]
    elif len(customer_dbs) == 1:
      action["views"] = [(self.env.ref("hn_sale.sale_customer_db_view_form").id, "form")]
      action['res_id'] = customer_dbs.id
    else:
      raise ValidationError('No customer database created for this SO yet.')
    return action
  
  def cron_generate_customer_db(self):
    sale_orders = self.env['sale.order'].search([('state','=','sale')])
    for order in sale_orders:
      order.with_context({'from_cron': True}).action_create_customer_db()
