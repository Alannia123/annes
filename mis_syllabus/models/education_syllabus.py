# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo import models, fields, api
import requests
import base64
import logging

_logger = logging.getLogger(__name__)


class EducationSyllabus(models.Model):
    """Model representing the Timetable for classes."""
    _name = 'education.syllabus'
    _description = 'Syllabus'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True,
        readonly=True,
        help="Generated name based on class, division, academic year, and subject(s)."
    )
    class_id = fields.Many2one('education.class',
                                        string='Class', required=True,
                                        help="Select the class for"
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
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(),
        help="Company associated with the timetable.")
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True)
    first_unit_syllabus_ids = fields.One2many('first.unit.syllabus', 'fir_syllabus_id',string='First Unit Syllabus',copy=False)
    half_syllabus_ids = fields.One2many('half.syllabus', 'half_syllabus_id',string='Halfly Syllabus',copy=False)
    second_unit_syllabus_ids = fields.One2many('second.unit.syllabus', 'sec_syllabus_id',string='Second Unit Syllabus',copy=False)
    annual_syllabus_ids = fields.One2many('annual.syllabus', 'annual_syllabus_id', string='Annual Syllabus', copy=False)

    _sql_constraints = [
        (
            'uniq_class_academic_year',
            'unique(class_id, academic_year_id)',
            'Syllabus already exists for this Class and Academic Year.'
        )
    ]

    @api.depends('class_id','academic_year_id')
    def _compute_name(self):
        for rec in self:
            parts = []
            if rec.class_id:
                parts.append(rec.class_id.name)
            if rec.academic_year_id:
                parts.append(rec.academic_year_id.name)
            rec.name = "/".join(parts) if parts else "New"

    @api.model
    def create(self, vals):
        record = super().create(vals)

        # 👇 Auto-create syllabus lines on create (button / cron / import)
        if record.class_id:
            subject_syllabus_ids = record._prepare_syllabus_lines(record.class_id)
            record.first_unit_syllabus_ids = subject_syllabus_ids
            record.half_syllabus_ids = subject_syllabus_ids
            record.second_unit_syllabus_ids = subject_syllabus_ids
            record.annual_syllabus_ids = subject_syllabus_ids
        return record



    def _prepare_syllabus_lines(self, class_id):
        """Prepare First Unit Syllabus lines for a class"""
        lines = []
        subjects = class_id.subject_ids.mapped('subject_id')
        for subject in subjects:
            lines.append((
                0, 0, {
                'subject_id': subject.id,
            }
            ))

        return lines


class EducationSyllabusFirst(models.Model):
    _name = 'first.unit.syllabus'
    _description = 'First Unit Syllabus'

    fir_syllabus_id = fields.Many2one('education.syllabus', 'First Syllabus',copy=False)
    subject_id = fields.Many2one('education.subject', 'Subject',copy=False)
    syllabus = fields.Char('Syllabus',copy=False)


class EducationHalf(models.Model):
    _name = 'half.syllabus'
    _description = 'Halfly Syllabus'

    half_syllabus_id = fields.Many2one('education.syllabus', 'Halfly Syllabus',copy=False)
    subject_id = fields.Many2one('education.subject', 'Subject',copy=False)
    syllabus = fields.Char('Syllabus',copy=False)


class EducationSyllabusSecond(models.Model):
    _name = 'second.unit.syllabus'
    _description = 'Second Unit Syllabus'

    sec_syllabus_id = fields.Many2one('education.syllabus', 'First Syllabus',copy=False)
    subject_id = fields.Many2one('education.subject', 'Subject',copy=False)
    syllabus = fields.Char('Syllabus',copy=False)


class EducationSyllabusAnnual(models.Model):
    _name = 'annual.syllabus'
    _description = 'Annual Syllabus'

    annual_syllabus_id = fields.Many2one('education.syllabus', 'First Syllabus',copy=False)
    subject_id = fields.Many2one('education.subject', 'Subject',copy=False)
    syllabus = fields.Char('Syllabus',copy=False)



