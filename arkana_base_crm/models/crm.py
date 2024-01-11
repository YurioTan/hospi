from odoo import _, api, fields, models

class LostReason(models.Model):
    _inherit = "crm.lost.reason"
    
    category_reason = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancel', 'Cancel'),
    ], string='Category Reason', index = True,
        copy = False)

class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'
    
    category_reason = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancel', 'Cancel'),
    ], string='Category Reason', index = True,
        copy = False)
    
    def action_lost_reason_apply(self):
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        if self.category_reason == 'won':
            leads.write({'lost_reason' : self.lost_reason_id.id, 'funnel_status' : 'won'})
            return leads.action_set_won_rainbowman()
        else:
            leads.action_set_lost(lost_reason=self.lost_reason_id.id)
            return leads.write({'funnel_status' : 'lost' if self.category_reason == 'lost' else 'cancel'})
    
class CRM(models.Model):
    _inherit = "crm.lead"
    
    # currency_id = fields.Many2one(
    #     'res.currency', 'Currency',
    #     default=lambda self: self.env.company.currency_id.id)
    is_from_leads_menu = fields.Boolean('From Leads Menu')
    e_cat_estimation_date = fields.Date('E-Cat Click Estimation', tracking = True)
    installation_estimation_date = fields.Date('Installation Estimation', tracking = True)
    distributor_id = fields.Many2one('distributor.distributor', string='Distributor',
                            index = True, tracking = True, copy = False)
    budget_source_id = fields.Many2one('budget.source', string='Budget Source',
                            index = True, tracking = True, copy = False)
    brand_id = fields.Many2one('product.brand', string='Brand',
                            index = True, tracking = True, copy = False)
    product_id = fields.Many2one('product.product', string='Product',
                                index = True, tracking = True, copy = False)
    product_name = fields.Char(
        'Product Name', index=True,
        compute='_compute_product_name', readonly=False, store=True)
    product_ids = fields.Many2many('product.product',
        compute='_compute_product_ids',
        string='Product Domain')
    partner_ids = fields.Many2many('res.partner',
        compute='_compute_partner_ids',
        string='Partner Domain')
    list_price = fields.Float('Product Price', related='product_id.list_price', store = True)
    product_qty = fields.Integer('Quantity', default = 0)
    price_subtotal = fields.Float(compute='_compute_price_subtotal', string='Total E-Cat Price', store = True)
    funnel_status = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancel', 'Cancel'),
    ], string='Funnel Status', index = True, tracking = True, copy = False)
    
    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        for rec in self:
            rec.product_id = False if rec.brand_id else False
    
    @api.depends('user_id', 'is_from_leads_menu')
    def _compute_partner_ids(self):
        for rec in self:
            domain = []
            if rec.user_id and rec.is_from_leads_menu:
                domain = [('alias_name', '!=', False), ('is_company', '=', True), '|', ('user_id', '=', False), ('user_id', 'in', rec.user_id.ids)]
            rec.partner_ids = self.env['res.partner'].sudo().search(domain)
            
    @api.depends('brand_id', 'is_from_leads_menu')
    def _compute_product_ids(self):
        for rec in self:
            domain = []
            if rec.brand_id and rec.is_from_leads_menu:
                domain += [('alias_name', '!=', False), ('brand_id', 'in', rec.brand_id.ids)]
            rec.product_ids = self.env['product.product'].sudo().search(domain)
            
    @api.depends('is_from_leads_menu', 'product_id', 'list_price', 'product_qty')
    def _compute_price_subtotal(self):
        for rec in self:
            if rec.product_id and rec.is_from_leads_menu:
                price_subtotal = rec.list_price * rec.product_qty
                rec.price_subtotal = price_subtotal
                rec.expected_revenue = price_subtotal
            else: 
                rec.price_subtotal = 0.0
                rec.expected_revenue = 0.0
    
    @api.depends(lambda self: ['tag_ids', 'stage_id', 'team_id'] + self._pls_get_safe_fields())
    def _compute_probabilities(self):
        lead_probabilities = self._pls_get_naive_bayes_probabilities()
        for lead in self:
            if lead.id in lead_probabilities:
                was_automated = lead.active and lead.is_automated_probability
                lead.automated_probability = lead_probabilities[lead.id]
                if was_automated:
                    lead.probability = lead.automated_probability
    
    def toggle_active(self):
        res = super(CRM, self).toggle_active()
        activated = self.filtered(lambda lead: lead.active)
        archived = self.filtered(lambda lead: not lead.active)
        if activated:
            activated.write({'lost_reason': False, 'funnel_status' : False})
            activated._compute_probabilities()
        if archived:
            archived.write({'probability': 0, 'automated_probability': 0,
                            'funnel_status' : False})
        return res
    
    def _prepare_partner_name_from_partner(self, partner):
        partner_name = partner.parent_id.name if not self.is_from_leads_menu else partner.alias_name
        if not partner_name and partner.is_company:
            partner_name = partner.name
        return {'partner_name': partner_name or self.partner_name}
    
    @api.depends('product_id')
    def _compute_product_name(self):
        for lead in self:
            lead.update(lead._prepare_product_name_from_product(lead.product_id))
    
    def _prepare_product_name_from_product(self, product):
        product_name = product.alias_name
        return {'product_name': product_name or self.product_id.name or ''}

class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'
    _description = 'Convert Lead to Opportunity (not in mass)'
    
    is_from_leads_menu = fields.Boolean('From Leads Menu', related = 'lead_id.is_from_leads_menu')
    
    @api.depends('duplicated_lead_ids', 'lead_id')
    def _compute_name(self):
        for convert in self:
            if not convert.name:
                convert.name = 'convert' if convert.lead_id.is_from_leads_menu else \
                    'merge' if convert.duplicated_lead_ids and len(convert.duplicated_lead_ids) >= 2 else 'convert'

    @api.depends('lead_id')
    def _compute_action(self):
        for convert in self:
            if not convert.lead_id:
                convert.action = 'nothing'
            elif convert.lead_id.is_from_leads_menu:
                convert.action = 'exist'
            else:
                partner = convert.lead_id._find_matching_partner()
                if partner:
                    convert.action = 'exist'
                elif convert.lead_id.contact_name:
                    convert.action = 'create'
                else:
                    convert.action = 'nothing'