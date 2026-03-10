import os

from login import login_flow
from admin import admin_menu
from staff import staff_menu
from customer import customer_menu
from storage import ensure_files_and_defaults


def settings():
    # Build and return application settings and file paths.
    # Resolve project/data paths relative to this file location.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), "data")
    return {
        "data_dir": data_dir,
        "admins_file": os.path.join(data_dir, "admins.txt"),
        "staff_file": os.path.join(data_dir, "staff.txt"),
        "customers_file": os.path.join(data_dir, "customers.txt"),
        "transactions_file": os.path.join(data_dir, "transactions.txt"),
        "min_balance_savings": 1000.0,
        "min_balance_current": 1500.0,
        "default_customer_password": "cust123",
        "default_staff_password": "staff123",
    }


def main():
    # Run the top-level login loop and route users by role.
    s = settings()
    ensure_files_and_defaults(s)

    # Track consecutive failed logins; terminate after three failures.
    attempts = 0
    while True:
        role, user = login_flow(s)
        if role is None:
            print("Exiting system.")
            return
        if user is None:
            attempts += 1
            print(f"Login failed. Attempts remaining: {max(0, 3 - attempts)}")
            if attempts >= 3:
                print("Too many failed attempts. System terminated.")
                return
            continue

        attempts = 0
        if role == "admin":
            admin_menu(s)
        elif role == "staff":
            staff_menu(s)
        elif role == "customer":
            customer_menu(s, user)
        else:
            print("Unknown role.")


if __name__ == "__main__":
    main()
