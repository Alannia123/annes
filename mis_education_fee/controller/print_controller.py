from odoo import http
from odoo.http import request
#
# class StudentFeeController(http.Controller):
#
#     @http.route('/student/fee/bill/<int:student_id>', type='http', auth='user', website=True)
#     def preview_student_bill(self, student_id, **kw):
#
#         student = request.env['student.fee.line'].sudo().browse(student_id)
#         print('---==============-----------0000000000', student_id)
#
#         report = request.env.ref('mis_education_fee.report_mis_fee_invoices')
#         print('---==============-----------0000000000',student_id)
#
#         html = report._render_qweb_html(student.ids)[0]
#
#         return request.make_response(html)



class StudentFeeController(http.Controller):

    @http.route('/student/fee/bill/<int:student_id>', type='http', auth='user', website=True)
    def preview_student_bill(self, student_id, **kw):
        id = 378
        student = request.env['student.fee.line'].sudo().browse(id)
        print('ttttttttttttt88888888899------------',student)

        return request.render(
            'mis_education_fee.report_mis_fee_invoices',
            {
                'docs': student
            }
        )