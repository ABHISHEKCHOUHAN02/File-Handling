from data_reader import read_data, write_data
from .attendance_validator import (
    validate_employee_id, validate_date, validate_time, validate_time_order,
    calculate_status, calculate_working_hours, validate_leave
)
import datetime
from data_reader import FIELDNAMES
from Utilities.logger_config import get_logger
from Utilities.validator import ValidationError

logger = get_logger(__name__)

def update_record(emp_id):
    print("\n--- Update Attendance Record ---")
    logger.info("Initiating attendance record update")
    #emp_id = input("Enter Employee ID to update: ").strip()
    data = read_data()
    
    matching_records = [r for r in data if r["employee_id"] == emp_id]
    if not matching_records:
        logger.warning(f"No records found for Employee ID: {emp_id} to update")
        print("No records found for that Employee ID.")
        return
    
    print("Found records:")
    for r in matching_records:
        print(f"ID: {r['attendance_id']}, Date: {r['date']}, Status: {r['status']}")
        
    att_id = input("Enter the attendance_id of the record you want to update: ").strip()
    
    record = None
    for r in data:
        if r["attendance_id"] == att_id and r["employee_id"] == emp_id:
            record = r
            break
            
    if not record:
        print("Invalid attendance_id for this employee.")
        return
        
    column = input(f"Enter column to update ({', '.join(FIELDNAMES)}): ").strip()
    if record["status"] == "Leave" and column == "check_in_time" or column == "check_out_time":
            print("You cannot edit check_in_time as status is on leave")
            return
    if column not in FIELDNAMES:
        print("Invalid column.")
        return
    if column in ["attendance_id", "employee_id"]:
        print("Cannot update ID fields directly through this menu.")
        return
        
    new_value = input(f"Enter new value for {column}: ").strip()
    
    try:
        if column == "date":
            dt = validate_date(new_value)
        elif column == "check_in_time":
            
            validate_time(new_value, "check_in_time")
        elif column == "check_out_time":
            
            validate_time(new_value, "check_out_time")
        elif column == "status":
            pass # we could add forced validation here
    except ValidationError as e:
        logger.warning(f"Validation Error during record update (Employee ID: {emp_id}): {e}")
        print(f"Validation Error: {e}")
        return
        
    record[column] = new_value
    if column == "status" and new_value == "Absent":
        if record["check_in_time"] is not None:
            print("Cannot change column to Absent as check_in_time is not None")
            return
    # Optional logic to re-calculate working hours and status if dates/times change
    if column in ["date", "check_in_time", "check_out_time", "status"]:
        try:
            dt_obj = validate_date(record["date"]) if record["date"] else None
            ci_obj = validate_time(record["check_in_time"]) if record["check_in_time"] else None
            co_obj = validate_time(record["check_out_time"]) if record["check_out_time"] else None
            wh = calculate_working_hours(dt_obj, ci_obj, co_obj)
            record["working_hours"] = str(wh) if wh > 0 else "0"
            calc_status = calculate_status(dt_obj, ci_obj, record["status"])
            record["status"] = calc_status
        except ValidationError:
            pass
    
             
    logger.debug(f"Updated record {att_id} for Employee ID {emp_id}: set {column} to {new_value}")
    write_data(data)
    logger.info(f"Successfully updated record {att_id} for Employee ID: {emp_id}")
    print("Record updated successfully.")

def view_record(emp_id):
    print("\n--- View Attendance Record ---")
    logger.info("Initiating view attendance record")
    #emp_id = input("Enter Employee ID to view: ").strip()
    data = read_data()
    matching_records = [r for r in data if r["employee_id"] == emp_id]
    
    if not matching_records:
        logger.warning(f"No attendance records founpdate_recordd for Employee ID: {emp_id} to view")
        print("No attendance records found.")
        return
        
    print(f"\nAttendance for {emp_id}:")
    for r in matching_records:
        print(f"[{r['attendance_id']}] Date: {r['date']} | In: {r['check_in_time']} | Out: {r['check_out_time']} | Status: {r['status']} | Hrs: {r['working_hours']}")

def delete_record(emp_id):
    print("\n--- Delete Attendance Record ---")
    logger.info("Initiating delete attendance record")
    
    data = read_data()
    matching_records = [r for r in data if r["employee_id"] == emp_id]
    
    if not matching_records:
        logger.warning(f"No attendance records founpdate_recordd for Employee ID: {emp_id} to view")
        print("No attendance records found.")
        return
        
    print(f"\nAttendance for {emp_id}:")
    for r in matching_records:
        print(f"[{r['attendance_id']}] Date: {r['date']} | In: {r['check_in_time']} | Out: {r['check_out_time']} | Status: {r['status']} | Hrs: {r['working_hours']}")

    att_id = input("Enter Attendance ID to delete: ").strip()
    new_data = [r for r in data if r["attendance_id"] != att_id]
    
    if len(new_data) == len(data):
        logger.warning(f"Attendance ID {att_id} not found for deletion")
        print("Attendance ID not found.")
    else:
        logger.debug(f"Deleting record {att_id}")
        write_data(new_data)
        logger.info(f"Successfully deleted record {att_id}")
        print("Record deleted successfully.")

def checkout_record(emp_id):
    
    logger.info("Initiating employee checkout")
    #emp_id = input("Enter Employee ID to check out: ").strip()
    data = read_data()
    
    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    check_out_str = now.strftime("%H:%M")
    
    # find their record for today
    record = None
    for r in data:
        if r.get("employee_id") == emp_id and r.get("date") == today_str:
            record = r
            # If we find an active check-in (no checkout time), break immediately
            if not r.get("check_out_time") or str(r.get("check_out_time")).strip() == "":
                break
            
    if not record:
        logger.warning(f"No check-in record found for Employee ID: {emp_id} today")
        print("No check-in record found for today.")
        return
        
    
    if record["check_in_time"] > check_out_str:
        logger.warning(f"check_in_time cannot be greater than check_out_time")
        print("you cannot check_out as check_in_time cannot be greater than check_out_time")
        return
    record["check_out_time"] = check_out_str
    try:
        # Calculate working hours
        dt_obj = validate_date(record["date"]) if record["date"] else None
        ci_obj = validate_time(record["check_in_time"]) if record["check_in_time"] else None
        co_obj = validate_time(record["check_out_time"]) if record["check_out_time"] else None
        wh = calculate_working_hours(dt_obj, ci_obj, co_obj)
        record["working_hours"] = str(wh) if wh > 0 else "0"
    except ValidationError:
        pass
    print("\n--- Check Out ---")
    logger.debug(f"Checked out Employee ID {emp_id} at {check_out_str}")
    write_data(data)
    logger.info(f"Successfully checked out Employee ID: {emp_id}")
    print(f"Checked out successfully at {check_out_str}. Working hours recorded as {record['working_hours']}.")
