from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from datetime import date

class Lend(models.Model):
    _name = 'openlibrary.lend'
    _description = 'Open Library: Lending'
    _inherit = ['mail.thread','mail.activity.mixin']

    subscriber_id = fields.Many2one(comodel_name='openlibrary.subscriber', string='Subscriber', required=True, ondelete="restrict", domain="[('membership_ids.library_id', '=', library_id), ('membership_ids.status', 'in', ['active']),  ('membership_ids', 'not any', [('status', 'not in', ['active'])]) ]")
    book_repo_id = fields.Many2one(comodel_name='openlibrary.book_repository', string='Book Edition/Repository', required=True, ondelete="restrict", domain="[('repository_id.library_id', '=', library_id)]" )
    library_id = fields.Many2one(comodel_name='openlibrary.library', string='Library', related='book_repo_id.repository_id.library_id', store=False, readonly=True)
    repository_id = fields.Many2one(comodel_name='openlibrary.repository', string='Repository', related='book_repo_id.repository_id', store=False, readonly=True)
    book_id = fields.Many2one(comodel_name='openlibrary.book', string='Book', related='book_repo_id.book_edition_id.book_id', store=False, readonly=True)
    subscriber_due_day = fields.Integer(string='Allowed Days', related='subscriber_id.acceptable_day', readonly=True)
    start_date = fields.Date(string='Start Date', required=True,)
    due_date = fields.Date(string='Due Date', compute="_compute_due_date", store=True,)
    return_date = fields.Date(string='Return Date')
    days_late = fields.Integer(string='Delay', compute="_compute_days_late", store=True,)
    last_delay_update = fields.Date(string='Last Delay Update', default=fields.Date.today)
    status = fields.Selection(string='Status', selection=[
        ('free', '📘 Free'),
        ('lent', '📗 Lent'),
        ('delay', '📙 Delay'),
        ('suspicious', '📕 Suspicious Delay'),
        ('dangerous', '📓 Dangerous Delay'),]
        , compute="_compute_status", store=True, default='free',)
    status_sequence = fields.Selection(
            string='Status Sequence',
            selection=[
                ('50', '📘 Free'),
                ('40', '📗 Lent'),
                ('30', '📙 Delay'),
                ('20', '📕 Suspicious Delay'),
                ('10', '📓 Dangerous Delay'),],
            compute="_compute_status",
            store=True,
            help="Numerical order for kanban grouping"
        )
        
    def action_recompute_status(self):
        for record in self:
            # علامت گذاری فیلدهای وابسته
            record.modified(['start_date', 'subscriber_due_day', 'due_date', 'return_date', 'last_delay_update'])
            
            # محاسبه مجدد مستقیم
            record._compute_display_name()
            record._compute_due_date()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Fields recalculated successfully.'),
                'type': 'success',
                'sticky': False,
            }
        }

    @api.depends('days_late', 'return_date')
    def _compute_status(self):
        config = self.env['ir.config_parameter'].sudo()
        warning_days = int(config.get_param('openlibrary.delay_warning_threshold', default='3'))
        suspicious_days = int(config.get_param('openlibrary.delay_suspicious_threshold', default='30'))        
        for record in self:
            if record.return_date:
                record.status = 'free'
                record.status_sequence = '50'
            elif (not record.days_late):
                record.status = 'lent'
                record.status_sequence = '40'
            else:
                if record.days_late == 0:
                    record.status = 'lent'
                    record.status_sequence = '40'
                elif record.days_late <= warning_days:
                    record.status = 'delay'
                    record.status_sequence = '30'
                elif record.days_late <= suspicious_days:
                    record.status = 'suspicious'
                    record.status_sequence = '20'
                else:
                    record.status = 'dangerous'
                    record.status_sequence = '10'


    @api.depends('due_date')
    def _compute_days_late(self):
        for record in self:
            if record.due_date and record.last_delay_update:
                record.days_late = max((record.last_delay_update-record.due_date).days, 0)
            else:
                record.days_late = 0

    @api.depends('start_date','subscriber_due_day')
    def _compute_due_date(self):
        for record in self:
            if record.start_date and record.subscriber_due_day:
                record.due_date = record.start_date + timedelta(days=record.subscriber_due_day)
            else:
                record.due_date = False
    
    @api.model
    def cron_update_delay_days(self):
        today = fields.Date.today()
        
        # پیدا کردن همه امانت‌هایی که:
        # 1. هنوز بازگشت داده نشده‌اند
        # 2. تاریخ سررسید آنها گذشته است
        # 3. آخرین به‌روزرسانی آنها دیروز یا قبل‌تر بوده
        overdue_lends = self.search([
            ('return_date', '=', False),
            ('due_date', '<', today),
            '|',
                ('last_delay_update', '=', False),
                ('last_delay_update', '<', today)
        ])
        
        for lend in overdue_lends:
            # محاسبه مجدد تاخیر
            lend.last_delay_update = today
            lend._compute_due_date()
            
        # به‌روزرسانی امانت‌هایی که امروز بازگشت داده شده‌اند
        returned_today = self.search([
            ('return_date', '=', today)
        ])
        for lend in returned_today:
            lend._compute_days_late()
        
        return True

    @api.depends('book_repo_id.name', 'subscriber_id.name')
    def _compute_display_name(self):
        for record in self:
            name_parts = []
            
            if record.book_repo_id and record.book_repo_id.name:
                name_parts.append(record.book_repo_id.name)
            
            if record.subscriber_id and record.subscriber_id.name:
                name_parts.append(f"[{record.subscriber_id.name}]")
            
            record.display_name = ' '.join(name_parts) if name_parts else record.name or 'Unknown'        

    def button_return_book(self):
        self.ensure_one()

        if self.status == 'free':
            raise UserError(_('This book is not currently lent!'))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Return Book'),
            'res_model': 'openlibrary.return_book_wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [[self.env.ref('openlibrary.view_openlibrary_return_book_wizard_form').id, 'form']],
            'context': {
                'default_lend_id': self.id,
                'default_book_repo_id': self.book_repo_id.id,
                'default_subscriber_id':self.subscriber_id.id,
                'default_start_date': self.start_date,
                'default_due_date': self.due_date,
                'return_model': self._name,
                'return_id': self.id,
            }
        }