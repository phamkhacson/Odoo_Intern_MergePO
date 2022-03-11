# -*- coding: utf-8 -*-

{
    'name': 'Merge Purchase Order',
    'category': 'Purchases',
    'summary': 'This module will merge purchase order.',
    'version': '14.0.1.0.0',
    'website': 'http://www.aktivsoftware.com',
    'author': 'Son@magenest',
    'description': 'Merge Purchase Order',
    'license': "AGPL-3",

    'depends': ['purchase', 'stock', 'l10n_us'],
    'data': [
        'views/view.xml',
        'security/ir.model.access.csv'
    ],

    'images': [],
    'auto_install': False,
    'installable': True,
    'application': True

}
