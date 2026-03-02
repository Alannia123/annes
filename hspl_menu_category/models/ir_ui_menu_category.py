# Copyright 2018, 2021 Heliconia Solutions Pvt Ltd (https://heliconia.io)

from odoo import api, fields, models


class IrUiMenuCcategory(models.Model):
    _name = "ir.ui.menu.category"
    _order = "sequence asc"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        help="Gives the sequence category when displaying "
        "a list of menus at dashboard.",
    )
    menu_id = fields.One2many("ir.ui.menu", "category_id", string="Menu Items")
    # 🔐 Restrict category to a group
    group_ids = fields.Many2many(
        'res.groups',
        'menu_allowed_group_rel',  # relation table name
        'menu_id',  # column referring to this model
        'group_id',  # column referring to res.groups
        string='Allowed Groups',
        help='Only users belonging to at least one of these groups can see this menu category',
    )

    @api.model
    def get_category(self):
        user = self.env.user

        allowed_groups = self.env.ref(
            'mis_education_core.group_education_principal'
        ) | self.env.ref(
            'mis_education_core.group_education_office_admin'
        ) | self.env.ref(
            'mis_education_core.group_education_faculty'
        )

        # intersect user groups with allowed groups
        user_group_ids = (user.groups_id & allowed_groups).ids

        domain = [
            ('menu_id', '!=', False),
            '|',
            ('group_ids', '=', False),  # visible to all
            ('group_ids', 'in', user_group_ids)  # user belongs to allowed groups
        ]
        categories = self.env["ir.ui.menu.category"].search_read(domain)
        return categories
