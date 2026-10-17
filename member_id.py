import string
import secrets

def generate_member_id(members):
    existing_ids = {
        details["id"]
        for details in members.values()
    }
    while True:
        member_id = "".join(
            secrets.choice(string.digits)
            for _ in range(10)
        )
        if member_id not in existing_ids:
            return member_id