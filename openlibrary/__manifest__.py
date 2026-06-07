{
    'name': "Open Library",
    'version': '19.0.1.0.1',
    'summary': "Complete Library Management System",

    'description': """
Open Library Management System
===============================    
The **Open Library** module covers the management of a library. This module helps libraries manage their daily operations efficiently. \n

Features:
* Multi-library support
* Multi-repository support
* Book and author management
* Book Editions Management
* Book Genres & Tags
* Member registration and membership
* Lending and return tracking
* Reports and statistics
* Multi-company support
    """,    
    'author': "Madjid Nasiri",
    'website': "https://www.afsannama.ir",
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': 'openlibrary/static/description/icon.png',  
    'images': ['static/description/banner.jpg','static/description/screenshot_books.png','static/description/screenshot_kanban.png','static/description/screenshot_lending.png','static/description/screenshot_members.png','static/description/git_banner.jpg'],
    'maintainer': 'Madjid Nasiri',
    'contributors': ['Madjid Nasiri'],
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'USD',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'support': 'madjidnasiri@gmail.com',
    'category': 'Uncategorized',

    # Define hooks
    'post_init_hook': 'post_init_hook',
    'pre_init_hook': 'pre_init_hook',


    # any module necessary for this one to work correctly
    'depends': ['base','website', 'mail'],

    # always loaded
    "data": [
        "security/security.xml",
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/openlibrary_author_views.xml",
        "views/openlibrary_book_repository_views.xml",
        "views/openlibrary_book_views.xml",
        "views/openlibrary_bookedition_views.xml",
        "views/openlibrary_lend_views.xml",
        "views/openlibrary_lend_wizard_views.xml",
        "views/openlibrary_library_views.xml",
        "views/openlibrary_partner_views.xml",
        "views/openlibrary_repository_views.xml",
        "views/openlibrary_subscriber_views.xml",
        "views/openlibrary_tag_views.xml",
        "views/openlibrary_wizard_views.xml",
        "views/res_config_settings_views.xml",
        "views/templates.xml",
        "views/views.xml",
        "views/menu_view.xml"

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

