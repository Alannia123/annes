from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def action_generate_class_records(self):
        """Create records ONCE per enabled academic year for ALL classes"""

        self.ensure_one()

        # 🎓 Get ENABLED academic year
        year = self.env['education.academic.year'].search(
            [('enable', '=', True)],
            limit=1
        )

        if not year:
            raise UserError(_("No enabled Academic Year found."))

        # 🔒 Prevent duplicate generation
        key = f"class_records_generated_{year.id}"
        already_done = self.env['ir.config_parameter'].sudo().get_param(key)

        if already_done:
            raise UserError(
                _("Records already generated for Academic Year: %s") % year.name
            )

        classes = self.env['education.class'].search([])
        if not classes:
            raise UserError(_("No classes found."))

        # 🚀 Create records
        for cls in classes:
            self.env['education.syllabus'].create({
                'class_id': cls.id,
                'academic_year_id': year.id,
            })

        # ✅ Mark year as generated
        self.env['ir.config_parameter'].sudo().set_param(key, '1')

        # 🎉 Success toast
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _(
                    'Class records successfully created for Academic Year: %s'
                ) % year.name,
                'type': 'success',
                'sticky': True,
            }
        }
