#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta
from odoo_test_helper import FakeModelLoader

from odoo.tests import Form, TransactionCase

from .common import _get_name_from_date, _set_partner_name


class TestFields(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_models import FakeModel

        cls.loader.update_registry((FakeModel,))

        partner_form = Form(cls.env["res.partner"])
        partner_form.name = "Test"
        cls.partner = partner_form.save()

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def test_context_use_partner_name_history(self):
        """Context key `use_partner_name_history` allows to return
        the name according to the partner's history."""
        # Arrange
        one_day = relativedelta(days=1)
        partner = self.partner
        original_partner_name = partner.name
        change_dates = [
            datetime.date(2019, 1, 1),
            datetime.date(2020, 1, 1),
        ]
        date_to_names = {date: _get_name_from_date(date) for date in change_dates}
        for change_date, name in date_to_names.items():
            _set_partner_name(
                partner,
                name,
                date=change_date,
            )

        # Act
        fake_records = self.env["fake.model"].create(
            [
                {
                    "partner_id": partner.id,
                    "date": date,
                }
                for date in [
                    change_dates[0] - one_day,
                    change_dates[0] + one_day,
                    change_dates[1] - one_day,
                    change_dates[1] + one_day,
                ]
            ]
        )

        # Assert
        last_partner_name = partner.name
        one_day = relativedelta(days=1)
        date_to_expected_name = {
            change_dates[0] - one_day: original_partner_name,
            change_dates[0] + one_day: _get_name_from_date(change_dates[0]),
            change_dates[1] - one_day: _get_name_from_date(change_dates[0]),
            change_dates[1] + one_day: last_partner_name,
        }
        fake_records_with_ctx = fake_records.with_context(use_partner_name_history=True)
        for record_date, expected_name in date_to_expected_name.items():
            # Without context, the record has the latest name of the partner
            partner.invalidate_recordset(
                fnames=[
                    "name",
                ],
            )
            fake_record = fake_records.filtered(lambda fr: fr.date == record_date)
            self.assertEqual(last_partner_name, fake_record.partner_id.name)

            # With context, the partner's name is the one at the specific date
            fake_record_with_ctx = fake_records_with_ctx.filtered(
                lambda fr: fr.date == record_date
            )
            self.assertEqual(expected_name, fake_record_with_ctx.partner_id.name)
