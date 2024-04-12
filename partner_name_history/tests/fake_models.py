#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FakeModel(models.Model):
    _name = "fake.model"
    _description = "Fake model used in tests"
    _partner_name_history_field_map = {
        "partner_id": "date",
    }

    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    date = fields.Date()
