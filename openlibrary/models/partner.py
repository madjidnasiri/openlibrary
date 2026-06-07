from odoo import _, api, fields, models


class partner(models.Model):
    _inherit = 'res.partner'

    subscriber_id = fields.Many2one(comodel_name='openlibrary.subscriber', string='Subscriber', copy=False, ondelete='set null',)
    
