from datetime import datetime


def input_non_empty(prompt):
    # Prompt until a non-empty value is entered.
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def input_float(prompt, min_val=None):
    # Prompt for floating-point number and optional minimum bound.
    while True:
        value = input(prompt).strip()
        try:
            num = float(value)
        except ValueError:
            print("Enter a valid amount.")
            continue
        if min_val is not None and num < min_val:
            print(f"Amount must be at least {min_val}.")
            continue
        return num


def input_email(prompt):
    # Prompt until basic email format is entered.
    while True:
        email = input_non_empty(prompt)
        if "@" in email and "." in email:
            return email
        print("Enter a valid email.")


def input_phone(prompt):
    # Prompt until a phone-like value with at least 7 digits is entered.
    while True:
        phone = input_non_empty(prompt)
        # Count digits while allowing symbols/spaces in user input.
        digits = "".join([c for c in phone if c.isdigit()])
        if len(digits) == 10:
            return phone
        print("Enter a valid phone number.")


def input_account_type(prompt):
    # Prompt until account type is S (savings) or C (current).
    while True:
        acc = input_non_empty(prompt).upper()
        if acc in ["S", "C"]:
            return acc
        print("Enter S for Savings or C for Current.")


def input_date(prompt):
    # Prompt until valid date in YYYY-MM-DD format is entered.
    while True:
        value = input_non_empty(prompt)
        try:
            dt = datetime.strptime(value, "%Y-%m-%d").date()
            return dt
        except ValueError:
            print("Enter date in YYYY-MM-DD format.")


def confirm(prompt):
    # Prompt for Y/N confirmation and return boolean result.
    while True:
        value = input_non_empty(prompt + " (Y/N): ").upper()
        if value in ["Y", "N"]:
            return value == "Y"
        print("Enter Y or N.")
