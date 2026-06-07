from odoo import models, fields, api

class wizard(models.TransientModel):
    _name = 'openlibrary.wizard'
    _description = 'OpenLibrary: Wizard'

    number = fields.Integer(string='Number', default=1)
    book_edition_id = fields.Many2one(comodel_name='openlibrary.bookedition', string='Book Edition', )
    repository_id = fields.Many2one(comodel_name='openlibrary.repository', string='Repository',)
    purchase_price = fields.Float(string='Price',)

    def create_book_repo(self):
        print('---***( Hello )***---')
        for i in range(self.number):
            print(f"{self.number}:{i+1}")
            self.env['openlibrary.book_repository'].sudo().create(
                {
                    'book_edition_id':self.book_edition_id.id ,
                    'repository_id': self.repository_id.id,
                    'purchase_price': self.purchase_price,
                    'active': True,
                }
            )

