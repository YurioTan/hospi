from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritSalaryRuleKomponenGaji(models.Model):
    _inherit = 'hr.salary.rule'

    _order = "sequence asc"
    
    report_mode = fields.Selection([("income","Income"),("deduction","Deduction"),("comp","Company Contribution")], string='Report Category')
    show_in_excel_list = fields.Boolean(string='Show Report Excel')

    bpjs_report_type = fields.Selection([("basis","Basis BPJS"),("company","Company Contribution"),("employee","Employee")], string='BPJS Kes. Report')
    bpjstk_report_type = fields.Selection([("basis","Basis BPJS"),("company","Company Contribution"),("employee","Employee")], string='BPJS TK. Report')

    pph1721_report = fields.Selection([("kolom1","Kolom 1"),("kolom2","Kolom 2"),("kolom3","Kolom 3"),
                                       ("kolom4","Kolom 4"),("kolom5","Kolom 5"),("kolom6","Kolom 6"),
                                       ("kolom7","Kolom 7"),("kolom8","Kolom 8"),("kolom9","Kolom 9"),
                                       ("kolom10","Kolom 10"),("kolom11","Kolom 11"),("kolom12","Kolom 12"),
                                       ("kolom13","Kolom 13"),("kolom14","Kolom 14"),("kolom15","Kolom 15"),
                                       ("kolom16","Kolom 16"),("kolom17","Kolom 17"),("kolom18","Kolom 18"),
                                       ("kolom19","Kolom 19"),("kolom20","Kolom 20")], string='Kolom')