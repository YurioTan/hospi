from odoo import models, fields, api

class PayrollInputExtrasInsentifLineCategory(models.Model):
    _name = 'hr.payroll.extras.insentif.category'
    _description = 'Payroll Extras Insentif Category'

    name = fields.Char(string='Income Adjustment Category')
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active',default=True)

class PayrollInputExtrasInsentifLine(models.Model):
    _name = 'hr.payroll.extras.insentif.line'
    _description = 'Payroll Extras Insentif Line'

    name = fields.Many2one('hr.employee', string='Employee')
    insentif = fields.Integer(string='Besaran Insentif')
    insentif_id = fields.Many2one('hr.payroll.extras.insentif', string='Insentif Id')

class PayrollInputExtrasInsentif(models.Model):
    _name = 'hr.payroll.extras.insentif'
    _description = 'Payroll Extras Insentif'

    name = fields.Char(string='Description')
    category_id = fields.Many2one('hr.payroll.extras.insentif.category', string='Category')
    state = fields.Selection([("draft","Draft"),("confirm","Confirm"),("done","Done")], string='Status', default="draft")
    cutoff_periode_id = fields.Many2one('cutoff.periode', string='Cutoff Periode')
    # start_date = fields.Date(string='Start Date')
    # end_date = fields.Date(string='End Date')
    insentif_line = fields.One2many('hr.payroll.extras.insentif.line', 'insentif_id', string='List Insentif')

    def confirm_insentif(self):
        for doc in self:
            doc.state = 'confirm'
    
    def draft_insentif(self):
        for doc in self:
            doc.state = 'draft'

    def done_insentif(self):
        for doc in self:
            doc.state = 'done'
class PayrollInputExtrasAdjDeductionCategory(models.Model):
    _name = 'hr.payroll.extras.deduction.adjustment.category'
    _description = 'Payroll Extras Insentif Category'

    name = fields.Char(string='Deduction Adjustment Category')
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active',default=True)


class PayrollInputExtrasAdjustmentDeductionLine(models.Model):
    _name = 'hr.payroll.extras.deduction.adjustment.line'
    _description = 'Payroll Extras Adjustment Line'

    name = fields.Many2one('hr.employee', string='Employee')
    nilai = fields.Integer(string='Besaran Adjustment')
    deduction_adj_id = fields.Many2one('hr.payroll.extras.deduction.adjustment', string='Adjustment Deduction Id')

class PayrollInputExtrasAdjustmentDeduction(models.Model):
    _name = 'hr.payroll.extras.deduction.adjustment'
    _description = 'Payroll Extras Adjustment'

    name = fields.Char(string='Description')
    cutoff_periode_id = fields.Many2one('cutoff.periode', string='Cutoff Periode')
    category_id = fields.Many2one('hr.payroll.extras.deduction.adjustment.category', string='Category')
    state = fields.Selection([("draft","Draft"),("confirm","Confirm"),("done","Done")], string='Status', default="draft")
    # start_date = fields.Date(string='Start Date')
    # end_date = fields.Date(string='End Date')
    line_ids = fields.One2many('hr.payroll.extras.deduction.adjustment.line', 'deduction_adj_id', string='List Adjustment Deduction')

    def confirm_insentif(self):
        for doc in self:
            doc.state = 'confirm'
    
    def draft_insentif(self):
        for doc in self:
            doc.state = 'draft'

    def done_insentif(self):
        for doc in self:
            doc.state = 'done'

class PayrollInputExtrasPotonganRutinLine(models.Model):
    _name = 'hr.payroll.extras.potongangrutin.line'
    _description = 'Payroll Extras Potongan Rutin Line'

    name = fields.Many2one('hr.employee', string='Employee')
    nilai = fields.Integer(string='Nilai Potongan')
    potongan_id = fields.Many2one('hr.payroll.extras.potongangrutin', string='Potongan Id')

class PayrollInputExtrasPotonganRutin(models.Model):
    _name = 'hr.payroll.extras.potongangrutin'
    _description = 'Payroll Extras Potongan Rutin'

    name = fields.Char(string='Description')
    state = fields.Selection([("draft","Draft"),("confirm","Confirm"),("done","Done")], string='Status', default="draft")
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    line_ids = fields.One2many('hr.payroll.extras.potongangrutin.line', 'potongan_id', string='List Potongan Rutin')

    def confirm_insentif(self):
        for doc in self:
            doc.state = 'confirm'
    
    def draft_insentif(self):
        for doc in self:
            doc.state = 'draft'

    def done_insentif(self):
        for doc in self:
            doc.state = 'done'
