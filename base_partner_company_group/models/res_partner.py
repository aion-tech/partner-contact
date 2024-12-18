# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models,api


class Contact(models.Model):
    _inherit = "res.partner"

    company_group_id = fields.Many2one(
        "res.partner",
        "Company group",
        domain=[("is_company", "=", True)],
        recursive=True,
    )
    company_group_member_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="company_group_id",
        string="Company group members",
    )
    company_group_company_member_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="company_group_id",
        string="Company group members",
        domain=[("parent_id", "=", False)],
    )

    def _commercial_fields(self):
        return super()._commercial_fields() + ["company_group_id"]

    def open_company_group_member(self): 
        return {
            'type': 'ir.actions.act_window', 
            'res_model': 'res.partner', 
            'name': self.name, 
            'view_type': 'form', 
            'view_mode': 'form', 
            'res_id': self.id, 
            'target': 'current', 
        }