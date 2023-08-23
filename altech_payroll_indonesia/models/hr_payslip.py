from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AltechHrEmployeePayslips(models.Model):
    _inherit = 'hr.payslip'

    is_last_slip = fields.Boolean(string='Last Slip')
    cutoff_periode_id = fields.Many2one('cutoff.periode', string='Cutoff Periode',related="payslip_run_id.cutoff_periode_id")
    tahun_pajak = fields.Integer(string='Tahun Pajak', related="cutoff_periode_id.tax_year")
    masa_pajak = fields.Selection([
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10'),
        ('11','11'),
        ('12','12')], string='Masa Pajak', related="cutoff_periode_id.tax_period_month")
    ##########
    amt_income_data = fields.Float(string='INCOME', compute='get_amount_income')
    amt_deduction_data = fields.Float(string='DEDUCTION', compute='get_amount_deduction')
    amt_comp_contribut = fields.Float(string='COMP. CONTRIBUTION', compute='get_amount_comp_contrib')
    amt_thp = fields.Float(string='Takehome Pay', compute='get_amount_thp')

    def action_print_payslip(self):
        return self.env.ref('altech_payroll_indonesia.action_report_recap_payslip').report_action(self)

    @api.depends('line_ids')
    def get_amount_income(self):
        for doc in self:
            hasil = 0
            for baris in doc.line_ids:
                if baris.code == 'BRUTO':
                    hasil = hasil + baris.total
            doc.amt_income_data = hasil
    
    @api.depends('line_ids')
    def get_amount_deduction(self):
        for doc in self:
            hasil = 0
            for baris in doc.line_ids:
                if baris.category_id.code == 'ALT_DEDUCTION':
                    hasil = hasil + baris.total
                if baris.category_id.code == 'ALT_DEDUCTION_TAX':
                    hasil = hasil + baris.total
            doc.amt_deduction_data = hasil
    
    @api.depends('line_ids')
    def get_amount_comp_contrib(self):
        for doc in self:
            hasil = 0
            for baris in doc.line_ids:
                if baris.category_id.code == 'ALT_COMP_CONTRIB_TAX':
                    hasil = hasil + baris.total
                if baris.category_id.code == 'ALT_COMP_CONTRIB':
                    hasil = hasil + baris.total
            doc.amt_comp_contribut = hasil
    
    @api.depends('amt_income_data', 'amt_deduction_data')
    def get_amount_thp(self):
        for doc in self:
            doc.amt_thp = doc.amt_income_data - doc.amt_deduction_data

    def get_days_prorate(self):
        lama_kerja = 0
        hasil = {}
        selisih  = self.date_to - self.date_from
        lama_hari = selisih.days + 1
        is_prorate = False
        cek1 = False
        cek2 = False
        if self.contract_id.date_start <= self.date_to and self.contract_id.date_start >= self.date_from:
            selisih1 = self.date_to - self.contract_id.date_start
            lama_kerja = selisih1.days + 1
            is_prorate = True
            cek1 = True
        if self.contract_id.date_end != False:
            if self.contract_id.date_end >= self.date_from and self.contract_id.date_end <= self.date_to:
                selisih2 = self.date_to - self.contract_id.date_end
                lama_kerja = selisih2.days
                is_prorate = True
                cek2 = True
        if cek1 and cek2:
            selisih3 = self.contract_id.date_end - self.contract_id.date_start
            lama_kerja = selisih3.days + 1
        if is_prorate:
            hasil['kalender'] = lama_hari
            hasil['aktif'] = lama_kerja
        else:
            hasil['kalender'] = lama_hari
            hasil['aktif'] = lama_hari
        return hasil
    
    def action_payslip_done(self):
        for doc in self:
            super(AltechHrEmployeePayslips, doc).action_payslip_done()
            get_pinjaman = doc.env['hr.pinjaman.line'].search(['&','&','&',('cutoff_periode_id','=',doc.cutoff_periode_id.id),('state','=','open'),('pinjaman_id.employee_id','=',doc.employee_id.id),('pinjaman_id.state','=','progress')])
            for ls in get_pinjaman:
                ls.state = 'done'
class InheritPayslipLineEmployee(models.Model):
    _inherit = 'hr.payslip.line'

    report_mode = fields.Selection(
        [("timesheet", "Timesheet"), ("contract", "Contract Reference"), ("income", "Income"),
         ("deduction", "Deduction"), ("comp", "Company Contribution")], related="salary_rule_id.report_mode",
        string='Report Category')

    code_grup = fields.Char(string='Code Group', related="category_id.code")
    
    notes = fields.Text(string='Notes', related="salary_rule_id.note")