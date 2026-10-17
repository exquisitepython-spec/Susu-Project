from implement import (
                        Decimal,
                        datetime,
                        Amount)
from metadata import load_metadata
from members import load_members
from saved_data import save_data
from money import read_money
from member_id import generate_member_id





def main():
    while True:
        print(
                "\n--- SUSU MENU ---\n"
                "1. Add member\n"
                "2. List Members\n"
                "3. Update Amount\n"
                "4. Show Payout Report\n"
                "5. Exit"
                )
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                prompt = input(
                    "Do you want to add a member (yes/no): "
                ).strip().lower()
                if prompt != "yes":
                    print("Member registration cancelled.")

                else:
                    # this prevents duplication and keeps names exactly as entered
                    name = input("Enter name: ").strip()
                    member_key = name.casefold()
                    if not name:
                        print("Member name cannot be empty.")
                    else:
                        metadata = load_metadata()
                        new_members = load_members(
                            metadata["current_week"]
                        )
                        if member_key in new_members:
                            print("This member already exists.")
                        else:
                            user_amount = read_money(
                                "Enter initial contribution: GHS "
                            )
                            if user_amount < Decimal("0.00"):
                                print("Initial contribution cannot be negative.")
                            elif user_amount > Amount:
                                print(
                                    f"Initial contribution cannot exceed "
                                    f"GHS {Amount:.2f}."
                                )
                            else:
                                member_id = generate_member_id(new_members)
                                week_key = str(metadata["current_week"])
                                members = {
                                    "id": member_id,
                                    "name": name,
                                    "amount": str(user_amount),
                                    "weekly_contributions": {
                                        week_key: str(user_amount)
                                    },
                                    "payouts_received": "0.00"
                                }
                                new_members[member_key] = members
                                save_data(new_members, metadata)
                                print(f"Member added: {name}")
                                print(f"Member ID: {member_id}")
                                print(
                                    f"Initial contribution: "
                                    f"GHS {user_amount:.2f}"
                                        )
            elif choice == "2":
                metadata = load_metadata()
                new_members = load_members(metadata["current_week"])
                ###############################################################
                print("-"*40)
                print("    SUSU MEMBERS REPORT ")
                print("-"*40)
                print(f"Current contribution week: {metadata['current_week']}")
                if not new_members:
                        print("No members registered.")
                else:
                    print(   
                                f"\n{'Position':<10}"
                                f"{'Member':<20}"
                                f"{'Amount Paid':<18}"
                                f"{'Outstanding':<18}"
                            )
                    print("-" * 66)
                    for position, (key, details) in enumerate(
                                new_members.items(),
                                start=1
                            ):
                                paid = Decimal(str(details["amount"]))
                                remaining = max(Decimal("0.00"), Amount - paid)
                                print(
                                    f"{position:<10}"
                                    f"{details['name']:<20}"
                                    f"GHS {paid:<12.2f}"
                                    f"GHS {remaining:.2f}"
                                )
                    print("--"*40)
                    print("  MEMBERS STILL OWING ")
                    print("--"*30)
                    owing_members = []
                    for key, details in new_members.items():
                        paid = Decimal(str(details["amount"]))
                        
                        if paid < Amount:
                            owing_members.append(key)
                    if owing_members:
                                for key in owing_members:
                                    details = new_members[key]
                                    paid = Decimal(str(details["amount"]))
                                    remaining = Amount - paid
                                    print(
                                        f"{details['name']} owes "
                                        f"GHS {remaining:.2f}"
                                    )
                    else:
                                print("All members have completed their contributions.")
            
            elif choice == "3":
                metadata = load_metadata()
                new_members = load_members(metadata["current_week"])
                ########################################################
                print("--"*40)
                print("  UPDATE MEMBER CONTRIBUTION ")
                print("--"*40)
                if not new_members:
                    print("No members registered.")
                else:
                    update = input(
                        "Do you want to make a payment (yes/no): "
                    ).strip().lower()
                    if update != "yes":
                        print("Payment cancelled.")
                    else:
                        up_name = input("Enter member name: ").strip().casefold()
                        if up_name not in new_members:
                            print("Member not found.")
                        else:
                            details = new_members[up_name]
                            current_paid = Decimal(str(details["amount"]))
                            if current_paid >= Amount:
                                print(
                                    "This member has already completed "
                                    "the contribution for the current week."
                                )
                            else:
                                print(
                                    f"Current contribution: GHS {current_paid:.2f}"
                                )
                                print(
                                    f"Outstanding balance: "
                                    f"GHS {Amount - current_paid:.2f}"
                                )
                                add_value = read_money(
                                    "Enter payment amount: GHS "
                                )
                                if add_value <= Decimal("0.00"):
                                    print("Payment must be greater than zero.")
                                elif add_value > Amount - current_paid:
                                    print(
                                        "Payment exceeds the outstanding balance "
                                        f"of GHS {Amount - current_paid:.2f}."
                                    )
                                else:
                                    updated_amount = current_paid + add_value
                                    details["amount"] = str(updated_amount)
                                    week_key = str(metadata["current_week"])
                                    details["weekly_contributions"][week_key] = str(
                                        updated_amount
                                    )
                                    save_data(new_members, metadata)
                                    print("\nPayment recorded successfully.")
                                    print(f"Member: {details['name']}")
                                    print(
                                        f"Total paid this week: "
                                        f"GHS {updated_amount:.2f}"
                                    )
                                    print(
                                        f"Remaining balance: "
                                        f"GHS {Amount - updated_amount:.2f}"
                                    )
                
            elif choice == "4":
                metadata = load_metadata()
                new_members = load_members(metadata["current_week"])
                ########################################################
                print("--"*40)
                print("   SUSU PAYOUT REPORT   ")
                print("--"*40)
                print(f"Current week: {metadata['current_week']}")
                if not new_members:
                    print("No members found. Add members before making a payout.")
                else:
                    owing_list = []
                    overpaid_list = []
                    total = Decimal("0.00")
                    for key, details in new_members.items():
                        paid = Decimal(str(details["amount"]))
                        total += paid
                        if paid < Amount:
                            owing_list.append(key)
                        elif paid > Amount:
                            overpaid_list.append(key)

                    print("--"*40)
                    print(" CURRENT CONTRIBUTIONS ")
                    print("--"*40)
                    for key, details in new_members.items():
                        paid = Decimal(str(details["amount"]))
                        remaining = max(Decimal("0.00"), Amount - paid)
                        print(
                            f"{details['name']}: "
                            f"Paid GHS {paid:.2f}, "
                            f"Outstanding GHS {remaining:.2f}"
                        )
                    print(f"\nTotal collected: GHS {total:.2f}")

                    ###############################################3
                    print("--"*40)
                    print("   PAYOUT HISTORY  ")
                    print("--"*40)
                    if metadata["payout_history"]:
                        for record in metadata["payout_history"]:
                            print(
                                f"Week {record['week']}: "
                                f"{record['recipient']} received "
                                f"GHS {Decimal(str(record['amount'])):.2f} "
                                f"on {record['date']}"
                            )
                    else:
                        print("No payouts have been recorded yet.")
                    if owing_list:
                        print("\nPayout cannot be made.")
                        print(
                            "The following members have not completed "
                            "their contributions:"
                        )
                        for key in owing_list:
                            details = new_members[key]
                            paid = Decimal(str(details["amount"]))
                            owed = Amount - paid
                            print(
                                f"- {details['name']} still owes "
                                f"GHS {owed:.2f}"
                            )
                    elif overpaid_list:
                        print("\nPayout cannot be made.")
                        print("The following records need to be checked:")
                        for key in overpaid_list:
                            print(f"- {new_members[key]['name']}")
                    else:
                        firstmember = next(iter(new_members))
                        print("\nAll members have completed their contributions.")
                        print(f"Next recipient: {new_members[firstmember]['name']}")
                        print(f"Total payout: GHS {total:.2f}")
                        do_payout = input(
                            "Do you want to make this payout (yes/no): "
                        ).strip().lower()
                        if do_payout == "yes":
                            recipient = new_members[firstmember]
                            current_week = metadata["current_week"]
                            previous_payouts = Decimal(
                                str(recipient.get("payouts_received", "0.00"))
                            )
                            recipient["payouts_received"] = str(
                                previous_payouts + total
                            )
                            payout_record = {
                                "week": current_week,
                                "recipient": recipient["name"],
                                "recipient_id": recipient["id"],
                                "amount": str(total),
                                "date": datetime.now().astimezone().isoformat(
                                    timespec="seconds"
                                )
                            }
                            metadata["payout_history"].append(payout_record)
                            for details in new_members.values():
                                details["amount"] = "0.00"
                            move_member = new_members.pop(firstmember)
                            new_members[firstmember] = move_member
                            metadata["current_week"] += 1
                            next_week_key = str(metadata["current_week"])
                            for details in new_members.values():
                                details["weekly_contributions"][next_week_key] = (
                                    "0.00"
                                )
                            save_data(new_members, metadata)

                            print("--"*40)
                            print("   PAYOUT RECEIPT   ")
                            print("--"*40)
                            ##############################################
                            print(f"Recipient: {recipient['name']}")
                            print(f"Member ID: {recipient['id']}")
                            print(f"Week completed: {current_week}")
                            print(f"Amount paid out: GHS {total:.2f}")
                            print("Payout history updated.")
                            print("Contribution balances reset.")
                            print("Payout queue rotated.")
                            print(
                                f"Contribution Week {metadata['current_week']} "
                                "has started."
                            )
                            print("Payout completed successfully.")
                        else:
                            print("Payout cancelled. No changes were made.")

            elif choice == '5':
                print("Exiting program...")
                break

            else:
                print("Invalid option. Choose a number from 1 to 5")
        except (ValueError,OSError,KeyError,TypeError) as error:
            print(f"Error: {error}")
                
if __name__ == "__main__":
    main()