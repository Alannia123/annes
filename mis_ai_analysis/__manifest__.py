{
    'name': 'Odoo AI Search AMA',
    'version': '18.1',
    'category': 'Tools',
    'summary': 'Search pgvector embeddings from Odoo using AI',
    'description': 'Allows entering a search query in Odoo and fetching results from pgvector stored in Docker DB.',
    'author': 'Ifensys',
    'depends': ['base', 'sale'],
    'data': [
        'data/sequence.xml',
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/ai_search_log_view.xml',
        'views/user_query_views.xml',
        'views/error_logs_view.xml',
        'views/res_config_settings_view.xml',
        'views/ai_search_template.xml',
        'views/ai_ama_search.xml',
        'views/ai_menu.xml',
    ],

    'assets': {
        # Frontend (website/public)
        'web.assets_frontend': [
            '/mis_ai_analysis/static/src/css/ai_style.css',
            '/mis_ai_analysis/static/src/css/ai_language.css',
            '/mis_ai_analysis/static/src/js/ai_chart.js',
            '/mis_ai_analysis/static/src/js/ai_chat.js',
        ],

    },
    'installable': True,
    'application': True,
}
