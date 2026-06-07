from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BookEdition(models.Model):
    _name = 'openlibrary.bookedition'
    _description = 'OpenLibrary: Book edition'

    #name = fields.Char(string='Name', onchange='_change_name', readonly=True)
    name = fields.Char(string='Name', compute='_compute_name', )
    description = fields.Text(string='Description')
    book_id = fields.Many2one(comodel_name='openlibrary.book', string='Book')
    publisher_id = fields.Many2one(comodel_name='openlibrary.publisher', string='Publisher')
    publisher_name = fields.Char(string='Publisher Name', related='publisher_id.name', )
    edition = fields.Integer(string='Edition')
    publish_date = fields.Date(string='Publish Date')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    price = fields.Monetary(string='Price')

    @api.depends('book_id', 'publisher_id', 'edition', 'publish_date')
    def _compute_name(self):
        for record in self:
            rec_name = ''
            if record.book_id:
                rec_name += record.book_id.display_name + ' -> '
            if record.edition:
                rec_name += str(record.edition) + ' - '
            if record.publisher_id:
                rec_name += record.publisher_id.display_name + ' - '
            if record.publish_date:
                rec_name += str(record.publish_date.year) + ' - '

            if rec_name.endswith(' -> '):
                rec_name = rec_name[:-4]
            elif rec_name.endswith(' - '):
                rec_name = rec_name[:-3]

            record.name = rec_name
