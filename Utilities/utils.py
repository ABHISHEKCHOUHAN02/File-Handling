

class ValidationError(Exception):
    '''
        Custom exception for validation error.
    '''
    pass


def validate_required(value, field_name="Field"):
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValidationError(f"{field_name} is required.")
    return value


def validate_type(value, expected_type, field_name="Field"):
    if not isinstance(value, expected_type):
        raise ValidationError(f"{field_name} must be of type {expected_type}.")
    return value

def validate_numeric(value, field_name="Field"):
    try:
        num = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a valid number.")
    return num

def validate_positive_numeric(value, field_name="Field"):
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValidationError(f"{field_name} is required.")
    try:
        num = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a integer.")
    if num <= 0:
        raise ValidationError(f"{field_name} must be a positive integer gretaer than 0.")
    return num

def validate_list_not_empty(value, field_name="Field"):
    if not isinstance(value, list) or len(value) == 0:
        raise ValidationError(f"{field_name} must be non-empty list")
    return value