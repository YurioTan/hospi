from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import xlwt
import pytz
from io import BytesIO
from pprint import pprint
from datetime import datetime
import math

class payrollPph21PayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    cutoff_periode_id = fields.Many2one('cutoff.periode', string='Cutoff Periode')

    def recompute_batch_sheet(self):
        for baris in self.slip_ids:
            baris.compute_sheet()

    @api.onchange('cutoff_periode_id')
    def _onchange_cutoff_periode(self):
        if self.cutoff_periode_id:
            self.date_start = self.cutoff_periode_id.date_start
            self.date_end = self.cutoff_periode_id.date_end
            
    def download_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payroll Calculation Table'),
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'report.payroll.wizard',
            'view_id': self.env.ref('altech_payroll_indonesia.report_payroll_wizard_view_form').id,
            'context': {'active_id': self.id},
        }