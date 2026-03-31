import re
import datetime
from .utils import ValidationError

def validate_name(name, field_name="Name"):
    if not name or len(name.strip()) < 2:
        raise ValidationError(f"{field_name} must be at least 2 characters long.")
    if not all(c.isalpha() or c.isspace() for c in name):
        raise ValidationError(f"{field_name} must contain only alphabetical characters and spaces.")
    return name.strip()

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(c.isupper() for c in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain at least one digit.")
    return password

def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        raise ValidationError("Invalid email format.")
    return email.strip()

def validate_gender(gender):
    valid_genders = ["Male", "Female", "Other"]
    if gender.capitalize() not in valid_genders:
        raise ValidationError(f"Gender must be one of: {', '.join(valid_genders)}.")
    return gender.capitalize()

def validate_phone(phone):
    try:
        phone_clean = phone.strip()

        if not phone_clean:
            raise ValidationError("Phone number cannot be empty")
        phone_clean = phone_clean.replace(" ", "").replace("-", "")
        regex = r'^\+?\d{10,15}$'
        if not re.match(regex, phone_clean) or len(phone_clean) != 13:
            
            raise ValidationError(
                "Invalid phone number. Must be 10 digits, optional '+', country_code prefix"
            )

        if not phone_clean.startswith("+"):
            phone_clean = "+" + phone_clean

        digits_only = phone_clean[1:]

        # Example: restrict some known country codes (optional strict mode)
        VALID_COUNTRY_CODES = {"91", "1", "44", "61"}

        # Try matching first 1–3 digits as country code
        country_code = None
        for i in range(1, 4):
            code = digits_only[:i]
            if code in VALID_COUNTRY_CODES:
                country_code = code
                break

        if not country_code:
            raise ValidationError(
                f"Invalid or unsupported country code in {phone_clean}"
            )

        return phone_clean

    except:
        raise ValidationError(f"Phone number is invalid")
        
def validate_department(dept):
    tech_keywords = ["it", "software", "devops", "qa", "testing", "data", "app", "cyber_security", "development"]
    dept_lower = dept.lower()
    if not any(keyword in dept_lower for keyword in tech_keywords):
        raise ValidationError(f"Department '{dept}' is not valid.")
    return dept.strip()

def validate_role(role):
    role_keywords = ["intern", "traine", "Associate_Developer", "Developer", "Senioer_developer", "Manager"]
    dept_lower = role.lower()
    if not any(keyword in dept_lower for keyword in role_keywords):
        raise ValidationError(f"Department '{role}' is not valid.")
    return role.strip()
def validate_salary(salary):
    if not salary or salary.strip() == "":
         raise ValidationError("Salary is required.")
    try:
        val = float(salary)
        if val <= 0:
            raise ValidationError("Salary must be a positive number.")
        return val
    except ValueError:
        raise ValidationError("Salary must be numeric.")

def validate_date(date_str):
    if not date_str or date_str.strip() == "":
        raise ValidationError("Joining date is required.")
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        return date_str
    except ValueError:
        raise ValidationError("Date must be in YYYY-MM-DD format.")

def validate_status(status):
    valid_statuses = ["Active", "Inactive"]
    if status.capitalize() not in valid_statuses:
        raise ValidationError(f"Status must be 'Active' or 'Inactive'.")
    return status.capitalize()
