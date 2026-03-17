from datetime import datetime

from storage import load_staff, save_staff, load_customers, save_customers, append_transaction
from validation import (
    input_non_empty,
    input_email,
    input_phone,
    input_account_type,
    input_float,
    confirm,
)
from reports import print_statement


def _next_account_no(customers):
    # Return next account number in the format AC001, AC002, ...
    max_no = 0
    for c in customers:
        # Validate account number format before numeric comparison.
        acc = c.get("account_no", "")
        if acc.startswith("AC") and acc[2:].isdigit():
            num = int(acc[2:])
            if num > max_no:
                max_no = num
    return f"AC{str(max_no + 1).zfill(3)}"


def _register_customer(s):
    # Register a new customer and create initial deposit transaction.
    customers = load_customers(s)
    customer_id = input_non_empty("Customer ID: ")
    # Reject duplicate customer IDs.
    for c in customers:
        if c.get("customer_id") == customer_id:
            print("Customer ID already exists.")
            return
    name = input_non_empty("Customer Name: ")
    email = input_email("Email: ")
    for c in customers:
        if c.get("email") == email:
            print("Email already exists.")
            return
    phone = input_phone("Phone: ")
    address = input_non_empty("Address: ")
    account_type = input_account_type("Account Type (S/C): ")

    min_balance = s["min_balance_savings"] if account_type == "S" else s["min_balance_current"]
    initial_deposit = input_float(f"Initial Deposit (min {min_balance}): ", min_val=min_balance)

    account_no = _next_account_no(customers)
    password = s["default_customer_password"]
    created_date = datetime.now().strftime("%Y-%m-%d")

    customers.append(
        {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "account_no": account_no,
            "account_type": account_type,
            "balance": str(initial_deposit),
            "password": password,
            "created_date": created_date,
        }
    )
    save_customers(s, customers)
    # Log initial deposit in the transaction history.
    append_transaction(
        s,
        {
            "account_no": account_no,
            "date": created_date,
            "type": "DEPOSIT",
            "amount": str(initial_deposit),
            "balance_after": str(initial_deposit),
            "note": "Initial deposit",
        },
    )
    print(f"Customer registered. Account Number: {account_no} Default Password: {password}")


def _update_staff(s):
    # Update an existing staff member's email and/or password.
    staff = load_staff(s)
    staff_id = input_non_empty("Enter Staff ID to update: ")
    target = None
    for st in staff:
        if st.get("staff_id") == staff_id:
            target = st
            break
    if not target:
        print("Staff not found.")
        return
    print("You can update email and password only.")
    if confirm("Update email?"):
        target["email"] = input_email("New Email: ")
    if confirm("Update password?"):
        target["password"] = input_non_empty("New Password: ")
    save_staff(s, staff)
    print("Staff record updated.")


def _update_customer(s):
    # Update an existing customer's contact details.
    customers = load_customers(s)
    account_no = input_non_empty("Enter Customer Account Number: ")
    target = None
    for c in customers:
        if c.get("account_no") == account_no:
            target = c
            break
    if not target:
        print("Customer not found.")
        return
    print("You can update email, phone, and address only.")
    if confirm("Update email?"):
        target["email"] = input_email("New Email: ")
    if confirm("Update phone?"):
        target["phone"] = input_phone("New Phone: ")
    if confirm("Update address?"):
        target["address"] = input_non_empty("New Address: ")
    save_customers(s, customers)
    print("Customer record updated.")


def staff_menu(s):
    # Run staff menu loop until logout.
    while True:
        print("\n=== Staff Menu ===")
        print("1. Register Customer")
        print("2. Update Staff Details")
        print("3. Update Customer Details")
        print("4. Generate Customer Statement")
        print("0. Logout")
        choice = input_non_empty("Select option: ")
        if choice == "1":
            _register_customer(s)
        elif choice == "2":
            _update_staff(s)
        elif choice == "3":
            _update_customer(s)
        elif choice == "4":
            account_no = input_non_empty("Enter Account Number: ")
            print_statement(s, account_no)
        elif choice == "0":
            return
        else:
            print("Invalid option.")
