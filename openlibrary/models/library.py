from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Library(models.Model):
    _name = 'openlibrary.library'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'OpenLibrary: Library Information '
    _check_company_auto = True

    name = fields.Char(string='Name', required=True, tracking=True)
    address = fields.Char(string='Address')
    owner = fields.Char(string='Owner')
    responsible_user_id = fields.Many2one(comodel_name='res.users', string='User', ondelete='set null')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    repository_ids = fields.One2many(comodel_name='openlibrary.repository', inverse_name='library_id', string='Repository')

    membership_ids = fields.One2many(comodel_name='openlibrary.membership', inverse_name='library_id', string='Subscriber Memberships')
    subscriber_ids = fields.Many2many(comodel_name='openlibrary.subscriber', string='Subscribers', compute='_compute_subscriber_ids', store=True)

    @api.constrains('name', 'company_id')
    def _check_library_name(self):
        for record in self:
            # 1. بررسی خالی نبودن
            if not record.name or not record.name.strip():
                raise ValidationError('Library name cannot be empty!')
            
            # 2. بررسی یکتایی
            existing = self.search([
                ('name', '=ilike', record.name.strip()),
                ('company_id', '=', record.company_id.id),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(f'Library "{record.name}" already exists in this company!')

