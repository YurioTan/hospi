from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    alias_name = fields.Char('Alias Name', tracking = True, 
                            copy = False, index = True)
    brand_id = fields.Many2one('product.brand', string='Brand',
                        copy = False, index = True, tracking = True)
    
    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'default_code', 'alias_name'])
        if self.env.context.get('product_search', False):
            return [(template.id, '%s' % (template.alias_name and template.alias_name or template.name))
                    for template in self]
        else : 
            return super(ProductTemplate, self).name_get()

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    def name_get(self):
        if self.env.context.get('product_search', False):
            return [(template.id, '%s' % (template.product_tmpl_id.alias_name and template.product_tmpl_id.alias_name or template.product_tmpl_id.name))
                    for template in self]
        else:
            return super(ProductProduct, self).name_get()