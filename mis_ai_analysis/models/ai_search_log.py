from odoo import models, fields, api, _

class AiSearchLog(models.Model):
    _name = 'ai.search.log'
    _description = 'AI Search Log'
    _order = 'create_date desc'

    name = fields.Char('Name', copy=False)
    query_text = fields.Text(string="Search Query", required=True)
    rephrased_text = fields.Text(string="Rephrased Query", required=False)
    result_text = fields.Html(string="Results")
    user_id = fields.Many2one('res.users', string="Searched By", default=lambda self: self.env.user, readonly=True)
    create_date = fields.Datetime(string="Search Date", readonly=True)
    result_from_db = fields.Text(string="DB Response", readonly=True)
    generated_query = fields.Text(string="Generated Query", readonly=True)
    table_schema = fields.Text(string="table Schema", readonly=True)
    ai_explanation = fields.Text(string="AI Explanation", readonly=True)
    shared_with_ids = fields.Many2many(
                        'res.users',
                        'ai_search_log_users_rel',  # relation table name
                        'log_id',  # column linking to ai.search.log
                        'user_id',  # column linking to res.users
                        string="Shared With Users"
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('ai.search.log') or _("New")
        return super(AiSearchLog, self).create(vals_list)





class AiuserQuery(models.Model):
    _name = 'ai.user.queries'
    _description = 'AI User Queries'
    _order = 'create_date desc'

    query_text = fields.Text(string="Searched Query", required=True)
    create_date = fields.Datetime(string="Search Date", readonly=True)
    result_from_db = fields.Text(string="DB Response", readonly=True)
    generated_query = fields.Text(string="Generated Query", readonly=True)
    user_id = fields.Many2one('res.users', string="Searched By", default=lambda self: self.env.user, readonly=True)
    shared_with_ids = fields.Many2many(
        'res.users',
        'ai_user_query_users_rel',  # relation table name
        'query_id',  # column linking to ai.search.log
        'user_id',  # column linking to res.users
        string="Shared With Users"
    )


class AisearchError(models.Model):
    _name = 'ai.search.error'
    _description = 'AI Search Errors'
    _order = 'create_date desc'

    name = fields.Char('Name', copy=False)
    query_text = fields.Text(string="Searched Query", required=True)
    create_date = fields.Datetime(string="Search Date", readonly=True)
    error = fields.Text(string="Error", readonly=True)
    generated_query = fields.Text(string="Generated Query", readonly=True)
    error_on = fields.Char(string="Error On", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('ai.error.log') or _("New")
        return super(AisearchError, self).create(vals_list)
