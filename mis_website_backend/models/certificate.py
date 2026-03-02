from odoo import models, fields, api

class CertificateMaster(models.Model):
    _name = "mis.certificate"
    _description = "Certificate Configuration"

    name = fields.Char("Certificate Name", required=True)
    academic_year_id = fields.Many2one("education.academic.year", required=True)
    certificate_type = fields.Selection([
        ('participation', "Participation"),
        ('winner', "Winners"),
        ('custom', "Custom"),
    ], required=True)

    template_background = fields.Binary("Certificate Background (Image)")
    student_line_ids = fields.One2many("mis.certificate.line", "certificate_id", string="Students")


class CertificateLine(models.Model):
    _name = "mis.certificate.line"
    _description = "Certificate Students"

    certificate_id = fields.Many2one("mis.certificate", ondelete="cascade")
    student_id = fields.Many2one("education.student", required=True)
    position = fields.Selection([
        ('first', "First Place"),
        ('second', "Second Place"),
        ('third', "Third Place"),
        ('none', "Participation"),
    ], default="none")

    certificate_url = fields.Char("Download URL", compute="_compute_url")

    def _compute_url(self):
        for rec in self:
            rec.certificate_url = f"/my/certificate/{rec.id}"

