import os


def _read_lines(path):
    # Read non-empty stripped lines from a text file.
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _write_lines(path, lines):
    # Write all lines to a text file, one line per list item.
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def _append_line(path, line):
    # Append a single line to a text file.
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _load_records(path, fields):
    # Load pipe-delimited file rows into list of dictionaries.
    records = []
    normalized_fields = [f.strip().lower() for f in fields]
    for line in _read_lines(path):
        parts = line.split("|")
        normalized_parts = [p.strip().lower() for p in parts]
        # Skip optional header row if it matches the field names.
        if normalized_parts == normalized_fields:
            continue
        # Skip malformed rows with wrong column count.
        if len(parts) != len(fields):
            continue
        record = {}
        for i in range(len(fields)):
            record[fields[i]] = parts[i]
        records.append(record)
    return records


def _save_records(path, fields, records, include_header=False):
    # Save list of dictionaries as pipe-delimited rows.
    lines = []
    if include_header:
        lines.append("|".join(fields))
    for r in records:
        parts = []
        for f in fields:
            parts.append(str(r.get(f, "")))
        lines.append("|".join(parts))
    _write_lines(path, lines)


def ensure_files_and_defaults(s):
    # Create required files and seed a default admin if none exists.
    os.makedirs(s["data_dir"], exist_ok=True)
    for key in ["admins_file", "staff_file", "customers_file", "transactions_file"]:
        if not os.path.exists(s[key]):
            _write_lines(s[key], [])

    admins = load_admins(s)
    if not admins:
        default_admin = {
            "admin_id": "A001",
            "name": "Admin",
            "email": "admin@bank.com",
            "password": "admin123",
        }
        save_admins(s, [default_admin])


def load_admins(s):
    # Load admin records.
    fields = ["admin_id", "name", "email", "password"]
    return _load_records(s["admins_file"], fields)


def save_admins(s, records):
    # Save admin records.
    fields = ["admin_id", "name", "email", "password"]
    _save_records(s["admins_file"], fields, records)


def load_staff(s):
    # Load staff records.
    fields = ["staff_id", "name", "email", "password"]
    return _load_records(s["staff_file"], fields)


def save_staff(s, records):
    # Save staff records.
    fields = ["staff_id", "name", "email", "password"]
    _save_records(s["staff_file"], fields, records)


def load_customers(s):
    # Load customer records.
    fields = [
        "customer_id",
        "name",
        "email",
        "phone",
        "address",
        "account_no",
        "account_type",
        "balance",
        "password",
        "created_date",
    ]
    return _load_records(s["customers_file"], fields)


def save_customers(s, records):
    # Save customer records.
    fields = [
        "customer_id",
        "name",
        "email",
        "phone",
        "address",
        "account_no",
        "account_type",
        "balance",
        "password",
        "created_date",
    ]
    _save_records(s["customers_file"], fields, records, include_header=True)


def load_transactions(s):
    # Load transaction records.
    fields = ["account_no", "date", "type", "amount", "balance_after", "note"]
    return _load_records(s["transactions_file"], fields)


def append_transaction(s, record):
    # Append one transaction record to the transaction file.
    line = "|".join(
        [
            str(record.get("account_no", "")),
            str(record.get("date", "")),
            str(record.get("type", "")),
            str(record.get("amount", "")),
            str(record.get("balance_after", "")),
            str(record.get("note", "")),
        ]
    )
    _append_line(s["transactions_file"], line)
