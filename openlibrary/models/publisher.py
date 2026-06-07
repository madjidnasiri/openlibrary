from odoo import models, fields, api

class Publishers(models.Model):
    _name = 'openlibrary.publisher'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'OpenLibrary: Publisher Information'

    name = fields.Char(string='Name', required=True, tracking=True)
    