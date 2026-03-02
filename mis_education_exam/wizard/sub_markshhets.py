# -*- coding: utf-8 -*-

from odoo import fields, models, _
import xlwt
import io
from datetime import datetime
import base64
from odoo.exceptions import ValidationError, UserError


class SubGenerateMArk(models.TransientModel):
    _name = 'subject.marksheet.wizard'
    _description = 'Subject Marksheet'


    exam_valuation_id = fields.Many2one('education.exam.valuation', string='Select Validated Exam', required=True, domain=[('state', '=', 'completed')])


    def action_generate_subject_marksheet(self):
        data = {
            'exam_valuation_id': self.exam_valuation_id.id,
            # 'exam': self.exam_id.id,
        }
        return self.env.ref('mis_education_exam.exam_subject_marksheet_pdf').report_action(self.exam_valuation_id.id)

