# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import requests
import base64
import logging

_logger = logging.getLogger(__name__)


class EducationTimetable(models.Model):
    """Model representing the Timetable for classes."""
    _name = 'education.question.bank'
    _description = 'Question Bank'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        readonly=True,
        help="Generated name based on class, division, academic year, and subject(s)."
    )
    class_division_id = fields.Many2one('education.class.division',
                                        string='Class', required=True,
                                        help="Select the class and division for"
                                             "the timetable."
                                        )
    academic_year_id = fields.Many2one(
                'education.academic.year',
                string="Academic Year",
                domain="[('enable', '=', True)]",
                readonly=True,
                default=lambda self: self.env['education.academic.year']
                .search([('enable', '=', True)], limit=1)
            )
    subject_id = fields.Many2one('education.subject', 'Subject', copy=False,)
    subject_ids = fields.Many2many(
        comodel_name='education.subject',
        relation='education_student_subject_rel',
        column1='student_id',
        column2='subject_id',
        string='Subjects'
    )

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help="Company associated with the timetable.")
    pdf_file = fields.Binary(string="Upload Question Bank", attachment=True)
    file_name = fields.Char('File Name')
    preview_image = fields.Binary(string="PDF Preview", readonly=True)
    pre_file_name = fields.Char('File Name')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], 'State', default='draft', tracking=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)

    @api.depends(
        'class_division_id',
        'academic_year_id',
        'subject_id',
        'subject_ids'
    )
    def _compute_name(self):
        for rec in self:
            parts = []

            # Class / Division
            if rec.class_division_id:
                parts.append(rec.class_division_id.name)

            # Academic Year
            if rec.academic_year_id:
                parts.append(rec.academic_year_id.name)

            # Single Subject
            if rec.subject_id:
                parts.append(rec.subject_id.name)

            rec.name = "/".join(parts) if parts else "New"

    @api.onchange('class_division_id')
    def _onchange_division_id(self):
        self.subject_ids = False
        self.subject_id = False
        if self.class_division_id:
            subjects = self.class_division_id.class_id.subject_ids.mapped('subject_id')
            domain = [('id', 'in', subjects.ids)]
            self.subject_ids = subjects.ids

    def set_to_post(self):
        if self.pdf_file:
            self.state = 'done'

    def reste_to_draft(self):
        self.state = 'draft'


