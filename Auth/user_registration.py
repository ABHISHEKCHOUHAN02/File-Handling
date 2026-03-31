import csv
import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

from Utilities.hash_utility import hash_password
from Utilities.jwt_utility import verify_login_token
from Utilities.validator import (
    validate_name, validate_password, validate_email, 
    validate_gender, validate_phone, validate_department, 
    validate_salary, validate_date, validate_status, ValidationError
)

from Attendance.create_record import create_new_record, apply_leave_record
from Attendance.operation_on_existing_data import (
    checkout_record,
    update_record,
    view_record,
    delete_record,
)

CSV_PATH = project_root / "storage" / "employee.csv"

def generate_emp_id():
    """Auto-generate emp_id by finding the last id and incrementing it."""
    last_id = "EMP0000"
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, mode='r', encoding='utf-8-sig') as file:
                reader = list(csv.reader(file))
                if len(reader) > 1:
                    # Get the last non-empty row
                    for row in reversed(reader):
                        if row and row[0].strip():
                            last_id = row[0].strip()
                            break
        except Exception:
            pass
    
    # Extract numeric part. If format is EMP0109, numeric part is 0109
    # If it fails, fallback to something safe
    import re
    match = re.search(r'(\d+)', last_id)
    if match:
        number = int(match.group(1))
        new_number = number + 1
        # Maintain prefix "EMP" and pad with zeros to at least 4 digits
        return f"EMP{new_number:04d}"
    else:
        return "EMP0001"

def show_after_registration_menu(emp_id, session_token=None):
    """Print all options from main.py and execute them based on command name."""
    print(f"\n--- Commands for Employee {emp_id} ---")
    print("Available Commands: check_in, check_out, view_record, apply_leave, update_record, delete_record, logout, exit")
    
    while True:
        command = input(f"\n[{emp_id}] Enter command: ").strip().lower()

        if session_token and not verify_login_token(session_token):
            print("Session expired. Please login again.")
            break
        
        if command == 'check_in':
            create_new_record(emp_id)
        elif command == 'check_out':
            checkout_record(emp_id)
        elif command == 'view_record':
            view_record(emp_id)
        elif command == 'apply_leave':
            apply_leave_record(emp_id)
        elif command == 'update_record':
            update_record(emp_id)
        elif command == 'delete_record':
            delete_record(emp_id)
        elif command == 'logout':
            session_token = None
            print("Logged out successfully.")
            break
        elif command == 'exit':
            print("Exiting. Goodbye!")
            break
        elif command == '':
            continue
        else:
            print(f"Unknown command: '{command}'. Available: check_in, check_out, view_record, apply_leave, update_record, delete_record, logout, exit ❌")

def register_user():
    print("\n--- Register New User ---")
    
    # 1. Auto-generate Employee ID
    emp_id = generate_emp_id()
    print(f"Generated Employee ID: {emp_id}")
    
    # 2. Capture and validate other details
    while True:
        try:
            first_name = validate_name(input("Enter First Name: "), "First Name")
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            last_name = validate_name(input("Enter Last Name: "), "Last Name")
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            password = validate_password(input("Enter Password (min 8 chars, 1 upper, 1 lower, 1 digit): "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            email = validate_email(input("Enter Email: "))
            # Verify if email already exists
            if os.path.exists(CSV_PATH):
                try:
                    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as file:
                        reader = csv.DictReader(file)
                        if any(row.get('email') == email for row in reader):
                            print(f"Error: User with email {email} already exists! ❌")
                            continue
                except Exception as e:
                    print(f"Warning: Error reading CSV for email validation: {e}")
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            gender = validate_gender(input("Enter Gender (Male/Female/Other): "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            phone = validate_phone(input("Enter Phone with countrycode (eg +919027384950): "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            department = validate_department(input("Enter Department -  (it, software, devops, qa, testing, data, app, cyber_security, development): "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        role = input("Enter Role: ").strip()
        if role:
            break
        print("Error: Role is required. ❌")

    while True:
        try:
            salary = validate_salary(input("Enter Salary: "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            joining_date = validate_date(input("Enter Joining Date (YYYY-MM-DD): "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        try:
            status = validate_status(input("Enter Status (Active/Inactive): "))
            break
        except ValidationError as e:
            print(f"Error: {e} ❌")

    while True:
        location = input("Enter Location: ").strip()
        if location:
            break
        print("Error: Location is required. ❌")

    # 3. Email uniqueness already checked during input loop

    # 4. Hash password
    hashed_password = hash_password(password)

    # 5. Append new record
    try:
        new_row = [
            emp_id, first_name, last_name, hashed_password, email, 
            gender, phone, department, role, salary, 
            joining_date, status, location
        ]
        
        with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
            
        print(f"\nUser {first_name} {last_name} registered successfully! ✅")
        
        # 6. Show after registration menu
        show_after_registration_menu(emp_id)
        
    except Exception as e:
        print(f"Error saving to CSV: {e} ❌")

if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        print(f"Warning: CSV file not found at {CSV_PATH}. Make sure the path is correct.")
    register_user()
