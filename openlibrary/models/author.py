from odoo import models, fields, api

class Authors(models.Model):
    _name = 'openlibrary.author'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'OpenLibrary: Author'
    
    name = fields.Char(string='Name',required=True, tracking=True)
    pseudonym = fields.Char(string='Pseudonym')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'),], string='Gender')
    nationality_id = fields.Many2one(comodel_name='res.country', string='Nationality')
    birthday = fields.Date(string="Born Date")
    dieddate = fields.Date(string="Died Date")
    biography = fields.Html(string='Biography',tracking=True)
    book_ids = fields.Many2many(comodel_name='openlibrary.book', string='Books')

    def name_get(self):
        result = []
        for record in self:
            parts = []
            if record.name:
                parts.append(record.name)
            if record.pseudonym:
                parts.append(f"({record.pseudonym})")
            
            display = ' '.join(parts)
            result.append((record.id, display))
        return result    