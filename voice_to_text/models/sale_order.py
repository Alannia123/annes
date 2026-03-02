# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrder(models.Model):
    """
    Inherits sale.order to add custom functionality if needed in the future.
    """
    _inherit = 'sale.order'

    voice_note = fields.Char("Voice To Text")