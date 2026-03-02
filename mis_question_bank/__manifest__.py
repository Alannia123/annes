# -*- coding: utf-8 -*-

{
    'name': 'Educational Question bank MIS',
    'version': '17.0.1.0.1',
    'category': 'Extra Tools',
    'summary': """Timetable for Education erp""",
    'description': """Education Time Table provides a comprehensive timetable 
     management system, enhancing the functionality of  educational 
     institutions.""",
    'author': 'Alanniainfotechz',
    'company': 'Alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['mis_education_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/education_question_bank_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
