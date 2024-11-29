from odoo import models, fields, api, _
from odoo.exceptions import UserError

class masterUpahMinimumProvinsi(models.Model):
    _name = 'hr.master.ump'
    _description = 'Master data Upah Minimum Provinsi'

    def _get_country_id(self):
        getCountry = self.env['res.country'].search([('code','=','ID')])
        return [('country_id','=',getCountry.id)]

    name = fields.Integer(string='UMP Tahun')
    province_id = fields.Many2one('res.country.state', string='Provinsi',domain=_get_country_id)
    ump_nilai = fields.Integer(string='Nilai')
    is_default = fields.Boolean(string='Default')