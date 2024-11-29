from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from datetime import datetime
from datetime import timedelta
import pytz
import base64
import xlwt
import math
from io import BytesIO

class EnhancedPayrollOvertimeLembur(models.Model):
    _name = 'lembur.overtime.calculation'

    def _get_config_basis(self):
        get_conf = self.env['ir.config_parameter'].sudo().get_param('aletch.basis_perhitungan')        
        return get_conf
    
    def _get_config_granulity(self):
        get_conf = self.env['ir.config_parameter'].sudo().get_param('aletch.overtime_granulity')        
        return get_conf
    
    name = fields.Char(string='Description', compute='get_name_descirption', store=True,)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    overtime_group = fields.Many2one('lembur.overtime.periode', string='Overtime Periode')
    calculation_line = fields.One2many('lembur.overtime.calculation.line', 'calculation_id', string='Overtime Calculations')
    state = fields.Selection([("draft","Draft"),("waiting","Waiting"),("confirm","Confirmed"),("done","Done")], string='Status', default="draft", track_visibility="onchange")
    overtime_total = fields.Float(string='Total Overtime', compute='_compute_total_jam_real', store=True,)
    estimasi_total = fields.Float(string='Estimasi Nilai OT')
    overtime_jam = fields.Float(compute='_compute_total_jam_real', string='Total Real Jam')
    basis_perhitungan = fields.Selection([("manual","Manual"),("wt","Working Times")], string='Resources',default=lambda self: self._get_config_basis())
    overtime_granulity = fields.Selection([("rounding60d","60 menit Down"),("rounding30d","30 menit Down"),
                                           ("prorate","Prorate"),
                                           ("rounding30u","30 menit UP"),("rounding60u","60 menit UP")], string='Granulity', default=lambda self : self._get_config_granulity())
    
    note = fields.Text(string='Catatan')
    excel_file = fields.Binary(string='Download Report Excel', readonly="1")

    @api.constrains('calculation_line')
    def _check_exist_product_in_line(self):
      for doc in self:
          exist_date_list = []
          for line in doc.calculation_line:
             if line.name in exist_date_list:
                raise ValidationError(_('Duplicate date '+str(line.name.__format__("%d %b %Y"))+' in same line'))
             exist_date_list.append(line.name)

    
    @api.depends('employee_id', 'overtime_group')
    def get_name_descirption(self):
        for doc in self:
            hasil = 'Description'
            if doc.employee_id.id != False:
                hasil = str(doc.employee_id.name)
            if doc.overtime_group.id != False:
                hasil = hasil + ' - ' + str(doc.overtime_group.name)
            doc.name = hasil
    
    @api.depends('calculation_line')
    def _compute_total_jam_real(self):
        for order_doc in self:
            order_doc.overtime_jam = sum(order_doc.calculation_line.mapped('ot_total'))
            order_doc.overtime_total = sum(order_doc.calculation_line.mapped('ot_round'))

    def generate_days(self):
        clearall = []
        for linex in self.calculation_line:
            clearall.append((2,linex.id))
            linex.unlink()
        self.calculation_line = clearall
        
        d1 = fields.Date.from_string(self.overtime_group.tanggal_awal)
        d2 = fields.Date.from_string(self.overtime_group.tanggal_akhir)
        selisihdate = (d2 - d1).days
        baris = []
        nIncrement = 0
        while selisihdate >= 0:
            tglbaru = d1 + timedelta(days=nIncrement)
            baris.append((0,0,{'name':tglbaru.strftime("%Y-%m-%d")}))
            selisihdate = selisihdate - 1
            nIncrement = nIncrement + 1
        self.calculation_line = baris

    def submit_overtime(self):
        for doc in self:
            cek = doc.calculation_line.filtered(lambda x: x.state != 'draft')
            if len(cek) > 0:
                raise UserError('Hanya data draft yang dapat di submit')
            else:
                doc.state = 'waiting'
    
    def set_to_draft(self):
        for doc in self:
            doc.state = 'draft'
        
    def set_to_rollback(self):
        update_data = []
        dihapus = []
        for baris in self.calculation_line:
            update_data.append((1,baris.id,{'state': 'draft', 'employee_ot': False}))
            dihapus.append(baris.employee_ot)
        self.calculation_line = update_data
        self.state = 'draft'
        self.estimasi_total = 0
        for hapus in dihapus:
            hapus.unlink()

    def confirm_overtime(self):
        for doc in self:
            nilai = 0
            updatex = []
            for baris in doc.calculation_line:
                isian = []
                isibaru = {}
                if baris.state == 'draft':
                    isibaru = {'name':doc.employee_id.id,'date_ot': baris.name,'ot1_in': baris.ot1_in,'ot1_out': baris.ot1_out, 'ot2_in': baris.ot2_in, 'ot2_out': baris.ot2_out, 'state' : 'confirm'}
                    isian.append(1)
                    isian.append(baris.id)
                    nilai = nilai + baris.ot_round
                    idbaru = self.env['employee.lembur.overtime'].create(isibaru)
                    isian.append({'state' : 'confirm','employee_ot': idbaru.id})
                elif baris.state == 'confirm':
                    updatedata = {'ot1_in': baris.ot1_in,'ot1_out': baris.ot1_out, 'ot2_in': baris.ot2_in, 'ot2_out': baris.ot2_out}
                    nilai = nilai + baris.ot_round
                    kk = self.env['lembur.employee'].browse(baris.employee_ot.id)
                    kk.write(updatedata)
                    isian.append(4)
                    isian.append(baris.id)
                    isian.append(False)
                else:
                    isian.append(4)
                    isian.append(baris.id)
                    isian.append(False)
                updatex.append(isian)
            self.overtime_total = nilai
            self.state = 'confirm'
            self.calculation_line = updatex

            gaji = 0
            datalines = self.employee_id.contract_id.attribut_lines
            for bb in datalines:
                if bb.name.overtime_rate == True:
                    gaji = gaji + bb.nilai
            get_amt = self.env['ir.config_parameter'].sudo().get_param('aletch.overtime_pembagi')
            self.estimasi_total = nilai * gaji / int(get_amt)
        
    def _convenrttotime(self,nilai):
        hasil = ''
        depan = math.floor(nilai)
        menit = nilai - depan
        menit = menit * 60
        menit = int(round(menit,0))
        if depan < 10:
            hasil = '0' + str(depan)
        else:
            hasil = str(depan)
        if menit < 10:
            hasil = hasil +  ':0' + str(menit)
        else:
            hasil = hasil + ':' + str(menit)
        return hasil
    
    def _setGetTime(self, nilai, granulity):
        aa = {}
        aa['set'] = ''
        aa['sisa'] = 0
        if nilai >= 1:
            aa['set'] = 1
            aa['sisa'] = nilai - 1
        else:
            if nilai == 0:
                aa['set'] = ''
                aa['sisa'] = 0
            else:
                if granulity == 'prorate':
                    nilai2 = nilai
                if granulity == 'rounding30d':
                    if nilai < 0.5:
                        nilai2 = 0
                    else:
                        nilai2 = 0.5
                if granulity == 'rounding30u':
                    if nilai <= 0.5:
                        nilai2 = 0.5
                    else:
                        nilai2 = 1
                if granulity == 'rounding60d':
                    nilai2 = 0
                if granulity == 'rounding60u':
                    nilai2 = 1
                aa['set'] = nilai2
                aa['sisa'] = 0
        return aa
    
    def se_to_done(self):
        for otc in self:
            updatex = []
            for baris in otc.calculation_line:
                isian = []
                if baris.state == 'confirm':
                    isian.append(1)
                    isian.append(baris.id)
                    isian.append({'state' : 'done'})
                    baris.employee_ot.state = 'done'
                else:
                    isian.append(4)
                    isian.append(baris.id)
                    isian.append(False)
                updatex.append(isian)
            otc.calculation_line = updatex
            otc.state = 'done'

    def print_excel(self):
        granulity = self.overtime_granulity
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet = workbook.add_sheet(self.employee_id.name,cell_overwrite_ok=True)
        style0 = xlwt.easyxf('font: bold True, color black; align: horiz center;')
        style1 = xlwt.easyxf('font: bold True, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color lime; align: horiz center;')
        style2 = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;')
        style3 = xlwt.easyxf('font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;', "#,###")
        style4 = xlwt.easyxf('font: bold True, color black; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color lime; align: horiz center;', "#,###")
        namakolom = ['No','Date','Days','Type','Employee ID','Employee Name','Early OT','Afternoon OT','Calculation Time','Total Real Jam','Total Jam','Calculation OT','Rate Overtime','Nominal','Status','Note']
        lebarkolom = [4,15,15,15,15,30,7,7,7,7,5,5,5,5,5,5,5,5,5,5,5,15,15,15,15,15,15,15]
        worksheet.write_merge(0, 0, 0, 27,'Overtime Application List', style0)
        worksheet.write_merge(1, 1, 0, 27,'('+str(self.overtime_group.tanggal_awal)+' - '+str(self.overtime_group.tanggal_akhir)+')', style0)
        nn = 0
        for lebar in lebarkolom:
            worksheet.col(nn).width = 256 * lebar
            nn = nn + 1
        worksheet.write_merge(3, 4, 0, 0,namakolom[0], style1)
        worksheet.write_merge(3, 4, 1, 1,namakolom[1], style1)
        worksheet.write_merge(3, 4, 2, 2,namakolom[2], style1)
        worksheet.write_merge(3, 4, 3, 3,namakolom[3], style1)
        worksheet.write_merge(3, 4, 4, 4,namakolom[4], style1)
        worksheet.write_merge(3, 4, 5, 5,namakolom[5], style1)
        worksheet.write_merge(3, 3, 6, 7,namakolom[6], style1)
        worksheet.write_merge(3, 3, 8, 9,namakolom[7], style1)
        worksheet.write_merge(3, 3, 10, 20,namakolom[8], style1)
        worksheet.write_merge(3, 4, 21, 21,namakolom[9], style1)
        worksheet.write_merge(3, 4, 22, 22,namakolom[10], style1)
        worksheet.write_merge(3, 4, 23, 23,namakolom[11], style1)
        worksheet.write_merge(3, 4, 24, 24,namakolom[12], style1)
        worksheet.write_merge(3, 4, 25, 25,namakolom[13], style1)
        worksheet.write_merge(3, 4, 26, 26,namakolom[14], style1)
        worksheet.write_merge(3, 4, 27, 27,namakolom[15], style1)
        worksheet.write(4,6,'Start',style1)
        worksheet.write(4,7,'Finish',style1)
        worksheet.write(4,8,'Start',style1)
        worksheet.write(4,9,'Finish',style1)
        worksheet.write(4,10,'L1',style1)
        worksheet.write(4,11,'L2',style1)
        worksheet.write(4,12,'L3',style1)
        worksheet.write(4,13,'L4',style1)
        worksheet.write(4,14,'L5',style1)
        worksheet.write(4,15,'L6',style1)
        worksheet.write(4,16,'L7',style1)
        worksheet.write(4,17,'L8',style1)
        worksheet.write(4,18,'L9',style1)
        worksheet.write(4,19,'L10',style1)
        worksheet.write(4,20,'L11',style1)
        baris = 5
        no = 1
        rateot = 0
        kol22 = 0
        kol23 = 0
        kol25 = 0
        for linex in self.calculation_line:
            if linex.ot_total > 0:
                worksheet.write(baris,0,no,style2)
                worksheet.write(baris,1,linex.name,style2)
                worksheet.write(baris,2,linex.dayname,style2)
                worksheet.write(baris,3,linex.daystat,style2)
                worksheet.write(baris,4,'',style2)
                worksheet.write(baris,5,self.employee_id.name,style2)
                teks1 = self._convenrttotime(linex.ot1_in)
                teks2 = self._convenrttotime(linex.ot1_out)
                teks3 = self._convenrttotime(linex.ot2_in)
                teks4 = self._convenrttotime(linex.ot2_out)
                worksheet.write(baris,6,teks1,style2)
                worksheet.write(baris,7,teks2,style2)
                worksheet.write(baris,8,teks3,style2)
                worksheet.write(baris,9,teks4,style2)
                gettotal = linex.ot_total
                getX = self._setGetTime(gettotal,granulity)
                worksheet.write(baris,10,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,11,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,12,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,13,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,14,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,15,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,16,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,17,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,18,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,19,getX['set'],style2)
                getX = self._setGetTime(getX['sisa'],granulity)
                worksheet.write(baris,20,getX['set'],style2)
                relx = self._convenrttotime(linex.ot_total)
                worksheet.write(baris,21,relx,style2)
                worksheet.write(baris,22,linex.ot_total,style2)
                worksheet.write(baris,23,linex.ot_round,style2)
                kol22 = kol22 + linex.ot_total
                kol23 = kol23 + linex.ot_round
                
                gaji = 0
                datalines = self.employee_id.contract_id.attribut_lines
                for bb in datalines:
                    if bb.name.overtime_rate == True:
                        gaji = gaji + bb.nilai
                rateot = gaji / 173

                worksheet.write(baris,24,round(rateot,0),style3)
                worksheet.write(baris,25,round((rateot * linex.ot_round),0),style3)
                kol25 = kol25 + (rateot * linex.ot_round)
                worksheet.write(baris,26,linex.state,style2)
                if linex.notes == False:
                    worksheet.write(baris,27,'',style2)
                else:
                    worksheet.write(baris,27,linex.notes,style2)
                baris = baris + 1
                no = no + 1
        worksheet.write_merge(baris, baris, 0, 21,'TOTAL', style1)
        worksheet.write(baris,22,kol22,style1)
        worksheet.write(baris,23,kol23,style1)
        worksheet.write(baris,24,round(rateot,0),style4)
        worksheet.write(baris,25,round(kol25,0),style4)
        fp = BytesIO()
        workbook.save(fp)
        self.excel_file = base64.encodestring(fp.getvalue())
        fp.close()
        return {
            'type' : 'ir.actions.act_url',
            'url' : 'web/content/?model=lembur.overtime.calculation&field=excel_file&download=true&id=%s&filename=Overtime_Applcation_list.xls'%(self.id),
            'target' : 'self'
        }

class EnhancedOvertimePayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        for doc in self:
            super(EnhancedOvertimePayslip, doc).action_payslip_done()
            get_ot = doc.env['lembur.overtime.calculation'].search([('state','=','confirm'),('employee_id','=',doc.employee_id.id)])
            for ls in get_ot:
                ls.state = 'done'

    