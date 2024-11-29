from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EnhancedOvertimeWorkingHour(models.Model):
    _inherit = 'resource.calendar'

    # version 12
    typework = fields.Selection([
            ("5", '5 Hari Kerja dalam seminggu'),
            ("6", '6 Hari Kerja dalam seminggu'),
        ], string='Status', default='5')

class EnhancedOvertimeWorkingHourAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'
    isHalfday = fields.Boolean(string='Short Day')

class EnhancedEmployeeOvertime(models.Model):
    _name = 'employee.lembur.overtime'

    name = fields.Many2one('hr.employee', string='Employee')
    date_ot = fields.Date(string='Tanggal')
    ot1_in = fields.Float(string='OT1 In')
    ot1_out = fields.Float(string='OT1 Out')
    ot2_in = fields.Float(string='OT2 In')
    ot2_out = fields.Float(string='OT2 Out')
    state = fields.Selection([('confirm', 'Confirmed'),('done', 'Done')], string='Status')

class EenhancedOvertimeKoefisien(models.Model):
    _name = 'overtime.lembur.koefisien'

    name = fields.Selection([("workday","Workday"),("offday5","Offday (5)"),("holiday5","Holiday (5)"),("offday6","Offday (6)"),("holiday6","Public Holiday (6)"),("holiday61","Public Holiday (6) in Short Day")], string='Days Coefficient')
    jam1 = fields.Float(string='1 Jam')
    jam2 = fields.Float(string='2 Jam')
    jam3 = fields.Float(string='3 Jam')
    jam4 = fields.Float(string='4 Jam')
    jam5 = fields.Float(string='5 Jam')
    jam6 = fields.Float(string='6 Jam')
    jam7 = fields.Float(string='7 Jam')
    jam8 = fields.Float(string='8 Jam')
    jam9 = fields.Float(string='9 Jam')
    jam10 = fields.Float(string='10 Jam')
    jam11 = fields.Float(string='11 Jam')

class EnhancedOvertimeEmplyee(models.Model):
    _inherit = 'hr.employee'
    
    allow_overtime = fields.Boolean(string='Allow Overtime')