from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    sidebar_type = fields.Selection(
        selection=[
            ('invisible', 'Invisible'),
            ('small', 'Small'),
            ('large', 'Large')
        ],
        string="Sidebar Type",
        default='large',
        required=True,
    )

    # ✅ Extend self-readable and writable fields properly
    def _get_self_readable_fields(self):
        return super()._get_self_readable_fields() + ['sidebar_type']

    def _get_self_writeable_fields(self):
        return super()._get_self_writeable_fields() + ['sidebar_type']
