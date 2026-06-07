from odoo import models, fields, api

class Books(models.Model):
    _name = "openlibrary.book"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "OpenLibrary: Book Information and Summury"
    _rec_name = 'title'
    _order = 'title'

    title = fields.Char(string='Title',required=True, tracking=True)
    subtitle = fields.Char(string='Sub Title',)
    summary = fields.Html(string='Summary',)
    book_edition_ids = fields.One2many(comodel_name='openlibrary.bookedition', inverse_name='book_id', string='Book Prints')
    author_ids = fields.Many2many(comodel_name='openlibrary.author', string='Authors')
    tag_ids = fields.Many2many(comodel_name='openlibrary.tag', string='Tags')
    