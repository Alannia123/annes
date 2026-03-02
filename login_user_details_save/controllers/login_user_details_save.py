from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.home import Home, ensure_db
from odoo.addons.web.controllers.session import Session
from odoo.addons.web.controllers.utils import ensure_db

import base64
import odoo


class SessionWebsite(Session):
    @http.route('/web/session/logout_popup', type='http', auth="public", website=True)
    def logout_popup(self, **kw):
        """Render logout popup with all saved user records"""
        saved_users = request.env['logout.popup'].sudo().search([])
        conf_param = request.env['ir.config_parameter'].sudo()
        base_url = conf_param.get_param('web.base.url')
        users = []
        for rec in saved_users:
            users.append({
                'id': rec.id,
                'name': rec.name,
                'display': rec.user_id.name,
                'image': f"{base_url}/web/image?model=res.users&id={rec.user_id.id}&field=image_1920"
            })
        return request.render("login_user_details_save.logout_popup_template", {'saved_users': users})

    @http.route('/web/session/remove_saved_user', type='json', auth="user", csrf=False)
    def remove_saved_user(self, user_id):
        """AJAX endpoint to delete a saved user"""
        rec = request.env['logout.popup'].sudo().browse(int(user_id))
        if rec.exists():
            rec.unlink()
            return {"success": True}
        return {"success": False, "error": "User not found"}


class WebHomeAutoSave(Home):
    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, **kw):

        ensure_db()
        request.params['login_success'] = False

        # Let Odoo handle public environment safely
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        # No need to manually set public user, Odoo already provides it
        values = dict(kw)
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            try:
                login = request.params['login']
                password = request.params['password']
                uid = request.session.authenticate(request.db, login, password)
                request.params['login_success'] = True

                # ✅ Auto-save credentials safely
                logout_popup = request.env['logout.popup'].sudo()
                rec = logout_popup.search([('user_id', '=', uid)], limit=1)
                if not rec:
                    logout_popup.create({
                        'name': login,
                        'user_id': uid,
                        'password': logout_popup.encrypt_password(password),
                        'save_details': True,
                    })
                else:
                    rec.password = logout_popup.encrypt_password(password)

                return request.redirect(self._login_redirect(uid, redirect=redirect))

            except odoo.exceptions.AccessDenied:
                values['error'] = "Wrong login or password"

        # ✅ Always render with sudo so website layouts load fine
        # response = request.render('web.login', values, sudo=True)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response

