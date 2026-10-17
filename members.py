import os
import json
from decimal import Decimal, InvalidOperation
import implement


def load_members(current_week):
    if not os.path.exists(implement.filename):
        return {}
    try:
        with open(implement.filename, "r", encoding="utf-8") as file:
            members = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{implement.filename} contains invalid JSON. "
            "Correct the file before continuing."
        ) from error

    except OSError as error:
        raise ValueError(
            f"Couldn't read {implement.filename}: {error}"
        ) from error
    
    if not isinstance(members, dict):
        raise ValueError("The members file has an invalid structure.")
    
    week_key = str(current_week)
    for key, details in members.items():
        if not isinstance(details, dict):
            raise ValueError(f"Invalid member record for {key}.")
        details.setdefault("id", "")
        details.setdefault("name", key)
        details.setdefault("payouts_received", "0.00")
        try:
            amount = Decimal(str(details.get("amount", "0.00")))
            if not amount.is_finite() or amount < 0:
                raise ValueError(
                    f"Invalid contribution amount for {key}."
                )
            amount = amount.quantize(Decimal("0.01"))
        except InvalidOperation as error:
            raise ValueError(
                f"Invalid contribution amount for {key}."
            ) from error
        details["amount"] = str(amount)
        weekly_contributions = details.get("weekly_contributions")

        if weekly_contributions is None:
            weekly_contributions = {week_key: str(amount)}

        if not isinstance(weekly_contributions, dict):
            raise ValueError(
                f"Invalid weekly contribution records for {key}."
            )
        '''weekly_contributions.setdefault(week_key, str(amount))
                details["weekly_contributions"] = weekly_contributions'''
        weekly_contributions[week_key] = str(amount)
        details["weekly_contributions"]= weekly_contributions
        try:
            payouts_received = Decimal(
                str(details["payouts_received"])
            )
            if not payouts_received.is_finite() or payouts_received < 0:
                raise ValueError(
                    f"Invalid payout record for {key}."
                )
            details["payouts_received"] = str(
                payouts_received.quantize(Decimal("0.01"))
            )
        except InvalidOperation as error:
            raise ValueError(
                f"Invalid payout record for {key}."
            ) from error
    return members
