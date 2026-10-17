import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import implement
import main


class TestSusuSystem(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.old_filename = implement.filename
        self.old_metadata_file = implement.metadata_file

        implement.filename = str(
            Path(self.temp_dir.name) / "list.json"
        )
        implement.metadata_file = str(
            Path(self.temp_dir.name) / "susu_storage.json"
        )

    def tearDown(self):
        implement.filename = self.old_filename
        implement.metadata_file = self.old_metadata_file
        self.temp_dir.cleanup()

    def write_test_data(self, members, metadata=None):
        if metadata is None:
            metadata = {
                "current_week": 1,
                "payout_history": []
            }

        with open(
            implement.filename, "w", encoding="utf-8"
        ) as file:
            json.dump(members, file, indent=4)

        with open(
            implement.metadata_file, "w", encoding="utf-8"
        ) as file:
            json.dump(metadata, file, indent=4)

    def read_test_data(self):
        with open(
            implement.filename, "r", encoding="utf-8"
        ) as file:
            members = json.load(file)

        with open(
            implement.metadata_file, "r", encoding="utf-8"
        ) as file:
            metadata = json.load(file)

        return members, metadata

    def make_member(self, member_id, name, amount):
        return {
            "id": member_id,
            "name": name,
            "amount": str(amount),
            "weekly_contributions": {
                "1": str(amount)
            },
            "payouts_received": "0.00"
        }

    def run_program(self, answers):
        output = StringIO()

        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                main.main()

        return output.getvalue()

    def test_register_member_and_save_to_json(self):
        output = self.run_program([
            "1",
            "yes",
            "Alice",
            "10.00",
            "5"
        ])

        members, metadata = self.read_test_data()

        self.assertIn("Member added: Alice", output)
        self.assertIn("alice", members)
        self.assertEqual(members["alice"]["name"], "Alice")
        self.assertEqual(members["alice"]["amount"], "10.00")
        self.assertEqual(
            members["alice"]["weekly_contributions"]["1"],
            "10.00"
        )
        self.assertEqual(metadata["current_week"], 1)

    def test_additional_payment_updates_amount_and_history(self):
        self.write_test_data({
            "alice": self.make_member(
                "1234567890", "Alice", "20.00"
            )
        })

        output = self.run_program([
            "3",
            "yes",
            "Alice",
            "10.00",
            "5"
        ])

        members, metadata = self.read_test_data()

        self.assertIn("Payment recorded successfully.", output)
        self.assertEqual(members["alice"]["amount"], "30.00")
        self.assertEqual(
            members["alice"]["weekly_contributions"]["1"],
            "30.00"
        )
        self.assertEqual(metadata["current_week"], 1)

    def test_payout_blocked_when_member_still_owes(self):
        self.write_test_data({
            "alice": self.make_member(
                "1234567890", "Alice", "50.00"
            ),
            "bob": self.make_member(
                "1234567891", "Bob", "30.00"
            )
        })

        output = self.run_program([
            "4",
            "5"
        ])

        members, metadata = self.read_test_data()

        self.assertIn("Payout cannot be made.", output)
        self.assertIn("Bob still owes GHS 20.00", output)
        self.assertEqual(metadata["current_week"], 1)
        self.assertEqual(metadata["payout_history"], [])
        self.assertEqual(members["alice"]["amount"], "50.00")
        self.assertEqual(members["bob"]["amount"], "30.00")

    def test_successful_payout_resets_balances_and_rotates_queue(self):
        self.write_test_data({
            "alice": self.make_member(
                "1234567890", "Alice", "50.00"
            ),
            "bob": self.make_member(
                "1234567891", "Bob", "50.00"
            )
        })

        output = self.run_program([
            "4",
            "yes",
            "5"
        ])

        members, metadata = self.read_test_data()

        self.assertIn("Payout completed successfully.", output)
        self.assertEqual(metadata["current_week"], 2)
        self.assertEqual(len(metadata["payout_history"]), 1)

        record = metadata["payout_history"][0]

        self.assertEqual(record["recipient"], "Alice")
        self.assertEqual(record["amount"], "100.00")

        # Bob should become the next recipient.
        self.assertEqual(list(members.keys()), ["bob", "alice"])

        # Balances should reset for the next week.
        for details in members.values():
            self.assertEqual(details["amount"], "0.00")
            self.assertEqual(
                details["weekly_contributions"]["2"],
                "0.00"
            )

        # Alice should have the payout recorded in her account.
        self.assertEqual(
            members["alice"]["payouts_received"],
            "100.00"
        )

    def test_invalid_menu_option(self):
        output = self.run_program([
            "9",
            "5"
        ])

        self.assertIn("Invalid option", output)
        self.assertIn("Exiting program...", output)


if __name__ == "__main__":
    unittest.main()