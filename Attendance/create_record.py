from data_reader import read_data, write_data, generate_attendance_id
from .attendance_validator import (
    validate_employee_id, validate_date, validate_time, validate_time_order,
    calculate_status, calculate_working_hours, validate_leave
)
from Utilities.logger_config import get_logger
from Utilities.validator import ValidationError

logger = get_logger(__name__)
import datetime

def create_new_record(emp_id):
    print("\n--- Create New Attendance Record ---")
    logger.info("Initiating new attendance record creation")
    data = read_data()
    att_id = generate_attendance_id(data)
    

    #emp_id = input("Enter Employee ID (e.g., EMP0001): ").strip()
    try:
        validate_employee_id(emp_id)
    except ValidationError as e:
        logger.warning(f"Validation Error during record creation: {e}")
        print(f"Validation Error: {e}")
        return

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    # Check if employee is already actively checked in without checking out
    for r in data:
        if r.get("employee_id") == emp_id and r.get("date") == date_str:
            if not r.get("check_out_time") or str(r.get("check_out_time")).strip() == "":
                logger.warning(f"Employee {emp_id} attempted to check in but is already checked in.")
                print(f"Employee {emp_id} is already checked in for today! Please check out first.")
                return

    check_in_str = now.strftime("%H:%M")
    
    dt = now.date()
    check_in_time = now.time()
    check_out_str = ""
    check_out_time = None
    print(f"Generated Attendance ID: {att_id}")
    print(f"Date auto-filled: {date_str}")
    print(f"Check-in Time auto-filled: {check_in_str}")

    status_str = "Present"
    final_status = calculate_status(dt, check_in_time, status_str)

    leave_type = ""
    leave_reason = ""
    
    working_hours = 0.0

    new_row = {
        "attendance_id": att_id,
        "employee_id": emp_id,
        "date": date_str,
        "check_in_time": check_in_str,
        "check_out_time": check_out_str,
        "status": final_status,
        "working_hours": str(working_hours) if working_hours > 0 else "0",
        "leave_type": leave_type,
        "leave_reason": leave_reason
    }

    logger.debug(f"Creating record: {new_row}")
    data.append(new_row)
    write_data(data)
    logger.info(f"Successfully created record for Employee ID: {emp_id}")
    print("Record created and saved successfully to attendance.csv!")

def apply_leave_record(emp_id):
    print("\n--- Apply for Leave ---")
    logger.info("Initiating leave application")
    data = read_data()
    att_id = generate_attendance_id(data)
    print(f"Generated Attendance ID: {att_id}")

    #emp_id = input("Enter Employee ID (e.g., EMP0001): ").strip()
    try:
        validate_employee_id(emp_id)
    except ValidationError as e:
        logger.warning(f"Validation Error during leave application: {e}")
        print(f"Validation Error: {e}")
        return

    date_str = input("Enter Future Date for Leave (YYYY-MM-DD): ").strip()
    try:
        dt = validate_date(date_str, allow_future=True)
    except ValidationError as e:
        logger.warning(f"Validation Error during leave application: {e}")
        print(f"Validation Error: {e}")
        return

    status_str = input("Enter Status (Leave/Half-Day): ").strip()
    if status_str not in ["Leave", "Half-Day"]:
        print("Status must be 'Leave' or 'Half-Day'.")
        return

    leave_type = input("Enter Leave Type: ").strip()
    leave_reason = input("Enter Leave Reason: ").strip()
    try:
        validate_leave(status_str, leave_type, leave_reason)
    except ValidationError as e:
        logger.warning(f"Validation Error during leave application: {e}")
        print(f"Validation Error: {e}")
        return

    new_row = {
        "attendance_id": att_id,
        "employee_id": emp_id,
        "date": date_str,
        "check_in_time": "",
        "check_out_time": "",
        "status": status_str,
        "working_hours": "0",
        "leave_type": leave_type,
        "leave_reason": leave_reason
    }

    logger.debug(f"Creating leave record: {new_row}")
    data.append(new_row)
    write_data(data)
    logger.info(f"Successfully created leave record for Employee ID: {emp_id}")
    print("Leave application created and saved successfully!")
