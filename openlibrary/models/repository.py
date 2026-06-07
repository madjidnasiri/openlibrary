from odoo import _, api, fields, models


class Repository(models.Model):
    _name = 'openlibrary.repository'
    _description = 'OpenLibrary: Library Repository'
    
    name = fields.Char(string='Name', required=True, )
    library_id = fields.Many2one(comodel_name='openlibrary.library', string='Library')
    active = fields.Boolean(string='Active', default=True)
    type = fields.Selection(string='Type', selection=[('1', '📚 Normal'), ('2', '🏛️ Depository'), ('3','🔍 Reference'), ('4','👑 Treasure'),('8', '📦 Archive'), ('9','🗄️ Others'),])
    book_repo_ids = fields.One2many(comodel_name='openlibrary.book_repository', inverse_name='repository_id', string='Books in repository')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', related='library_id.company_id', required=True)

    @api.depends('name', 'library_id.name')
    def _compute_display_name(self):
        for record in self:
            name_parts = []
            
            if record.name:
                name_parts.append(record.name)
            
            if record.library_id and record.library_id.name:
                name_parts.append(f"[{record.library_id.name}]")
            
            record.display_name = ' '.join(name_parts) if name_parts else record.name or 'Unknown'