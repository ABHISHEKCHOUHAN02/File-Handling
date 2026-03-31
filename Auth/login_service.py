import csv
import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

from Utilities.hash_utility import verify_password
from Utilities.jwt_utility import create_login_token
from .user_registration import show_after_registration_menu

CSV_PATH = project_root / "storage" / "employee.csv"


def login_user():
    print("\n--- User Login ---")

    emp_id = input("Enter Employee ID: ").strip()
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    normalized_emp_id = emp_id.lower()
    normalized_email = email.lower()

    if not os.path.exists(CSV_PATH):
        print(f"Error: Employee data file not found at {CSV_PATH} X")
        return

    try:
        with open(CSV_PATH, mode="r", encoding="utf-8-sig") as file:
            reader_list = list(csv.reader(file))
            if not reader_list:
                print("Error: Employee data is empty X")
                return

            matched_user = None
            for row in reader_list[1:]:
                if len(row) > 4:
                    curr_emp_id = row[0].strip().lower()
                    curr_email = row[4].strip().lower()
                    if curr_emp_id == normalized_emp_id and curr_email == normalized_email:
                        matched_user = row
                        break

            if not matched_user:
                print(f"\nNo user found with ID {emp_id} and email {email}. X")
                return

            stored_hash = matched_user[3].strip()
            if verify_password(password, stored_hash):
                login_token = create_login_token(matched_user[0].strip(), matched_user[4].strip())
                print(f"\nLogin successful! Welcome, {matched_user[1]} {matched_user[2]}!")
                show_after_registration_menu(matched_user[0].strip(), login_token)
                return

            print("\nInvalid password! X")

    except Exception as e:
        print(f"Error during login: {e} X")


if __name__ == "__main__":
    login_user()
