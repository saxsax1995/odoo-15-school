from odoo import models, fields

# inherit model "sale.order"
class SaleOrder(models.Model):
    # the value is the model you want to inherit
    # get by click on debug mode view form
    # when you inherit other modules, you must add it in depends in __manifest__.py
    _inherit = "sale.order"

    # create new column to table "sale_order" in database
    custom_field = fields.Char(string='Custom Field')

# inherit model "res.partner"
class ResPartner(models.Model):
    # the value is the model you want to inherit
    # get by click on debug mode view form
    # when you inherit other modules, you must add it in depends in __manifest__.py
    _inherit = "res.partner"

    # add new option to select field
    company_type = fields.Selection(selection_add=[('student', 'Student')], default=None)