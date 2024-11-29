from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class PayrollInheritHrEmployee(models.Model):
    _inherit = "hr.employee"

    def get_usia(self):
        umur = relativedelta(fields.Date.today(), self.birthday).years
        return umur

    have_bpjsks = fields.Boolean(string='BPJS Kesehatan')
    have_bpjstk = fields.Boolean(string='BPJS Tenaker')
    have_pension = fields.Boolean(string='BPJS Pensiun')
    have_npwp = fields.Boolean(string='NPWP')

    no_npwp = fields.Char(string='No. NPWP')
    no_bpjsks = fields.Char(string='No. BPJS KES')
    no_bpkstk = fields.Char(string='No. BPJS TK')
    no_pension = fields.Char(string='No. Pension')

    resiko_kerja = fields.Many2one('hr.jkktabel', string='Resiko Lokasi Kerja')
    ptkp_id = fields.Many2one('hr.ptkp', string='PTKP Code')
    full_thr = fields.Boolean(string='Get Full THR')
    