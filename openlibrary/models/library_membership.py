from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryMembership(models.Model):
    _name = 'openlibrary.membership'
    _description = 'Library Membership'
    
    subscriber_id = fields.Many2one('openlibrary.subscriber', string='Subscriber', required=True)
    library_id = fields.Many2one('openlibrary.library', string='Library', required=True)
    join_date = fields.Date(string='Join Date', default=fields.Date.today)
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive'), ('suspended', 'Suspended')], string='Status', default='active')
    
    @api.constrains('subscriber_id', 'library_id')
    def _check_unique_membership(self):
        for record in self:
            existing = self.search([
                ('subscriber_id', '=', record.subscriber_id.id),
                ('library_id', '=', record.library_id.id),
                ('id', '!=', record.id)
            ], limit=1)
            if existing:
                raise ValidationError(_(
                    'This subscriber is already a member of this library!'
                ))