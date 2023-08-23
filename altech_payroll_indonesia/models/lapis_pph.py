from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import uuid
import logging


class HrLapisPPH(models.Model):
    _name = 'hr.lapis.pph'
    _description = 'Tingkat Lapis PPH'
    _order = 'name'

    name = fields.Char(string='Tingkat Lapis PPH Name ')
    lapis = fields.Integer(string='Lapisan')
    amount_batas_bawah = fields.Float(string='Amount Batas Bawah')
    amount_batas_atas = fields.Float(string='Amount Batas Atas')
    percentage = fields.Float(string='Persentase')
    akumulasi = fields.Float(string='Akumulasi')
