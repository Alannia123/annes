from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError




class StudentHomework(models.Model):
    _name = 'student.homework'
    _description = 'Student Homework'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(string="Homework Title", required=True, readonly=True, default='New' )
    description = fields.Text(string="Description")
    homework_date = fields.Date(string='Homework Date', default=fields.Date.today, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Division', required=True, readonly=True)
    work_line_ids = fields.One2many('student.homework.line', 'work_id', string="Home Work")
    academic_year = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
        default=lambda self: self._get_default_academic_year(),
        readonly=True
    )
    faculty_user_id = fields.Many2one('res.users', 'Faculty User', copy=False)

    @api.model
    def _get_default_academic_year(self):
        """Return the active academic year where enable=True."""
        return self.env['education.academic.year'].search([('enable', '=', True)], limit=1)
    # state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], 'State', default='draft', tracking=True)
    # homework_desc = fields.Html('Homeworks', readonly=True)
    # faculty_id = fields.Many2one('education.faculty', string='Faculty')
    # user_ids = fields.Many2many('res.users', 'homework_user_rel', 'homework_user_id', 'user_id',
    #                                'Faculties')

    # @api.model
    # def create(self, vals):
    #     res = super(StudentHomework, self).create(vals)
    #     res.name = str(res.class_div_id.name) + ' - (' + str(res.homework_date.strftime("%d-%m-%Y")) +')'
    #     res.description = res.name
    #     return res



class StudentHomeworkLine(models.Model):
    _name = 'student.homework.line'
    _description = 'Student Homework Line'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"


    name = fields.Char('Name')
    work_id = fields.Many2one('student.homework', string="Home Work")
    homework_date = fields.Date(string='Homework Date', default=fields.Date.today, readonly=True)
    class_div_id = fields.Many2one('education.class.division', 'Division', required=True)
    subject_id = fields.Many2one('education.subject', 'Subject', required=True)
    domain_subjects = fields.Many2many('education.subject', 'edu_sub_mis_rel', 'edu_subject_id', 'subject_id',
                                       'Subjects')
    homework = fields.Text('Homework')
    uploaded_by = fields.Many2one('res.users', 'Uploaded By', default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], 'State', default='draft', tracking=True)
    academic_year = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
        default=lambda self: self._get_default_academic_year(),
        readonly=True
    )
    faculty_user_id = fields.Many2one('res.users', 'Faculty User', copy=False, readonly=True)


    @api.model
    def _get_default_academic_year(self):
        """Return the active academic year where enable=True."""
        return self.env['education.academic.year'].search([('enable', '=', True)], limit=1)


    @api.model
    def create(self, vals):
        # Get class division and subject
        class_div = self.env['education.class.division'].browse(vals.get('class_div_id'))
        subject = self.env['education.subject'].browse(vals.get('subject_id'))

        # Set record name
        name = f"{class_div.name} ({subject.name})" if class_div and subject else _("New")
        vals["name"] = name

        # Determine today's date (or use vals['date'] if available)
        today = vals.get('homework_date') or fields.Date.context_today(self)

        # Check if already created for today
        existing = self.search([
            ('class_div_id', '=', class_div.id),
            ('subject_id', '=', subject.id),
            ('homework_date', '=', today)
        ], limit=1)

        if existing:
            raise ValidationError(_(
                f"A Homework for {class_div.name} ({subject.name}) already exists for {today}."
            ))

        # Create record
        return super().create(vals)


    @api.onchange('class_div_id', 'subject_id')
    def domain_subject_ids(self):
        # if not self.class_div_id:
        #     raise ValidationError(_( "Please enter Division First...!" ))
        if self.class_div_id:
            self.domain_subjects = self.class_div_id.class_id.subject_ids.mapped('subject_id').ids
        else:
            self.domain_subjects = False

    def action_post(self):
        work_line_id = False
        homework_id = False
        today = date.today()
        homework_id = self.env['student.homework'].search([('class_div_id', '=', self.class_div_id.id), ('homework_date', '=', self.homework_date)])
        if not homework_id:
            homework_id = self.env['student.homework'].sudo().create({
                                'faculty_user_id': self.class_div_id.faculty_id.user_id.id,
                                'homework_date': today,
                                'class_div_id': self.class_div_id.id,
                                'name': str(self.class_div_id.name) + ' - (' + str(today.strftime("%d-%m-%Y")) + ')',
                            })
        self.work_id = homework_id.id
        self.faculty_user_id = self.class_div_id.faculty_id.user_id.id
        self.state  = 'post'

    def reset_to_draft(self):
        self.state = 'draft'

    def view_home_work(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Homework',
            'res_model': 'student.homework',
            'res_id': self.work_id.id,  # record you want to open
            'view_mode': 'form',
            'view_id': self.env.ref('mis_homework.view_student_homework_form').id,
            'target': 'current',  # or 'new' to open in popup
        }