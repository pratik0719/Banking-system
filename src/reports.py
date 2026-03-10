from datetime import datetime

from storage import load_transactions, load_customers
from validation import input_date


def _parse_date(value):
    # Parse YYYY-MM-DD string into date object; return None if invalid.
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def print_statement(s, account_no, start_date=None, end_date=None):
    # Print account statement for a date range with transaction totals.
    # Ask for dates interactively when not provided by caller.
    if start_date is None:
        start_date = input_date("Start date (YYYY-MM-DD): ")
    if end_date is None:
        end_date = input_date("End date (YYYY-MM-DD): ")
    if end_date < start_date:
        print("End date cannot be earlier than start date.")
        return

    customers = load_customers(s)
    customer = None
    for c in customers:
        if c.get("account_no") == account_no:
            customer = c
            break

    if not customer:
        print("Account not found.")
        return

    transactions = load_transactions(s)
    filtered = []
    total_deposit = 0.0
    total_withdraw = 0.0
    for t in transactions:
        # Skip transactions for other accounts.
        if t.get("account_no") != account_no:
            continue
        t_date = _parse_date(t.get("date", ""))
        if not t_date:
            continue
        if start_date <= t_date <= end_date:
            filtered.append(t)
            amount = float(t.get("amount", "0") or 0)
            # Sum deposits and withdrawals separately for reporting.
            if t.get("type") == "DEPOSIT":
                total_deposit += amount
            elif t.get("type") == "WITHDRAW":
                total_withdraw += amount

    print("\n--- Statement of Account ---")
    print(f"Name: {customer.get('name')}")
    print(f"Account No: {account_no}")
    print(f"Account Type: {customer.get('account_type')}")
    print(f"Period: {start_date} to {end_date}")
    print("Date       | Type     | Amount  | Balance After | Note")
    print("-" * 60)
    if not filtered:
        print("No transactions in this period.")
    else:
        for t in filtered:
            print(
                f"{t.get('date'):10} | {t.get('type'):8} | {t.get('amount'):7} | "
                f"{t.get('balance_after'):13} | {t.get('note')}"
            )
    print("-" * 60)
    print(f"Total Deposits: {total_deposit}")
    print(f"Total Withdrawals: {total_withdraw}")
    print("--- End of Statement ---\n")
