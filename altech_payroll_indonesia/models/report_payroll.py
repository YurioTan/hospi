import xlsxwriter
import base64
from io import BytesIO

from odoo import fields, models, api, _
from odoo.exceptions import UserError

class WizardReportPph21i(models.TransientModel):

    _name = 'wizard.pph21.i.wizard'
    _description = 'Wizard PPh21-I'

    tahun_pajak = fields.Integer(string='Tahun Pajak')
    masa_pajak = fields.Selection([
        ('1','1'),('2','2'),('3','3'),('4','4'),
        ('5','5'),('6','6'),('7','7'),('8','8'),
        ('9','9'),('10','10'),('11','11'),('12','12')], string='Masa Pajak')
    excel_file = fields.Binary(string='Download Report Excel',)
    
    @api.model
    def default_get(self, xx):
        res = super(WizardReportPph21i, self).default_get(xx)
        res.update({'tahun_pajak': fields.Date.today().year})
        return res
    
    def download_excel_pph21(self):
        file_name = BytesIO()
        workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        style3 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#deb4d0', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style5 = workbook.add_format({'font_size': 11,'border': 1})
        # #######################
        worksheet = workbook.add_worksheet()
        # ###################Header Column#################################
        headerKolom = ["Masa Pajak","Tahun Pajak","Pembetulan","NPWP","Nama","Kode Pajak","Jumlah Bruto","Jumlah PPh","Kode Negara"]
        lebarKolom = [11, 11, 14, 12,12,16,13,11,13]
        kol = 0
        for nn in headerKolom:
            worksheet.write(0, kol, nn, style3)
            worksheet.set_column(kol, kol, lebarKolom[kol])
            kol = kol + 1
        sql1 = """select T1.*, T2.bruto, T3.pph21 from (select he.id, he.name, he.no_npwp from hr_payslip hp
                    left join hr_employee he ON he.id = hp.employee_id
                    left join hr_payslip_run hpr ON hpr.id = hp.payslip_run_id
                    left join cutoff_periode cp ON cp.id = hpr.cutoff_periode_id
                    where hp.company_id = """+str(self.env.company.id)+""" and hp.state in ('verify','done')
                    and cp.tax_year = """+str(self.tahun_pajak)+""" and cp.tax_period_month = '"""+str(self.masa_pajak)+"""'
                    group by he.id) T1
                    left join (
                        select  sum(hpl.total) as bruto,hp.employee_id from hr_payslip_line hpl
                        left join hr_payslip hp ON hp.id = hpl.slip_id
                        left join hr_payslip_run hpr ON hpr.id = hp.payslip_run_id
                        left join cutoff_periode cp ON cp.id = hpr.cutoff_periode_id
                        where hpl.code = 'BRUTO_TAX_ALL'  and hp.company_id = """+str(self.env.company.id)+""" 
                        and hp.state in ('verify','done') 
                        and cp.tax_year = """+str(self.tahun_pajak)+""" and cp.tax_period_month = '"""+str(self.masa_pajak)+"""'
                        group by hp.employee_id
                    ) T2 ON T2.employee_id = T1.id
                    left join (
                        select  sum(hpl.total) as pph21,hp.employee_id from hr_payslip_line hpl
                        left join hr_payslip hp ON hp.id = hpl.slip_id
                        left join hr_payslip_run hpr ON hpr.id = hp.payslip_run_id
                        left join cutoff_periode cp ON cp.id = hpr.cutoff_periode_id
                        where hpl.code = 'PPH21_ALL'  and hp.company_id = """+str(self.env.company.id)+"""  
                        and hp.state in ('verify','done') 
                        and cp.tax_year = """+str(self.tahun_pajak)+""" and cp.tax_period_month = '"""+str(self.masa_pajak)+"""'
                        group by hp.employee_id
                    ) T3 ON T3.employee_id = T1.id"""
        self.env.cr.execute(sql1)
        get_data = self.env.cr.dictfetchall()
        baris = 1
        for ls in get_data:
            worksheet.write(baris, 0, self.masa_pajak, style5)
            worksheet.write(baris, 1, self.tahun_pajak, style5)
            worksheet.write(baris, 2, "", style5)
            worksheet.write(baris, 3, ls['no_npwp'], style5)
            worksheet.write(baris, 4, ls['name'], style5)
            worksheet.write(baris, 5, "21-100-1", style5)
            worksheet.write(baris, 6, ls['bruto'], style5)
            worksheet.write(baris, 7, ls['pph21'], style5)
            worksheet.write(baris, 8, "", style5)
            baris = baris + 1

        workbook.close()
        file_name.seek(0)
        file_base64 = base64.b64encode(file_name.read())
        file_name.close()
        filename_report = ('Report_PPh21-I.xlsx')
        self.excel_file = file_base64
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=wizard.pph21.i.wizard&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename_report),
            'target': 'self'
        }
    
