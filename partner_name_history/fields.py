#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Many2one

# Monkey patch to use a model's field
# to automatically show the partner name at a specific date
original_convert_to_record = Many2one.convert_to_record


def partner_name_history_convert_to_record(self, value, record):
    partner = original_convert_to_record(self, value, record)
    # Do this only when needed:
    # - specific context key is present
    # - returned record is a partner
    if (
        record.env.context.get("use_partner_name_history")
        and partner._name == "res.partner"
    ):
        model_date_field_map = getattr(record, "_partner_name_history_field_map", {})
        model_date_field = model_date_field_map.get(self.name)
        if model_date_field in record._fields:
            # Otherwise the name of the partner
            # is retrieved once and always returned,
            # even if it is requested for different dates
            partner.invalidate_recordset(
                fnames=[
                    "name",
                ],
            )
            partner = partner.with_context(
                partner_name_date=record[model_date_field],
            )
    return partner


Many2one.convert_to_record = partner_name_history_convert_to_record
