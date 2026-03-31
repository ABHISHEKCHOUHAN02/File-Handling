import datetime
from Utilities.utils import validate_required, ValidationError

def validate_employee_id(emp_id):
    validate_required(emp_id, "employee_id")
    if not emp_id.startswith("EMP"):
        raise ValidationError("employee_id must start with EMP")
    return emp_id

def validate_date(date_str, allow_future=False):
    validate_required(date_str, "date")
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.datetime.now().date()
        if dt > today and not allow_future:
            raise ValidationError("date should not be in future")
        return dt
    except ValueError:
        raise ValidationError("date must be in YYYY-MM-DD format")

def validate_time(time_str, field_name="time"):
    if not time_str or str(time_str).strip() == "":
        return None
    try:
        return datetime.datetime.strptime(str(time_str).strip(), "%H:%M").time()
    except ValueError:
        raise ValidationError(f"{field_name} must be in HH:MM format")

def validate_time_order(check_in, check_out):
    if check_in and check_out:
        if check_out <= check_in:
            raise ValidationError("check_out_time must be greater than check_in_time")

def calculate_status(row_date, check_in_time, forced_status=""):
    forced_status = str(forced_status).strip()
    now = datetime.datetime.now()
    absent_cutoff_time = datetime.datetime.strptime("20:20", "%H:%M").time()

    if check_in_time:
        return "Present"
    elif forced_status and forced_status not in ["Leave", "Half-Day"]:
        if row_date and row_date < now.date():
            return "Absent"
        elif row_date and row_date == now.date() and now.time() > absent_cutoff_time:
            return "Absent"
        else:
            return forced_status
    elif forced_status in ["Leave", "Half-Day"]:
        return forced_status
    else:
        if row_date and row_date < now.date():
            return "Absent"
        elif row_date and row_date == now.date() and now.time() > absent_cutoff_time:
            return "Absent"
        return ""

def calculate_working_hours(row_date, check_in_time, check_out_time):
    if check_in_time and check_out_time and row_date:
        check_in_date_time = datetime.datetime.combine(row_date, check_in_time)
        check_out_date_time = datetime.datetime.combine(row_date, check_out_time)
        working_hours = (check_out_date_time - check_in_date_time).total_seconds() / 3600
        return round(working_hours, 2)
    return 0.0

def validate_leave(status, leave_type, leave_reason):
    if status == "Leave":
        if not leave_type or leave_type.strip() == "":
            raise ValidationError("leave_type is required when status is Leave")
        if not leave_reason or leave_reason.strip() == "":
            raise ValidationError("leave_reason is required when status is Leave")
