from odoo import fields, models, tools

class OpenLibraryTagReport(models.Model):
    _name = 'openlibrary.tag.report'
    _description = 'OpenLibrary: Tag Report (Stock vs Lending)'
    _auto = False
    _order = 'tag_id'

    tag_id = fields.Many2one('openlibrary.tag', string='Tag', readonly=True)

    book_repo_count = fields.Integer(string='Total Copies', readonly=True)
    available_count = fields.Integer(string='Available Now', readonly=True)
    lent_now_count = fields.Integer(string='Lent Now', readonly=True)
    lent_now_percentage = fields.Float(string='Lent Now %', readonly=True, aggregator='avg')

    total_lend_count = fields.Integer(string='Total Lend Events', readonly=True, help='Total number of times any copy with this tag has ever been lent.')
    ever_lent_copies = fields.Integer(string='Copies Ever Lent', readonly=True, help='Number of distinct copies that have been lent at least once.')
    ever_lent_percentage = fields.Float(string='Ever Lent %', readonly=True, aggregator='avg')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    t.id                                       AS id,
                    t.id                                       AS tag_id,

                    -- وضعیت فعلی موجودی
                    COUNT(DISTINCT br.id)                      AS book_repo_count,
                    COUNT(DISTINCT br.id)
                        FILTER (WHERE br.status = 'free')      AS available_count,
                    COUNT(DISTINCT br.id)
                        FILTER (WHERE br.status IN
                            ('lent', 'delay', 'suspicious', 'dangerous'))
                                                                AS lent_now_count,
                    ROUND(
                        100.0 * COUNT(DISTINCT br.id)
                            FILTER (WHERE br.status IN
                                ('lent', 'delay', 'suspicious', 'dangerous'))
                        / NULLIF(COUNT(DISTINCT br.id), 0)
                    , 2)                                        AS lent_now_percentage,

                    -- تاریخچهٔ تجمعی امانت‌ها
                    COUNT(l.id)                                AS total_lend_count,
                    COUNT(DISTINCT l.book_repo_id)              AS ever_lent_copies,
                    ROUND(
                        100.0 * COUNT(DISTINCT l.book_repo_id)
                        / NULLIF(COUNT(DISTINCT br.id), 0)
                    , 2)                                        AS ever_lent_percentage

                FROM openlibrary_tag t
                LEFT JOIN openlibrary_book_openlibrary_tag_rel rel
                       ON rel.openlibrary_tag_id = t.id
                LEFT JOIN openlibrary_book b
                       ON b.id = rel.openlibrary_book_id
                LEFT JOIN openlibrary_book_repository br
                       ON br.book_id = b.id AND br.active = true
                LEFT JOIN openlibrary_lend l
                       ON l.book_repo_id = br.id
                GROUP BY t.id
            )
        """ % self._table)
