# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
    Configure the access credentials
    """
    _inherit = 'res.config.settings'

    is_ai_connector = fields.Boolean(config_parameter='mis_ai_analysis.is_ai_connector', default=False,
                                                help='Enable or disable the Amazon S3 connector.')
    mcp_internal_secret = fields.Char(string="MCP Secret Key", readonly=False,
                                      config_parameter='mis_ai_analysis.mcp_internal_secret',
                                      help='Enter MCP Secret Key here.')
    mcp_server_url = fields.Char(string="MCP Server Url", readonly=False,
                                      config_parameter='mis_ai_analysis.mcp_server_url',
                                      help='Enter MCP Secret Key here.')
