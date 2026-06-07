from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class BookRepository(models.Model):
    _name = 'openlibrary.book_repository'
    _description = 'OpenLibrary: Book in Repository'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = 'name'
    _check_company_auto = True

    book_edition_id = fields.Many2one(comodel_name='openlibrary.bookedition', string='Book Edition')
    repository_id = fields.Many2one(comodel_name='openlibrary.repository', string='Repository')
    library_id = fields.Many2one(comodel_name='openlibrary.library', string='Library', related='repository_id.library_id', store=True, readonly=True)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    purchase_price = fields.Monetary(string='Price', currency_field='currency_id')
    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True, )
    code = fields.Char(string='Code', required=True, copy=False, readonly=True, default='New')
    repository_type = fields.Selection(string='Repository Type', related='repository_id.type', readonly=True )
    lend_ids = fields.One2many(comodel_name='openlibrary.lend', inverse_name='book_repo_id', string='Lending History')
    is_lent = fields.Boolean(string='Is lent', compute='_compute_is_lent', store=True)
    current_lend_id = fields.Many2one('openlibrary.lend', string='Current Lend', compute='_compute_is_lent', store=True)

    status = fields.Selection(string='Status', selection=[
        ('free', '📘 Free'),
        ('lent', '📗 Lent'),
        ('delay', '📙 Delay'),
        ('suspicious', '📕 Suspicious Delay'),
        ('dangerous', '📓 Dangerous Delay'),]
        , compute="_compute_status", store=True, default='free',)


    book_id = fields.Many2one('openlibrary.book', string='Book', compute='_compute_book_id', store=True, readonly=True )
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='repository_id.company_id', required=True)
    
    @api.depends('book_edition_id', 'book_edition_id.book_id')
    def _compute_book_id(self):
        for record in self:
            record.book_id = record.book_edition_id.book_id.id if record.book_edition_id else False

    @api.depends('current_lend_id', 'current_lend_id.days_late')
    def _compute_status(self):
        for record in self:
            if record.current_lend_id:
                record.status = record.current_lend_id.status
            else:
                record.status = 'free'

    @api.model
    def create(self, vals):
        vals[0]['code'] = self.env['ir.sequence'].next_by_code('openlibrary.book_repository.code') or 'New'
        vals[0]['status'] = 'free'
        return super(BookRepository, self).create(vals)

    @api.depends('lend_ids', 'lend_ids.return_date')
    def _compute_is_lent(self):
        # محاسبه وضعیت امانت بودن کتاب
        for book in self:
            # پیدا کردن امانت فعال (بدون تاریخ برگشت)
            active_lend = self.env['openlibrary.lend'].search([('book_repo_id', '=', book.id),('return_date', '=', False)], limit=1)
            
            if active_lend:
                book.is_lent = True
                book.current_lend_id = active_lend.id
            else:
                book.is_lent = False
                book.current_lend_id = False

    @api.depends('book_edition_id')
    def _compute_name(self):
        for record in self:
            if record and record.book_edition_id and record.book_edition_id.book_id and record.code:
                dn = record.code + ' | ' + record.book_edition_id.book_id.title + ' - '
                for a in record.book_edition_id.book_id.author_ids:
                    dn += a.name + ' , '
                if dn.endswith(' , '):
                    dn = dn[:-3]
                record.name = dn
            else:
                record.name = False

    def repeat_this_book(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Multi Book from ...'),
            'res_model': 'openlibrary.wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [[self.env.ref('openlibrary.book_repository_repeat_form').id, 'form']],
            'context': {
                'default_number':1,
                'default_book_edition_id': self.book_edition_id.id,
                'default_repository_id': self.repository_id.id,
                'default_purchase_price': self.purchase_price,
                },
        }

    def button_lending_this_book(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lending Book ...'),
            'res_model': 'openlibrary.lend_wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [[self.env.ref('openlibrary.book_lending_wizard_form').id, 'form']],
            'context': {
                'default_library_id': self.repository_id.library_id.id,
                'default_book_repo_id': self.id,
                'return_model': self._name,
                'return_id': self.id,
            },
        }

    def button_return_book(self):
        self.ensure_one()

        if not self.is_lent:
            raise UserError(_('This book is not currently lent!'))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Return Book'),
            'res_model': 'openlibrary.return_book_wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [[self.env.ref('openlibrary.view_openlibrary_return_book_wizard_form').id, 'form']],
            'context': {
                'default_lend_id': self.current_lend_id.id,
                'default_book_repo_id': self.id,
                'default_subscriber_id':self.current_lend_id.subscriber_id.id,
                'default_start_date': self.current_lend_id.start_date,
                'default_due_date': self.current_lend_id.due_date,
                'return_model': self._name,
                'return_id': self.id,
            }
        }