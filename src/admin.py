from storage import load_staff, save_staff, load_customers
from validation import input_non_empty, input_email
from reports import print_statement


def _next_staff_id(staff_records):
    # Return the next staff ID in the format S0001, S0002, ...
    max_id = 0
    for s in staff_records:
        # Read existing ID and validate format before converting to number.
        sid = s.get("staff_id", "")
        if sid.startswith("S") and sid[1:].isdigit():
            num = int(sid[1:])
            if num > max_id:
                max_id = num
    # Increment the largest number found and left-pad with zeros.
    return f"S{str(max_id + 1).zfill(1)}"


def _create_staff(s):
    # Create and store a new staff account.
    staff = load_staff(s)
    staff_id = _next_staff_id(staff)
    name = input_non_empty("Staff Name: ")
    email = input_email("Staff Email: ")
    password = input("Password (leave blank for default): ").strip()
    if not password:
        # Use  default password when user leaves it empty.
        password = s["default_staff_password"]

    staff.append(
        {
            "staff_id": staff_id,
            "name": name,
            "email": email,
            "password": password,
        }
    )
    save_staff(s, staff)
    print(f"Staff account created. Staff ID: {staff_id}")


def _view_staff(s):
    # Display all staff records.
    staff = load_staff(s)
    print("\n--- Staff Details ---")
    for st in staff:
        print(f"{st.get('staff_id')} | {st.get('name')} | {st.get('email')}")
    if not staff:
        print("No staff records.")


def _view_customers(s):
    # Display all customer records.
    customers = load_customers(s)
    print("\n--- Customer Details ---")
    for c in customers:
        print(
            f"{c.get('customer_id')} | {c.get('name')} | {c.get('email')} | "
            f"{c.get('account_no')} | {c.get('account_type')} | {c.get('balance')}"
        )
    if not customers:
        print("No customer records.")


def _search_by_id_or_email(s):
    # Search staff and customers by ID or email.
    value = input_non_empty("Enter ID or Email to search: ")
    staff = load_staff(s)
    customers = load_customers(s)
    found = False
    for st in staff:
        if st.get("staff_id") == value or st.get("email") == value:
            print(f"Staff: {st.get('staff_id')} | {st.get('name')} | {st.get('email')}")
            found = True
    for c in customers:
        if c.get("customer_id") == value or c.get("email") == value:
            print(
                f"Customer: {c.get('customer_id')} | {c.get('name')} | {c.get('email')} | "
                f"{c.get('account_no')}"
            )
            found = True
    if not found:
        print("No matching record found.")


def admin_menu(s):
    # Run the admin menu until the admin logs out.
    while True:
        print("\n=== Admin Menu ===")
        print("1. Create Staff Account")
        print("2. View Staff")
        print("3. View Customers")
        print("4. Search by ID or Email")
        print("5. Generate Customer Statement")
        print("0. Logout")
        choice = input_non_empty("Select option: ")
        if choice == "1":
            _create_staff(s)
        elif choice == "2":
            _view_staff(s)
        elif choice == "3":
            _view_customers(s)
        elif choice == "4":
            _search_by_id_or_email(s)
        elif choice == "5":
            account_no = input_non_empty("Enter Account Number: ")
            print_statement(s, account_no)
        elif choice == "0":
            return
        else:
            print("Invalid option.")
