# -*- coding: utf-8 -*-

{
    "name": "Educational Fee Management MIS",
    "version": '17.0.1.0.1',
    "category": 'Industries',
    'summary': """Education fee is the core module of Educational ERP software, 
     a management application for effective school run .""",
    'description': """Education fee provides a comprehensive student fee
     management solution to automate, streamline and transform fee processing
     in educational institutions.""",
    "author": "Alanniainfotechz",
    "company": "Alanniainfotechz",
    'maintainer': 'Alanniainfotechz',
    "depends": ['account', 'mis_education_core', 'hr_expense'],
    "data": [
        'data/inv_generate.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        # 'reports/fee_report_template.xml',
        'reports/school_fee_template.xml',
        # 'reports/media_print_format.xml',
        'reports/ir_action_report.xml',
        'reports/application_fee_receipt_template.xml',

        'views/application_receipt_view.xml',
        # 'views/account_move_line_views.xml',
        'views/education_fee_structure_views.xml',
        'views/student_fees_views.xml',
        'views/fees_collect_overview.xml',
        # 'views/school_receipt_view.xml',
        # 'views/account_journal_templates.xml',
        'views/account_journal_views.xml',
        'views/fee_concession_view.xml',
        'views/education_fee_structure_menu_views.xml',
    ],

    'assets': {
            'web.assets_backend': [
                'mis_education_fee/static/src/js/fee_overview.js',
                # 'mis_education_fee/static/src/xml/fee_overview.xml',
                'mis_education_fee/static/src/xml/version_1.xml',
            ],
        },

    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    "installable": True,
    "auto_install": False,
    'application': True,
}
