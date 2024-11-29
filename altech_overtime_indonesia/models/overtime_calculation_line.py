from odoo import models, fields, api, _
from odoo.exceptions import UserError
import math
from datetime import datetime,timedelta

class EnhancedCalculationLine(models.Model):
    _name = 'lembur.overtime.calculation.line'

    name = fields.Date(string='Tanggal')
    dayname = fields.Selection([("0","Minggu"),("1","Senin"),("2","Selasa"),("3","Rabu"),("4","Kamis"),("5","Jumat"),("6","Sabtu")], string='Hari', compute='set_dayname')
    daystat = fields.Selection([("workday","Workday"),("offday5","Offday (5)"),("holiday5","Holiday (5)"),("offday6","Offday (6)"),("holiday6","Public Holiday (6)"),("holiday61","Public Holiday (6) in Short Day")], string='Jenis', compute='set_dayname', store=True)
    ot1_in = fields.Float(string='OT1 In')
    ot1_out = fields.Float(string='OT1 Out')
    ot2_in = fields.Float(string='OT2 In')
    ot2_out = fields.Float(string='OT2 Out')
    ot_total = fields.Float(string='OT Total', compute='get_ot_total')
    ot_round = fields.Float(string='OT Calculation', compute='get_ot_round')
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirmed'),('done', 'Done'),('invalid', 'Invalid')], string='Status', compute='set_dayname')
    calculation_id = fields.Many2one('lembur.overtime.calculation', string='Calculation Id')
    notes = fields.Char(string='Note')
    employee_ot = fields.Many2one('employee.lembur.overtime', string='Employee OT')
                
    @api.depends('name')
    def set_dayname(self):
        for doc in self:
            doc.get_ot_total()
            setdate = fields.Date.from_string(doc.name)
            if setdate is None:
                doc.dayname =  False
            else:
                doc.dayname =  setdate.strftime("%w")
            ####cek status#####
            get_state = doc._get_status_tgl(doc.name, doc.calculation_id.employee_id)
            doc.state = get_state['state']
            if get_state['eot'] != False:
                doc.employee_ot = get_state['eot']
                doc.ot1_in  = get_state['ot1_in']
                doc.ot1_out = get_state['ot1_out']
                doc.ot2_in  = get_state['ot2_in']
                doc.ot2_out = get_state['ot2_out']
            ####cek config#####
            doc.daystat = "workday"
            get_conf = self.env['ir.config_parameter'].sudo().get_param('aletch.basis_perhitungan')
            if get_conf == 'wt':
                doc.daystat = doc._get_stat_by_wt(setdate, doc.calculation_id.employee_id, doc.dayname)
                
    def _get_stat_by_wt(self, tgl, emplpoyee, dayname):
        statushari = False
        if tgl is not None:
            dif_utc_local = datetime.now() - datetime.utcnow()
            selsih_jam = dif_utc_local.seconds / 60 / 60
            date_time_start  = datetime.strptime(tgl.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
            d1 = date_time_start - timedelta(hours=selsih_jam)
            res_cal = emplpoyee.resource_calendar_id
            get_ph = res_cal.global_leave_ids.filtered(lambda x: x.date_from <= d1 and x.date_to >= d1)
            get_schedule = res_cal.attendance_ids.filtered(lambda x: x.dayofweek == dayname)
            if len(get_ph) > 0:
                if len(get_schedule) > 0:
                    if res_cal.typework == "5":
                        statushari = 'holiday5'
                    if res_cal.typework == "6":
                        if get_schedule[0].isHalfday == True:
                            statushari = 'holiday61'
                        else:
                            statushari = 'holiday6'
                else:
                    if res_cal.typework == "5":
                        statushari = 'holiday5'
                    if res_cal.typework == "6":
                        statushari = 'holiday6'
            else:
                if len(get_schedule) > 0:
                    statushari = 'workday'
                else:
                    if res_cal.typework == "5":
                        statushari = 'offday5'
                    if res_cal.typework == "6":
                        statushari = 'offday6'
        return statushari

    def _get_status_tgl(self, tgl, employee):
        output = {}
        state = 'draft'
        eot = False
        if tgl != False:
            cari = self.env['employee.lembur.overtime'].search(['&',('date_ot','=',tgl),('name','=',employee.id)])
            if len(cari) > 0:
                state = cari[0].state
                eot = cari[0].id
                output['ot1_in']    = cari[0].ot1_in
                output['ot1_out']   = cari[0].ot1_out
                output['ot2_in']    = cari[0].ot2_in
                output['ot2_out']   = cari[0].ot2_out
        output['state']  = state
        output['eot']  = eot
        return output
    
    @api.depends('daystat','ot1_in','ot1_out','ot2_in','ot2_out')
    def get_ot_total(self):
        for doc in self:
            jam1 = 0
            jam2 = 0
            if doc.ot1_in != 0 and doc.ot1_out != 0:
                jam1 = doc.ot1_out - doc.ot1_in
                if jam1 <= 0:
                    raise UserError('Invalid OT1')
            if doc.ot2_in != 0 and doc.ot2_out != 0:
                temp1 = doc.ot2_out
                if doc.ot2_out < doc.ot2_in:
                    temp1 = doc.ot2_out + 24
                jam2 = temp1 - doc.ot2_in
            granulity = doc.calculation_id.overtime_granulity
            total1 = jam2 + jam1
            if granulity == 'prorate':
                doc.ot_total = total1
            if granulity == 'rounding30d':
                sisa = total1 - math.floor(total1)
                if sisa < 0.5:
                    sisa = 0
                else:
                    sisa = 0.5
                total2 = math.floor(total1) + sisa
                doc.ot_total = total2
            if granulity == 'rounding30u':
                sisa = total1 - math.floor(total1)
                if sisa <= 0.5:
                    sisa = 0.5
                else:
                    sisa = 1
                total2 = math.floor(total1) + sisa
                doc.ot_total = total2
            if granulity == 'rounding60d':
                total2 = math.floor(total1)
                doc.ot_total = total2
            if granulity == 'rounding60u':
                sisa = total1 - math.floor(total1)
                if sisa > 0:
                    sisa = 1
                total2 = math.floor(total1) + sisa
                doc.ot_total = total2
            

    @api.depends('ot_total')
    def get_ot_round(self):
        for doc in self:
            koefisien = self.env['overtime.lembur.koefisien'].search([('name','=',doc.daystat)])
            angka = math.ceil(doc.ot_total)
            nilaitotal = 0
            if angka > 0:
                naik = range(angka)
                for xx in naik:
                    sisa = doc.ot_total - xx
                    if sisa < 1:
                        if xx == 0:
                            nilaitotal = nilaitotal + (koefisien.jam1 * sisa)
                        if xx == 1:
                            nilaitotal = nilaitotal + (koefisien.jam2 * sisa)
                        if xx == 2:
                            nilaitotal = nilaitotal + (koefisien.jam3 * sisa)
                        if xx == 3:
                            nilaitotal = nilaitotal + (koefisien.jam4 * sisa)
                        if xx == 4:
                            nilaitotal = nilaitotal + (koefisien.jam5 * sisa)
                        if xx == 5:
                            nilaitotal = nilaitotal + (koefisien.jam6 * sisa)
                        if xx == 6:
                            nilaitotal = nilaitotal + (koefisien.jam7 * sisa)
                        if xx == 7:
                            nilaitotal = nilaitotal + (koefisien.jam8 * sisa)
                        if xx == 8:
                            nilaitotal = nilaitotal + (koefisien.jam9 * sisa)
                        if xx == 9:
                            nilaitotal = nilaitotal + (koefisien.jam10 * sisa)
                        if xx == 10:
                            nilaitotal = nilaitotal + (koefisien.jam11 * sisa)
                        if xx > 10:
                            nilaitotal = nilaitotal + (koefisien.jam11 * sisa)
                    else:
                        if xx == 0:
                            nilaitotal = nilaitotal + koefisien.jam1
                        if xx == 1:
                            nilaitotal = nilaitotal + koefisien.jam2
                        if xx == 2:
                            nilaitotal = nilaitotal + koefisien.jam3
                        if xx == 3:
                            nilaitotal = nilaitotal + koefisien.jam4
                        if xx == 4:
                            nilaitotal = nilaitotal + koefisien.jam5
                        if xx == 5:
                            nilaitotal = nilaitotal + koefisien.jam6
                        if xx == 6:
                            nilaitotal = nilaitotal + koefisien.jam7
                        if xx == 7:
                            nilaitotal = nilaitotal + koefisien.jam8
                        if xx == 8:
                            nilaitotal = nilaitotal + koefisien.jam9
                        if xx == 9:
                            nilaitotal = nilaitotal + koefisien.jam10
                        if xx == 10:
                            nilaitotal = nilaitotal + koefisien.jam11
                        if xx > 10:
                            nilaitotal = nilaitotal + koefisien.jam11
                    
            doc.ot_round = nilaitotal