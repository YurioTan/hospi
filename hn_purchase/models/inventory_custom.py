from odoo import api, fields, models


class KoliCustom(models.Model):
    _inherit = 'stock.picking'

    total_koli = fields.Float(string='Total Koli',compute='_get_total_koli',store=True)
    
    @api.depends('move_line_ids_without_package','move_line_ids_without_package.koli')
    def _get_total_koli(self):
        total=0.0
        for r in self:
            for line in r.move_line_ids_without_package:
                total+=line.koli
            r['total_koli']=total

class KoliEachCustom(models.Model):
    _inherit='stock.move.line'
    
    koli = fields.Float(string='Koli')

    
