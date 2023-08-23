from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EnhancedLimitTunjnaganBPJS(models.Model):
    _name = 'hr.limit.bpjs.ks'
    _description = 'limit tunjangan bpjs kesehatan'

    name = fields.Char(string='Deskripsi')
    batas = fields.Integer(string='Batas')
    aktif = fields.Boolean(string='Aktif')

class EnhancedTabelJKK(models.Model):
    _name = 'hr.jkktabel'
    _description = 'settings jkk tabel'

    name = fields.Char(string='Tingkat risiko lingkungan kerja')
    persentase = fields.Float(string='Persentase')

class EnhancedTabelPTKP(models.Model):
    _name = 'hr.ptkp'
    _description = 'Konfigurasi PTKP'
    _order = 'sequence asc'
    name = fields.Char(string='Family Code')
    tax_reduction = fields.Float(string='Tax Reduction')
    sequence = fields.Integer(string='Sequence')

class EnhancedLimitTunjnaganPensiun(models.Model):
    _name = 'hr.limit.jp'
    _description = 'limit tunjangan pensiun'

    name = fields.Char(string='Deskripsi')
    batas = fields.Integer(string='Batas')
    usia = fields.Integer(string='Maksimum Usia')
    aktif = fields.Boolean(string='Aktif')

class EnhancedLimitBiayaJabatan(models.Model):
    _name = 'hr.limit.bijab'
    _description = 'limit biaya Jabatan'

    name = fields.Char(string='Deskripsi')
    batas = fields.Integer(string='Batas')
    batas_tahunan = fields.Integer(string='Batas Setahun')
    persen = fields.Float(string='Persentase dari Bruto')
    aktif = fields.Boolean(string='Aktif')