class WizardReportPph211721(models.TransientModel):

    _name = 'wizard.pph21.i'
    _description = 'Wizard PPh21-1721'

    tahun_pajak = fields.Integer(string='Tahun Pajak')
    masa_pajak = fields.Selection([
        ('1','1'),('2','2'),('3','3'),('4','4'),
        ('5','5'),('6','6'),('7','7'),('8','8'),
        ('9','9'),('10','10'),('11','11'),('12','12')], string='Masa Pajak')
    excel_file = fields.Binary(string='Download Report Excel',)

    @api.model
    def default_get(self, xx):
        res = super(WizardReportPph211721, self).default_get(xx)
        res.update({'tahun_pajak': fields.Date.today().year})
        return res
    
    def download_excel_1721(self):
        file_name = BytesIO()
        workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        style3 = workbook.add_format({'bold': True, 'font_size': 11, 'fg_color': '#deb4d0', 'border': 1, 'text_wrap': True,'valign': 'center'})
        style5 = workbook.add_format({'font_size': 11,'border': 1})
        # #######################
        worksheet = workbook.add_worksheet()
        # ###################Header Column#################################
        headerKolom = ["Masa Pajak","Tahun Pajak","Pembetulan","Nomor Bukti Potong",
                       "Masa Perolehan Awal","Masa Perolehan Akhir","NPWP","NIK",
                       "Nama","Alamat","Jenis Kelamin","Status PTKP","Jumlah Tanggungan",
                       "Nama Jabatan","WP Luar Negeri","Kode Negara", "Kode Pajak",
                       "Jumlah 1","Jumlah 2","Jumlah 3","Jumlah 4", "Jumlah 5",
                       "Jumlah 6","Jumlah 7","Jumlah 8","Jumlah 9", "Jumlah 10",
                       "Jumlah 11","Jumlah 12","Jumlah 13","Jumlah 14", "Jumlah 15",
                       "Jumlah 16","Jumlah 17","Jumlah 18","Jumlah 19", "Jumlah 20",
                       "Status Pindah","NPWP Pemotong","Nama Pemotong", "Tanggal Bukti Potong"]
        lebarKolom = [8, 8,12,15,10,10,23,15,27,30,10,10,12,25,11,9,15,
                      11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,
                      12,26,20,16]
        kol = 0
        for nn in headerKolom:
            worksheet.write(0, kol, nn, style3)
            worksheet.set_column(kol, kol, lebarKolom[kol])
            kol = kol + 1
        sql1 = """select he.id, he.name, he.no_npwp ,he.gender,
                min(cp.tax_period_month) as awal, max(cp.tax_period_month) as akhir
                from hr_payslip hp
                left join hr_employee he ON he.id = hp.employee_id
                left join hr_payslip_run hpr ON hpr.id = hp.payslip_run_id
                left join cutoff_periode cp ON cp.id = hpr.cutoff_periode_id
                where hp.company_id = """+str(self.env.company.id)+""" and hp.state in ('verify','done')
                and cp.tax_year = """+str(self.tahun_pajak)+""" and cp.tax_period_month <= '"""+str(self.masa_pajak)+"""'
                group by he.id
                """
        self.env.cr.execute(sql1)
        get_data = self.env.cr.dictfetchall()
        baris = 1
        for ls in get_data:
            worksheet.write(baris, 0, self.masa_pajak, style5)
            worksheet.write(baris, 1, self.tahun_pajak, style5)
            worksheet.write(baris, 2, "", style5)
            get_nomor = self._get_nomor(baris,self.masa_pajak, self.tahun_pajak)
            worksheet.write(baris, 3, get_nomor, style5)
            worksheet.write(baris, 4, ls['awal'], style5)
            worksheet.write(baris, 5, ls['akhir'], style5)
            worksheet.write(baris, 6, ls['no_npwp'], style5)
            worksheet.write(baris, 7, "", style5)
            worksheet.write(baris, 8, ls['name'], style5)
            worksheet.write(baris, 9, "", style5)
            lk = ""
            if ls['gender']== "male":
                lk = "M"
            if ls['gender']== "female":
                lk = "F"
            worksheet.write(baris, 10, lk, style5)
        #     worksheet.write(baris, 5, "21-100-1", style5)
        #     worksheet.write(baris, 6, ls['bruto'], style5)
        #     worksheet.write(baris, 7, ls['pph21'], style5)
        #     worksheet.write(baris, 8, "", style5)
            baris = baris + 1

        workbook.close()
        file_name.seek(0)
        file_base64 = base64.b64encode(file_name.read())
        file_name.close()
        filename_report = ('Report_PPh21-1721-A1.xlsx')
        self.excel_file = file_base64
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=wizard.pph21.i&field=excel_file&download=true&id=%s&filename=%s' % (
                self.id, filename_report),
            'target': 'self'
        }

    def _get_nomor(self, urutan, bulan,tahun):
        if urutan < 10:
            angka = "0000" + str(urutan)
        elif urutan < 100:
            angka = "000" + str(urutan)
        elif urutan < 1000:
            angka = "00" + str(urutan)
        elif urutan < 10000:
            angka = "0" + str(urutan)
        else:
            angka = str(urutan)
        output = "1.1-"+str(bulan)+"."+str(tahun)+"-"+str(angka)
        return output