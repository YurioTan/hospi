# -*- coding: utf-8 -*-
from odoo import api, fields, models, modules


class AltechResConfigOvertime(models.TransientModel):
    _inherit = 'res.config.settings'

    overtime_granulity = fields.Selection([("rounding60d","60 menit Down"),("rounding30d","30 menit Down"),
                                           ("prorate","Prorate"),
                                           ("rounding30u","30 menit UP"),("rounding60u","60 menit UP")], string='Granulity')
    basis_perhitungan = fields.Selection([("manual","Manual"),("wt","Working Times")], string='Resources')
    overtime_pembagi = fields.Integer(string='Nilai Pembagi')

    @api.model
    def get_values(self):
        res = super(AltechResConfigOvertime, self).get_values()
        res.update(
            overtime_granulity = self.env['ir.config_parameter'].sudo().get_param('aletch.overtime_granulity')   
        )
        res.update(
            basis_perhitungan = self.env['ir.config_parameter'].sudo().get_param('aletch.basis_perhitungan')
        )
        res.update(
            overtime_pembagi = self.env['ir.config_parameter'].sudo().get_param('aletch.overtime_pembagi')
        )
        return res

    def set_values(self):
        super(AltechResConfigOvertime, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        set_keys = self.overtime_granulity or False
        set_basis = self.basis_perhitungan or False
        set_pembagi = self.overtime_pembagi or False
        
        param.set_param('aletch.overtime_granulity', set_keys)
        param.set_param('aletch.basis_perhitungan', set_basis)
        param.set_param('aletch.overtime_pembagi', set_pembagi)
