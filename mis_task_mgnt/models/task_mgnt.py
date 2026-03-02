# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime
from random import randint


class MisTask(models.Model):
    _name = 'task.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Task Management'
    _order = "id desc"

    name = fields.Char('Name', required=False, readonly=True, tracking=True)
    create_date = fields.Date('Date', default=lambda self: fields.Datetime.now(), tracking=True, readonly=True)
    scheduled_date = fields.Date('Scheduled Date', default=lambda self: fields.Datetime.now(), tracking=True)
    completion_date = fields.Date('Completion Date',  tracking=True)
    user_id = fields.Many2one('res.users', 'Assigned To', tracking=True, domain=lambda self: [('groups_id', 'in', [self.env.ref('base.group_user').id])])
    task_desc = fields.Text('Task Desc', copy=False, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('assigned', 'Assigned'), ('in_progress', 'In Progress'), ('done', 'Completed')],
                                        default='draft', string="State", help="Stages of attendance" , tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        print('fffffffffffff',vals_list)
        for vals in vals_list:
            if 'name' not in vals or vals['name'] == 'New':
                user_name = self.env['res.users'].browse(int(vals['user_id'])).name
                name = self.env['ir.sequence'].next_by_code('task.management') or _('New')
                vals['name'] = user_name + ' - ' + name
        return super().create(vals_list)


    def action_assign_to_faculty(self):
        self.activity_schedule('mis_task_mgnt.task_assign_to_faculty_notification',
                                   user_id=self.user_id.id, note=f'Task Assigned For You {self.name}')

        return self.write({"state": "assigned"})

    def accept_task_by_faculty(self):
        self.activity_schedule('mis_task_mgnt.task_accepted_by_faculty_notification',
                               user_id=self.create_uid.id, note=f'Task Accepted On  {self.name}')
        return self.write({"state": "in_progress"})

    def complete_task_by_faculty(self):
        self.activity_schedule('mis_task_mgnt.task_completed_by_faculty_notification',
                               user_id=self.create_uid.id, note=f'Task Completed On  {self.name}')
        assign_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id),
                                                         ('activity_type_id', '=', self.env.ref(
                                                             'mis_task_mgnt.task_assign_to_faculty_notification').id)])
        accept_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id),
                                                         ('activity_type_id', '=', self.env.ref(
                                                             'mis_task_mgnt.task_accepted_by_faculty_notification').id)])
        assign_activity_ids.unlink()
        accept_activity_ids.unlink()
        today_date = datetime.today().strftime('%Y-%m-%d')
        return self.write({"state": "done", 'completion_date': today_date})

    def reset_to_draft(self):
        return self.write({"state": "draft", 'completion_date': False})