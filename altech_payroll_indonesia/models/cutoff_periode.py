from odoo import api, fields, models, _
from datetime import date, datetime

import logging
_l = logging.getLogger(__name__)

class CutoffPeriode(models.Model):
    _name = 'cutoff.periode'
    _description = 'Cutoff Periode'
    _order = 'sequence'

    @api.depends('date_start', 'date_end')
    def set_default_name(self):
        txt1 = ""
        txt2 = ""
        if self.date_start != False:
            txt1 = self.date_start.__format__('%d %B %Y')
        if self.date_end != False:
            txt2 = self.date_end.__format__('%d %B %Y')
        self.name = "Cutoff Periode " + str(txt1) + " s/d " + str(txt2)

    name = fields.Char(string='Name', compute='set_default_name', store=True,)
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    tax_year = fields.Integer(string='Tahun Pajak')
    is_visible = fields.Boolean(string='Visible', default=True)
    sequence = fields.Integer(string='Sequence')
    tax_period_month = fields.Selection([
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
        ('12','12')], string='Masa Pajak')
    active = fields.Boolean(default=True, help="The active field allows you to hide the overtime coefficient without removing it.")
