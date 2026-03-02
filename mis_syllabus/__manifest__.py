# -*- coding: utf-8 -*-

{
    'name': 'Educational Syllabus',
    'version': '17.0.1.0.1',
    'category': 'Extra Tools',
    'summary': """Syllabus for Education erp""",
    'description': """Education Syllabus provides a comprehensive Syllabus 
     management system, enhancing the functionality of  educational 
     institutions.""",
    'author': 'Alanniainfotechz',
    'company': 'Alanniainfotechz',
    'maintainer': 'Alanniainfotechz',
    'depends': ['mis_education_core'],
    'data': [
        'security/ir.model.access.csv',
        'views/education_syllabus_views.xml',
        'views/ir_config_parameter_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
