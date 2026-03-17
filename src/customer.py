#pratik_dijan_rohan_dorje
#Np071181_Np071314_Np071204_Np071364
from datetime import datetime

from storage import load_customers, save_customers, append_transaction
from validation import input_non_empty, input_float
from reports import print_statement


def _find_customer_by_account(customers, account_no):
    # Return customer record for given account number, else None.
    for c in customers:
        if c.get("account_no") == account_no:
            return c
    return None


def _get_min_balance(s, account_type):
    # Return minimum required balance based on account type.
    if account_type == "S":
        return s["min_balance_savings"]
    return s["min_balance_current"]


def _deposit(s, account_no):
    # Deposit money to customer account and log transaction.
    amount = input_float("Deposit Amount: ", min_val=1)
    customers = load_customers(s)
    customer = _find_customer_by_account(customers, account_no)
    if not customer:
        print("Customer not found.")
        return
    balance = float(customer.get("balance", "0") or 0)
    balance += amount
    customer["balance"] = str(balance)
    save_customers(s, customers)

    # Write transaction entry for audit/history.
    today = datetime.now().strftime("%Y-%m-%d")
    append_transaction(
        s,
        {
            "account_no": account_no,
            "date": today,
            "type": "DEPOSIT",
            "amount": str(amount),
            "balance_after": str(balance),
            "note": "Customer deposit",
        },
    )
    print(f"Deposit successful. New balance: {balance}")


def _withdraw(s, account_no):
    # Withdraw money while enforcing minimum-balance rule.
    amount = input_float("Withdrawal Amount: ", min_val=1)
    customers = load_customers(s)
    customer = _find_customer_by_account(customers, account_no)
    if not customer:
        print("Customer not found.")
        return
    balance = float(customer.get("balance", "0") or 0)
    min_balance = _get_min_balance(s, customer.get("account_type"))
    if balance - amount < min_balance:
        print("Withdrawal denied. Minimum balance requirement not met.")
        return
    balance -= amount
    customer["balance"] = str(balance)
    save_customers(s, customers)

    # Write transaction entry for audit/history.
    today = datetime.now().strftime("%Y-%m-%d")
    append_transaction(
        s,
        {
            "account_no": account_no,
            "date": today,
            "type": "WITHDRAW",
            "amount": str(amount),
            "balance_after": str(balance),
            "note": "Customer withdrawal",
        },
    )
    print(f"Withdrawal successful. New balance: {balance}")


def _reset_password(s, account_no):
    # Change customer password after verifying current password.
    customers = load_customers(s)
    customer = _find_customer_by_account(customers, account_no)
    if not customer:
        print("Customer not found.")
        return
    current = input_non_empty("Current Password: ")
    if current != customer.get("password"):
        print("Incorrect password.")
        return
    new_pw = input_non_empty("New Password: ")
    customer["password"] = new_pw
    save_customers(s, customers)
    print("Password updated.")


def customer_menu(s, customer_user):
    # Run customer menu loop until logout.
    account_no = customer_user.get("account_no")
    while True:
        print("\n=== Customer Menu ===")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Reset Password")
        print("4. Statement of Account")
        print("0. Logout")
        choice = input_non_empty("Select option: ")
        if choice == "1":
            _deposit(s, account_no)
        elif choice == "2":
            _withdraw(s, account_no)
        elif choice == "3":
            _reset_password(s, account_no)
        elif choice == "4":
            print_statement(s, account_no)
        elif choice == "0":
            return
        else:
            print("Invalid option.")
