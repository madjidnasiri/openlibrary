from odoo import http
from odoo.http import request


class OpenLibrary(http.Controller):
    @http.route('/open_library/hello', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/books/status', auto='public', website=True)
    def book_status_in_website(self, **kw):
        Books = http.request.env['openlibrary.book_repository']
        return http.request.render('openlibrary.book_repositories_public_user', {'books': Books.search([])})

    @http.route('/open_library/ws_authors', auto='public', website=True)
    def index_website_authors(self, **kw):
        Authors = http.request.env['openlibrary.authors']
        return http.request.render('openlibrary.ws_author_list', {'authors': Authors.search([])})

    @http.route('/open_library/authors/<name>/', auth='public', website=True)
    def author_name(self, name):
        Authors = http.request.env['openlibrary.authors']
        return http.request.render('openlibrary.ws_author_list', {'authors': Authors.search([('name','like',name)])})
        #return '<h1>{}</h1>'.format(name)

    @http.route('/open_library/authors/<int:id>/', auth='public', website=True)
    def author_id(self, id):
        Authors = http.request.env['openlibrary.authors']
        return http.request.render('openlibrary.ws_author_list', {'authors': Authors.browse([id])})
 
    @http.route('/ol/author/<model("openlibrary.authors"):author>/', auth='public', website=True)
    def ol_author_view_by_model(self, author):
        return http.request.render('openlibrary.ws_author_view', {'author': author})
    
            
        #return '<h1>{}</h1>'.format(name)    

#     @http.route('/open_library/open_library/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('open_library.listing', {
#             'root': '/open_library/open_library',
#             'objects': http.request.env['open_library.open_library'].search([]),
#         })

#     @http.route('/open_library/open_library/objects/<model("open_library.open_library"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('open_library.object', {
#             'object': obj
#         })

