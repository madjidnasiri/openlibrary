
from odoo import _, api, fields, models


class tag(models.Model):
    _name = 'openlibrary.tag'
    _description = 'Tag for books and authors'

    name = fields.Char(string='Name')
