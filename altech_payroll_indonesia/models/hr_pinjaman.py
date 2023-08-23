from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging
_l = logging.getLogger(__name__)

class HrPinjaman(models.Model):
    _name = 'hr.pinjaman'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Pinjaman'
    _order = 'name'

    @api.depends('pinjaman_ids', 'pinjaman_ids.total', 'pinjaman_ids.state')
    def _compute_loan_calculation(self):
        """ Function generate total_pinjaman, sisa_pinjaman & tenor_pinjaman based on pinjaman_ids """
        for me in self:
            tot_pinj = 0
            sisa_pinj = 0
            if me.pinjaman_ids:
                for item in me.pinjaman_ids:
                    tot_pinj += item.total
                    if item.state == 'open':
                        sisa_pinj += item.total                                    

            me.total_pinjaman = tot_pinj
            me.sisa_pinjaman = sisa_pinj
            me.tenor_pinjaman = len(me.pinjaman_ids)
            
    name = fields.Char(string='Description',compute='set_nama_pinjaman', store=True,)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one('hr.department', string='Department')
    total_pinjaman = fields.Float(string='Total Pinjaman', compute='_compute_loan_calculation', store=True)
    sisa_pinjaman = fields.Float(string='Sisa Pinjaman', compute='_compute_loan_calculation', store=True)
    tenor_pinjaman = fields.Integer(string='Tenor Pinjaman', compute='_compute_loan_calculation', store=True)
    pinjaman_ids = fields.One2many('hr.pinjaman.line', 'pinjaman_id', string='List Tenor Pinjaman')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Done'),
    ], 'State', default='draft')
    active = fields.Boolean(default=True, help="The active field allows you to hide the overtime coefficient without removing it.")
    
    @api.depends('employee_id')
    def set_nama_pinjaman(self):
        txt1 = ""
        if self.employee_id.name != False:
            txt1 = self.employee_id.name
        self.name = "List Pinjaman " + str(txt1)

    def button_confirm(self):
        """ Move the Pinjaman from 'draft' to 'progress'. """
        for rec in self:
            rec.write({'state': 'progress'})
            # for item in rec.pinjaman_ids:
            #     item.write({'state': 'open'})

    def button_validate(self):
        """ Move the Pinjaman from 'progress' to 'done'. """
        for rec in self:
            rec.write({'state': 'done'})
            for item in rec.pinjaman_ids:
                if item.state == 'open':
                    raise ValidationError(_("Terdapat List tenor yang masih status open, cek kembali list tenor pinjaman"))
                item.write({'state': 'done'})

    def button_set_draft(self):
        """ Move the Pinjaman from 'progress' to 'draft'. """
        for rec in self:
            rec.write({'state': 'draft'})

    def button_import(self):
        """ function to import data """

    @api.constrains('pinjaman_ids')
    def _check_pinjaman_ids(self):
        # get cutoff id
        dataID = []
        cutoffName = []
        for baris in self.pinjaman_ids:
            if baris.cutoff_periode_id.id != False:
                dataID.append(baris.cutoff_periode_id.id)
                cutoffName.append(baris.cutoff_periode_id.name)
        sama = False
        teks = ""
        ke1 = 0
        for nn in dataID:
            ke2 = 0
            for mm in dataID:
                if ke1 != ke2:
                    if nn == mm:
                        sama = True
                        teks = cutoffName[ke2]
                ke2 = ke2 + 1
            ke1 = ke1 + 1
        if sama == True:
            raise ValidationError(_("Tenor Potongan " + str(teks) + " double"))

    @api.onchange('employee_id')
    def _set_default_department(self):
        if self.employee_id != False:
            self.department_id = self.employee_id.department_id.id
    
           
class HrPinjamanLine(models.Model):
    _name = 'hr.pinjaman.line'
    _description = 'List Tenor Pinjaman'

    pinjaman_id = fields.Many2one('hr.pinjaman', string='Pinjaman',ondelete="cascade")
    cutoff_periode_id = fields.Many2one('cutoff.periode', string='Tenor Potongan')
    total = fields.Float(string='Jumlah')
    state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done'),
    ], 'State', default='open')
    note = fields.Char(string='Note')
    
    def download_xlsx(self):
        ww = 4
        # data = self.search([],limit=1)
        # return self.env.ref('albisoft_hr_payroll_id.action_report_pinjaman_xlsx').report_action(data)
