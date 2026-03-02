from odoo import models

class ExamMarksheetReport(models.AbstractModel):
    _name = 'report.mis_education_exam.exam_marksheet_template'
    _description = 'Exam Marksheet PDF Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['education.exam.type'].browse(docids)
        print('wwwwwwwwwwwwwwwwwww',self)
        print('wwwwwwwwwwwwwwwwwwwdocids',docids)
        print('wwwwwwwwwwwwwwwwwwwdocs',docs)
        print('wwwwwwwwwwwwwwwwwwwdata',data)
        dfdfdf# adjust model
        return {
            'doc_ids': docs.ids,
            'doc_model': 'education.exam.type',
            'docs': docs,
            'data': data,
        }
