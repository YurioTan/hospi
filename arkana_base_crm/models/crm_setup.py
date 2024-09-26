from odoo import api, fields, models

class Brand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"

    active = fields.Boolean(default=True)
    name = fields.Char("Brand", index=True)

class BudgetSource(models.Model):
    _name = "budget.source"
    _description = "Budget Source"

    active = fields.Boolean(default=True)
    name = fields.Char("Budget Source", index=True)
    
class Distributor(models.Model):
    _name = "distributor.distributor"
    _description = "Distributor"

    active = fields.Boolean(default=True)
    name = fields.Char("Distributor", index=True)
    