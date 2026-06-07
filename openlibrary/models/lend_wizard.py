from odoo import models, fields, api, _

class lend_book_wizard(models.TransientModel):
    _name = 'openlibrary.lend_wizard'
    _description = 'OpenLibrary: Lend Wizard'

    library_id = fields.Many2one(string="Library", comodel_name="openlibrary.library", ondelete="set null", store=False)
    book_repo_id = fields.Many2one(string="Book", comodel_name="openlibrary.book_repository", ondelete="set null", store=False)
    subscriber_id = fields.Many2one(comodel_name='openlibrary.subscriber', string='Subscriber', required=True, ondelete="restrict", domain="[('membership_ids.library_id', '=', library_id), ('membership_ids.status', 'in', ['active']),  ('membership_ids', 'not any', [('status', 'not in', ['active'])])]")
    lend_date = fields.Date(string='Lending Date', default=fields.Date.today, required=True,)

    def lending_book(self):
        lend = self.env['openlibrary.lend'].sudo().create(
            {
                'subscriber_id': self.subscriber_id.id,
                'book_repo_id': self.book_repo_id.id,
                'start_date': self.lend_date,
            }
        )

        return_view_mode = self.env.context.get('return_source', 'form')
        return_model = self.env.context.get('return_model', 'openlibrary.book_repository')
        return_id = self.env.context.get('return_id')
    
        # بازگشت به نمای مناسب
        if return_view_mode == 'list':
            # برگشت به نمای لیست
            return {
                'type': 'ir.actions.act_window',
                'res_model': return_model,
                'view_mode': 'list,form',
                'target': 'current',
            }
        else:
            # برگشت به نمای فرم
            return {
                    'type': 'ir.actions.act_window_close',
                    'context': {'reload_parent': True},  # درخواست رفرش
            }

class return_book_wizard(models.TransientModel):
    _name = 'openlibrary.return_book_wizard'
    _description = 'OpenLibrary: Return Book Wizard'

    lend_id = fields.Many2one('openlibrary.lend', string='Lend Record', readonly=True, required=True)
    book_repo_id = fields.Many2one(comodel_name='openlibrary.book_repository', string='Book', related='lend_id.book_repo_id', store=False, readonly=True)
    subscriber_id = fields.Many2one(comodel_name='openlibrary.subscriber', string="Subscriber", related="lend_id.subscriber_id", store=False, readonly=True)
    return_date = fields.Date(string='Return Date', default=fields.Date.today, required=True)
    days_late = fields.Integer(string='Delay Days', compute='_compute_days_late', readonly=True)
    library_id = fields.Many2one(comodel_name='openlibrary.library', string='Library', related="book_repo_id.library_id", store=False, readonly=True)
    subscriber_due_day = fields.Integer(comodel_name='openlibrary.subscriber', string='Subscriber Due Day', related="subscriber_id.acceptable_day", store=False, readonly=True)
    start_date = fields.Date(comodel_name='openlibrary.lend', string='Lend Date', related="lend_id.start_date", store=False, readonly=True)
    due_date = fields.Date(comodel_name='openlibrary.lend', string='Due Date', related="lend_id.due_date", store=False, readonly=True)
    book_status = fields.Selection(string='Book Status', related='book_repo_id.status', readonly=True)
    
    @api.depends('return_date', 'lend_id')
    def _compute_days_late(self):
        for record in self:
            if record.lend_id and record.return_date and record.lend_id.due_date:
                if record.return_date > record.lend_id.due_date:
                    record.days_late = (record.return_date - record.lend_id.due_date).days
                else:
                    record.days_late = 0
            else:
                record.days_late = 0

    def return_book(self):
        self.ensure_one()
        
        # ثبت تاریخ برگشت
        self.lend_id.write({'return_date': self.return_date,})

        return_view_mode = self.env.context.get('return_source', 'form')
        return_model = self.env.context.get('return_model', 'openlibrary.book_repository')
        return_id = self.env.context.get('return_id')
    
        # بازگشت به نمای مناسب
        if return_view_mode == 'list':
            # برگشت به نمای لیست
            return {
                'type': 'ir.actions.act_window',
                'res_model': return_model,
                'view_mode': 'list,form',
                'target': 'current',
            }
        else:
            # برگشت به نمای فرم
            return {
                    'type': 'ir.actions.act_window_close',
                    'context': {'reload_parent': True},  # درخواست رفرش
            }
