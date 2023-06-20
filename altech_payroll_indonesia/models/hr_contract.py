from odoo import models, fields, api
from odoo.exceptions import UserError

class ResConfigSettingContract(models.TransientModel):
    _inherit = 'res.config.settings'

    contract_days_warning = fields.Float(string='Contarct Days Warning')

    @api.model
    def get_values(self):
        res = super(ResConfigSettingContract,self).get_values()
        IpcSudo = self.env['ir.config_parameter'].sudo()
        contract_days_warning_x = IpcSudo.get_param('contract_days_warning')
        
        res.update(
            contract_days_warning = contract_days_warning_x
        )
        return res
    
    def set_values(self):
        res = super(ResConfigSettingContract,self).set_values()
        self.env['ir.config_parameter'].set_param('contract_days_warning',self.contract_days_warning)
        return res


class ContractComponent(models.Model):
    _name = 'hr.contract.basecomponent'
    _description = 'Contract Attribut Description'

    name = fields.Char(string='Komponen')
    code = fields.Char(string='CODE')

class ContractComponentLines(models.Model):
    _name = 'hr.contract.lines'
    _description = 'Contract Attribut Lines'

    name = fields.Many2one('hr.contract.basecomponent', string='')
    prorate = fields.Selection([("calendar","By Kalender")], string='Prorate Method')
    nilai = fields.Float(string='Nilai')
    contract_id = fields.Many2one('hr.contract', string='Contract Id')

class ContractComponentInherit(models.Model):

    def _get_country_id(self):
        getCountry = self.env['res.country'].search([('code','=','ID')])
        return [('country_id','=',getCountry.id)]
        
    _inherit = 'hr.contract'

    attribut_lines = fields.One2many('hr.contract.lines', 'contract_id', 'Contract Component')
    province_id = fields.Many2one('res.country.state', string='Provinsi',domain=_get_country_id)