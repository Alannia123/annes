from odoo import http
from odoo.http import request

class MyWebTemplate(http.Controller):

    @http.route('/mis_ai_analysis/home', type='http', auth='user', website=True)
    def render_ai_template_page(self, **kw):
        user = request.env.user
        search_history = request.env['ai.user.queries'].sudo().search([])  # all records

        print('ddddddddddddddd',search_history)

        data = {
            'search_history': search_history,
            'message': 'Welcome to your custom Odoo web page!',
        }

        return request.render('mis_ai_analysis.ai_ama_chat_window', data)