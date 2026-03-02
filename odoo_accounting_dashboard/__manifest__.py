# -*- coding: utf-8 -*-
{
    'name': 'Accounting Dashboard Odoo17',
    'version': '17.0.1.0.1',
    'category': 'Accounting ',
    'summary': 'Odoo Accounting Dashboard, Accounting Dashboard V17, Account Dashboard, Dashboard, Odoo17 Accounting, Odoo17 Dashboard',
    'description': """Accounting, Odoo Accounting Dashboard, Accounting Dashboard V17, Account Dashboard, Dashboard, Invoice Dashboard, Invoice Graph View, Odoo17""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://cybrosys.com',
    'depends': ['base_accounting_kit','mis_education_fee'],
    'data': [
        'data/account_move_data.xml',
        'reports/today_payment_summary.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'odoo_accounting_dashboard/static/src/js/lib/chart/chart.min.js',
            'odoo_accounting_dashboard/static/src/xml/accounting_dashboard.xml',
            'odoo_accounting_dashboard/static/src/js/accounting_dashboard.js',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
