import xlsxwriter
import base64
from io import BytesIO
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ReportPayrollWizard(models.TransientModel):
    _name = 'report.payroll.wizard'
    _description = 'Report Payroll Wizard'

    def _get_payslip_run(self):
        return self.env['hr.payslip.run'].browse(self._context.get('active_ids'))

    payslip_run_id = fields.Many2one('hr.payslip.run', string='Payslip Run', default=_get_payslip_run)
    type_report = fields.Selection([
        ("salary_list_calc", "Payroll Calculation Table"),
        ("bpjs_kesehatan", "Summary BPJS Kesehatan"),
        ("bpjs_tenaker", "Summary BPJS Tenaker")],
        default='salary_list_calc', string='Select Report')

    excel_file = fields.Binary(string='Download Report Excel',)

    def action_download(self):
        if self.type_report == "salary_list_calc":
            return self.report_salary_list_calc()
        if self.type_report == "bpjs_kesehatan":
            return self.report_bpjs_kesehatan()
        if self.type_report == "bpjs_tenaker":
            return self.report_bpjs_tenaker()        
    
    def report_bpjs_tenaker(self):
        file_name = BytesIO()
        workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        run_id = self.payslip_run_id
        ######styling##########
        style1 = workbook.add_format({'bold': True, 'font_size': 14,})
        style2 = workbook.add_format({'bold': False, 'font_size': 12,})
        style3 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#deb4d0', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style4 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#f5f7be', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style5 = workbook.add_format({'font_size': 11,'border': 1})
        style6 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#34ebc6', 'border': 1, 'text_wrap': True,'valign': 'center'})
        #######################
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Report BPJS Ketenagakerjaan",style1)
        cutoff_name = str(self.payslip_run_id.cutoff_periode_id.name)
        worksheet.write(1, 0, cutoff_name,style2)
        tgl = datetime.now()
        worksheet.write(2, 0, tgl.strftime("%d %b %Y %H:%M"), style2)
        worksheet.set_row(4, 30)
        ###################Header Column#################################
        headerKolom = ["No","NIK","NAMA","No Peserta BPJS Kesehatan"]
        lebarKolom = [5, 16, 25, 25]
        kol = 0
        for nn in headerKolom:
            worksheet.write(4, kol, nn, style3)
            worksheet.set_column(kol, kol, lebarKolom[kol])
            kol = kol + 1

        if run_id.payslip_count > 0:
            #get komponen company
            struct_id = run_id.slip_ids[0].struct_id
            rules_ids = struct_id.rule_ids.filtered(lambda x:x.bpjstk_report_type == "company")
            for rl in rules_ids:
                worksheet.write(4, kol, rl.name, style4)
                worksheet.set_column(kol, kol, 12)
                kol = kol + 1
            worksheet.write(4, kol, "Total Iuran Porsi Perusahaan", style4)
            worksheet.set_column(kol, kol, 17)
            kol = kol + 1
            #get komponen employee
            struct_id = run_id.slip_ids[0].struct_id
            rules_ids = struct_id.rule_ids.filtered(lambda x:x.bpjstk_report_type == "employee")
            for rl in rules_ids:
                worksheet.write(4, kol, rl.name, style6)
                worksheet.set_column(kol, kol, 12)
                kol = kol + 1
            worksheet.write(4, kol, "Total Iuran Porsi Pegawai", style6)
            worksheet.set_column(kol, kol, 17)
            kol = kol + 1
        
        worksheet.write(4, kol, "Total Iuran", style3)
        worksheet.set_column(kol, kol, 16)
        no = 1
        baris = 5
        for row in run_id.slip_ids:
            employee_id = row.employee_id
            worksheet.write(baris, 0, no, style5)
            worksheet.write(baris, 1, employee_id.registration_number, style5)
            worksheet.write(baris, 2, employee_id.name, style5)
            worksheet.write(baris, 3, employee_id.no_bpjsks, style5)
            sub_total_1 = 0
            sub_total_2 = 0
            col = 4
            for calc_ids in row.line_ids.filtered(lambda x:x.salary_rule_id.bpjstk_report_type == "company"):
                worksheet.write(baris, col, calc_ids.total, style5)
                sub_total_1 = sub_total_1 + calc_ids.total
                col = col + 1
            worksheet.write(baris, col, sub_total_1, style5)
            col = col + 1
            for calc_ids in row.line_ids.filtered(lambda x:x.salary_rule_id.bpjstk_report_type == "employee"):
                worksheet.write(baris, col, calc_ids.total, style5)
                sub_total_2 = sub_total_2 + calc_ids.total
                col = col + 1
            worksheet.write(baris, col, sub_total_2, style5)
            col = col + 1
            worksheet.write(baris, col, (sub_total_1 + sub_total_2), style5)
            baris = baris + 1
            no = no + 1

        workbook.close()
        file_name.seek(0)
        file_base64 = base64.b64encode(file_name.read())
        file_name.close()
        filename_report = ('Report BPJS Tenaker ') + cutoff_name + '.xlsx'
        self.excel_file = file_base64
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=report.payroll.wizard&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename_report),
            'target': 'self'
        }

    def report_bpjs_kesehatan(self):
        file_name = BytesIO()
        workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        run_id = self.payslip_run_id
        ######styling##########
        style1 = workbook.add_format({'bold': True, 'font_size': 14,})
        style2 = workbook.add_format({'bold': False, 'font_size': 12,})
        style3 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#deb4d0', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style4 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#f5f7be', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style5 = workbook.add_format({'font_size': 11,'border': 1})
        #######################
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Report BPJS Kesehatan",style1)
        cutoff_name = str(self.payslip_run_id.cutoff_periode_id.name)
        worksheet.write(1, 0, cutoff_name,style2)
        tgl = datetime.now()
        worksheet.write(2, 0, tgl.strftime("%d %b %Y %H:%M"), style2)
        worksheet.set_row(4, 30)
        ###################Header Column#################################
        headerKolom = ["No","NIK","NAMA","No Peserta BPJS Kesehatan","UPAH BASIS BPJS","PORSI PERUSAHAAN", "PORSI PEGAWAI", "TOTAL Iuaran BPJS"]
        lebarKolom = [5, 16, 25, 25 ,19, 19, 19, 20]
        kol = 0
        for nn in headerKolom:
            worksheet.write(4, kol, nn, style3)
            worksheet.set_column(kol, kol, lebarKolom[kol])
            kol = kol + 1
        # #Kontent
        no = 1
        baris = 5
        for row in run_id.slip_ids:
            employee_id = row.employee_id
            worksheet.write(baris, 0, no, style5)
            worksheet.write(baris, 1, employee_id.registration_number, style5)
            worksheet.write(baris, 2, employee_id.name, style5)
            worksheet.write(baris, 3, employee_id.no_bpjsks, style5)
            sub_total = 0
            for calc_ids in row.line_ids.filtered(lambda x:x.salary_rule_id.bpjs_report_type != False):
                if calc_ids.salary_rule_id.bpjs_report_type == "basis":
                    worksheet.write(baris, 4, calc_ids.total, style5)
                    sub_total = sub_total + calc_ids.total
                if calc_ids.salary_rule_id.bpjs_report_type == "company":
                    worksheet.write(baris, 5, calc_ids.total, style5)
                    sub_total = sub_total + calc_ids.total
                if calc_ids.salary_rule_id.bpjs_report_type == "employee":
                    worksheet.write(baris, 6, calc_ids.total, style5)
                    sub_total = sub_total + calc_ids.total
            worksheet.write(baris, 7, sub_total, style5)
            baris = baris + 1
            no = no + 1

        workbook.close()
        file_name.seek(0)
        file_base64 = base64.b64encode(file_name.read())
        file_name.close()
        filename_report = ('Report BPJS Kesehatan ') + cutoff_name + '.xlsx'
        self.excel_file = file_base64
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=report.payroll.wizard&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename_report),
            'target': 'self'
        }
    
    def report_salary_list_calc(self):
        file_name = BytesIO()
        workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        run_id = self.payslip_run_id
        ######styling##########
        style1 = workbook.add_format({'bold': True, 'font_size': 14,})
        style2 = workbook.add_format({'bold': False, 'font_size': 12,})
        style3 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#deb4d0', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style4 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#f5f7be', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style5 = workbook.add_format({'font_size': 11,'border': 1})
        #######################
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, self.payslip_run_id.name,style1)
        worksheet.write(1, 0, str(self.payslip_run_id.cutoff_periode_id.name),style2)
        tgl = datetime.now()
        worksheet.write(2, 0, tgl.strftime("%d %b %Y %H:%M"), style2)
        worksheet.set_row(4, 30)
        ###################Header Column#################################
        headerKolom = ["No","NIK","NAMA","Department","Position","Frist Contract Date","End Contract Date","NPWP","PTKP Code"]
        lebarKolom = [5, 16, 25,18 ,18, 14, 14, 20, 9]
        kol = 0
        for nn in headerKolom:
            worksheet.write(4, kol, nn, style3)
            worksheet.set_column(kol, kol, lebarKolom[kol])
            kol = kol + 1
        kol = len(headerKolom)
        if run_id.payslip_count > 0:
            #get komponen
            struct_id = run_id.slip_ids[0].struct_id
            rules_ids = struct_id.rule_ids.filtered(lambda x:x.show_in_excel_list == True)
            for rl in rules_ids:
                worksheet.write(4, kol, rl.name, style4)
                kol = kol + 1
        worksheet.write(4, kol, "Takehome Pay", style4)
        worksheet.set_column(len(headerKolom), kol, 14)
        kol = kol + 1
        worksheet.write(4, kol, "Nama Bank", style3)
        worksheet.set_column(kol, kol, 18)
        kol = kol + 1
        worksheet.write(4, kol, "Nomor Rekening", style3)
        worksheet.set_column(kol, kol, 18)
        #Kontent
        no = 1
        baris = 5
        for row in run_id.slip_ids:
            employee_id = row.employee_id
            worksheet.write(baris, 0, no, style5)
            worksheet.write(baris, 1, employee_id.registration_number, style5)
            worksheet.write(baris, 2, employee_id.name, style5)
            worksheet.write(baris, 3, employee_id.department_id.name, style5)
            worksheet.write(baris, 4, employee_id.job_title, style5)
            worksheet.write(baris, 5, row.contract_id.first_contract_date.isoformat(), style5)
            if row.contract_id.date_end != False:
                worksheet.write(baris, 6, row.contract_id.date_end.isoformat(), style5)
            else:
                worksheet.write(baris, 6, "", style5)
            worksheet.write(baris, 7, employee_id.no_npwp, style5)
            worksheet.write(baris, 8, employee_id.ptkp_id.name, style5)
            kol = len(headerKolom)
            for calc_ids in row.line_ids.filtered(lambda x:x.salary_rule_id.show_in_excel_list == True):
                worksheet.write(baris, kol, calc_ids.total, style5)
                kol = kol + 1
            worksheet.write(baris, kol, row.amt_thp, style5)
            worksheet.write(baris, kol + 1, employee_id.bank_account_id.bank_id.name, style5)
            worksheet.write(baris, kol + 2, employee_id.bank_account_id.acc_number, style5)

            baris = baris + 1
            no = no + 1

        workbook.close()
        file_name.seek(0)
        file_base64 = base64.b64encode(file_name.read())
        file_name.close()
        batch_name = self.payslip_run_id.name
        filename_report = ('Payslip Calculation ') + str(batch_name) + '.xlsx'
        self.excel_file = file_base64
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=report.payroll.wizard&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename_report),
            'target': 'self'
        }