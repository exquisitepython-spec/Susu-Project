from decimal import Decimal,InvalidOperation
def read_money(prompt):
    while True:
        try:
            value = Decimal(input(prompt).strip())
            if not value.is_finite():
                print("Enter a valid finite monetary amount.")
                continue

            if value != value.quantize(Decimal("0.01")):
                print("Enter an amount with no more than two decimal places.")
                continue
            return value
        
        except (InvalidOperation,ValueError):
            print("Enter a valid numerical amount.")
