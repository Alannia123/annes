from odoo import models, fields, api
from odoo.exceptions import UserError

class SchoolStaffLeave(models.Model):
    _name = "school.staff.leave"
    _description = "School Staff Leave"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(default="Leave Request", readonly=True)
    staff_id = fields.Many2one(
        "res.users", string="Staff", required=True,
        default=lambda self: self.env.user
    )

    leave_type = fields.Selection([
        ("cl", "Casual Leave"),
        ("sl", "Sick Leave"),
        ("el", "Earned Leave"),
        ("permission", "Permission"),
    ], required=True)

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    reason = fields.Text(required=True)
    attachment = fields.Binary(string="Attachment")

    state = fields.Selection([
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ], default="draft", tracking=True)

    @api.onchange("date_from", "date_to")
    def _onchange_dates(self):
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError("From date cannot be after To date.")

    def action_submit(self):
        self.state = "submitted"

    def action_approve(self):
        self.state = "approved"

    def action_reject(self):
        self.state = "rejected"
