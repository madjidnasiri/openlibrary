# models/openlibrary_settings.py
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    delay_warning_threshold = fields.Integer(
        string="Warning Delay (Days)",
        default=3,
        help="If days late is less than or equal to this, status is 'Delay'", 
        config_parameter='openlibrary.delay_warning_threshold'      
    )
    
    delay_suspicious_threshold = fields.Integer(
        string="Suspicious Delay (Days)",
        default=30,
        help="If days late exceeds this, status is 'Dangerous Delay'",
        config_parameter='openlibrary.delay_suspicious_threshold'

    )

    def action_save_config(self):
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('openlibrary.delay_warning_threshold', self.delay_warning_threshold)
        config.set_param('openlibrary.delay_suspicious_threshold', self.delay_suspicious_threshold)
        
        return {
            'type': 'ir.actions.act_window_close',
        }

    def action_load_config(self):
        config = self.env['ir.config_parameter'].sudo()
        self.delay_warning_threshold = int(config.get_param('openlibrary.delay_warning_threshold', default='3'))
        self.delay_suspicious_threshold = int(config.get_param('openlibrary.delay_suspicious_threshold', default='30'))
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.config',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
