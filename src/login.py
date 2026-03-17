#pratik_dijan_rohan_dorje
#Np071181_Np071314_Np071204_Np071364

from storage import load_admins, load_staff, load_customers
from validation import input_non_empty


def _find_by_id_or_email(records, id_key, email_key, value):
    # Return first record where ID or email matches the given value.
    value_lower = value.strip().lower()
    for r in records:
        if r.get(id_key, "").lower() == value_lower:
            return r
        if r.get(email_key, "").lower() == value_lower:
            return r
    return None


def _authenticate_admin(s):
    # Authenticate an admin by ID/email and password.
    user_id = input_non_empty("Admin ID or Email: ")
    password = input_non_empty("Password: ")
    admins = load_admins(s)
    admin = _find_by_id_or_email(admins, "admin_id", "email", user_id)
    if admin and admin.get("password") == password:
        return admin
    return None


def _authenticate_staff(s):
    # Authenticate a staff user by ID/email and password.
    user_id = input_non_empty("Staff ID or Email: ")
    password = input_non_empty("Password: ")
    staff = load_staff(s)
    staff_user = _find_by_id_or_email(staff, "staff_id", "email", user_id)
    if staff_user and staff_user.get("password") == password:
        return staff_user
    return None


def _authenticate_customer(s):
    # Authenticate a customer by account number and password.
    account_no = input_non_empty("Account Number: ")
    password = input_non_empty("Password: ")
    customers = load_customers(s)
    for c in customers:
        if c.get("account_no") == account_no and c.get("password") == password:
            return c
    return None


def login_flow(s):
    # Show login menu and return (role, user_record).
    print("\n=== Banking Service System ===")
    print("1. Admin Login")
    print("2. Staff Login")
    print("3. Customer Login")
    print("0. Exit")
    choice = input_non_empty("Select option: ")
    if choice == "0":
        return None, None
    if choice == "1":
        return "admin", _authenticate_admin(s)
    if choice == "2":
        return "staff", _authenticate_staff(s)
    if choice == "3":
        return "customer", _authenticate_customer(s)
    print("Invalid option.")
    return "invalid", None
