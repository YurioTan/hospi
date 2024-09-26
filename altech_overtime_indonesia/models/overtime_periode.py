from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pytz
import base64
import xlwt
import math
from io import BytesIO
from pprint import pprint

class LemburOvertimePeriode(models.Model):
    _name = 'lembur.overtime.periode'

    name = fields.Char(string='Periode Overtime')
    tanggal_awal = fields.Date(string='Tanggal Awal')
    tanggal_akhir = fields.Date(string='Tanggal Akhir')
    excel_file = fields.Binary(string='Download Report Excel', readonly="1")
    active = fields.Boolean(string='Active',default=True)

    @api.model
    def create(self, vals):
        cc = fields.Date.from_string(vals['tanggal_akhir']) - fields.Date.from_string(vals['tanggal_awal'])
        if cc.days < 0:
            raise UserError('Format Range Tanggal tidak tepat')
        else:
            return super(LemburOvertimePeriode, self).create(vals)

    def confirm_all(self):
        gg = self.env['lembur.overtime.calculation'].search([('overtime_group','=',self.id)])
        for ls in gg:
            ls.confirm_overtime()

    def done_all(self):
        gg = self.env['lembur.overtime.calculation'].search([('overtime_group','=',self.id)])
        for ls in gg:
            ls.state = 'done'
    
    def write(self,vals):
        awal = self.tanggal_awal
        akhir = self.tanggal_akhir
        if vals.get('tanggal_awal',False):
            awal = vals['tanggal_awal']
        if vals.get('tanggal_akhir',False):
            akhir = vals['tanggal_akhir']
        cc = fields.Date.from_string(akhir) - fields.Date.from_string(awal)
        if cc.days < 0:
            raise UserError('Format Range Tanggal tidak tepat')
        else:
            return super(LemburOvertimePeriode, self).write(vals)

    def report_to_excel(self):
        workbook = xlwt.Workbook(encoding="UTF-8")
        # salarygroup = self.env['hr.employeesalgroup'].search([('id','>',0)])
        # for salgrup in salarygroup:
        worksheet = workbook.add_sheet(self.name,cell_overwrite_ok=True)
        style0 = xlwt.easyxf('font: bold True, color black; align: horiz center;')
        style1 = xlwt.easyxf('font: bold True, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color gray40; align: horiz center;')
        style2 = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
        namakolom = ['No','NIK','Name','Position','Employee Status','Join Date','Resign Date','Base Overtime','Total Days','Total','Calculation OT','Overtime Rate','Overtime Allowance','Status']
        lebarkolom = [4,15,20,20,20,15,15,15,15,15,15,20,23,20]
        worksheet.write(0,1,self.name,style0)
        kolom = 0
        for head1 in namakolom:
            worksheet.write(1,kolom,head1,style1)
            worksheet.col(kolom).width = 256 * lebarkolom[kolom]
            kolom = kolom + 1
        baris = 2
        # gg = self.env['lembur.overtime.calculation'].search(['&',('overtime_group','=',self.id),('employee_sal_grup','=',salgrup.id)])
        gg = self.env['lembur.overtime.calculation'].search([('overtime_group','=',self.id)])
        nomor = 1
        for ls in gg:
            worksheet.write(baris,0,nomor,style2)
            employee = ls.employee_id
            worksheet.write(baris,1,'',style2)
            # if employee.emp_id == False:
            #     worksheet.write(baris,1,'',style2)
            # else:
            #     worksheet.write(baris,1,employee.emp_id,style2)
            worksheet.write(baris,2,employee.name,style2)
            namestat = ''
            if employee.job_id.name != False:
                namestat = employee.job_id.name
            worksheet.write(baris,3,namestat,style2)
            namestat = ''
            # if employee.employeestat.name != False:
            #     namestat = employee.employeestat.name
            worksheet.write(baris,4,namestat,style2)
            # if employee.joining_date == False:
            #     worksheet.write(baris,5,'',style2)
            # else:
            #     worksheet.write(baris,5,employee.joining_date,style2)
            worksheet.write(baris,5,'',style2)
            worksheet.write(baris,6,'',style2)
            kontrak = employee.contract_id
            if kontrak.id == False:
                wage = 0
            else:
                wage = kontrak.wage
            wage173 = wage / 173
            worksheet.write(baris,7,wage,style2)
            banyak = 0
            waktuX = 0
            for cln in ls.calculation_line:
                banyak = banyak + 1
                waktuX = waktuX + cln.ot_total
            worksheet.write(baris,8,banyak,style2)
            worksheet.write(baris,9,waktuX,style2)
            worksheet.write(baris,10,ls.overtime_total,style2)
            worksheet.write(baris,11,wage173,style2)
            worksheet.write(baris,12,(wage173 * ls.overtime_total),style2)
            worksheet.write(baris,13,ls.state,style2)

            nomor = nomor + 1
            baris = baris + 1
        fp = BytesIO()
        workbook.save(fp)
        self.excel_file = base64.encodestring(fp.getvalue())
        fp.close()
        return {
            'type' : 'ir.actions.act_url',
            'url' : 'web/content/?model=lembur.overtime.periode&field=excel_file&download=true&id=%s&filename=Overtime_Report_list.xls'%(self.id),
            'target' : 'new'
        }