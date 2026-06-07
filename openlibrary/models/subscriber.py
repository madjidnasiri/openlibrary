from odoo import _, api, fields, models
from datetime import date
from dateutil.relativedelta import *
from odoo.exceptions import ValidationError

class Subscriber(models.Model):
    _name = 'openlibrary.subscriber'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'OpenLibrary: Subscriber'

    name = fields.Char(string='Name', required=True, tracking=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contact')
    birthday = fields.Date(string='Birthday', required=True, default=lambda self: date.today() - relativedelta(years=7))
    active = fields.Boolean(string='Active', default=True)
    age = fields.Integer(string='age', compute='_compute_age', )
    note = fields.Text(string='Node', tracking=True, )
    acceptable_day = fields.Integer(string='Acceptable number of days', default=10)
    membership_ids = fields.One2many('openlibrary.membership', 'subscriber_id', string='Library Memberships')
    library_ids = fields.Many2many('openlibrary.library', string='Libraries', compute='_compute_library_ids', store=True)
    lent_book_ids = fields.One2many(comodel_name='openlibrary.lend', inverse_name='subscriber_id', string='Lent Books')
    
    
    @api.depends('membership_ids.library_id')
    def _compute_library_ids(self):
        for record in self:
            record.library_ids = record.membership_ids.mapped('library_id')

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birthday:
                born = record.birthday
                record.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                record.age = 0


    @api.constrains("birthday")
    def _check_age(self):
        for record in self:
            if record.age:
                if record.age < 7:
                    raise ValidationError(_('Subscriber cann''t has small of 7 old year'))
            else:
                raise ValidationError(_('Subscriber''s birthday don''t enter'))
