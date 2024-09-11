from odoo import api, fields, models

class Ownership(models.Model):
    _name = "partner.ownership"
    _description = "Partner Ownership"

    active = fields.Boolean(default=True)
    name = fields.Char("Name", index=True)

class PartnerCategory(models.Model):
    _name = "partner.category"
    _description = "Wilayah"

    active = fields.Boolean(default=True)
    name = fields.Char("Name", index=True)
    
class PartnerClass(models.Model):
    _name = "partner.class"
    _description = "Kelas RS"

    active = fields.Boolean(default=True)
    name = fields.Char("Name", index=True)
    
class PartnerLocation(models.Model):
    _name = "partner.location"
    _description = "Partner Location"

    active = fields.Boolean(default=True)
    name = fields.Char("Name", index=True)
    
class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Partner'
    
    ownership_id = fields.Many2one('partner.ownership', string='Pemilik',
                    index = True, copy = False, tracking = True)
    partner_location_id = fields.Many2one('partner.location', string='Pulau',
                    index = True, copy = False, tracking = True)
    partner_category_id = fields.Many2one('partner.category', string='Wilayah',
                    index = True, copy = False, tracking = True)
    partner_class_id = fields.Many2one('partner.class', string='Kelas RS',
                    index = True, copy = False, tracking = True)
    alias_name = fields.Char('Alias Name', tracking = True, 
                            copy = False, index = True)
    
    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('partner_search', False):
                if record.alias_name:
                    result.append((record.id, record.alias_name))
                else:
                    result = super(Partner, self).name_get()
                    return result
            else:
                result = super(Partner, self).name_get()
                return result
        return result
