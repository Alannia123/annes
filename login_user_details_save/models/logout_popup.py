# -*- coding: utf-8 -*-
from odoo import fields, models, api
import base64


class LogoutPopup(models.Model):
    """Model for saved user credentials"""
    _name = "logout.popup"
    _description = "Logout Popup"

    name = fields.Char(string="Login Name", required=True)
    save_details = fields.Boolean(default=True, string="Save Login Details?")
    user_id = fields.Many2one('res.users', string='User', required=True)
    password = fields.Char(string="Encoded Password")

    @api.model
    def encrypt_password(self, plain):
        """Simple base64 encoding for demo (not secure for production)."""
        return base64.b64encode(plain.encode('utf-8')).decode('utf-8')

    @api.model
    def decrypt_password(self, encoded):
        try:
            return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        except Exception:
            return ''
