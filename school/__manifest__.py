# -*- coding: utf-8 -*-
{
    'name': "School",

    'summary': """ School System """,

    'description': """  """,

    'author': "Sally Ahmed",

    'price': 4.99,

    'currency': 'EUR',

    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Learn',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'depends':[ 'base','backend_theme_v11','account_invoicing'],

    'images':[],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/student_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]
}
