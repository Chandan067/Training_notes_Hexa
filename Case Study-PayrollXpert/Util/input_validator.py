import re
from datetime import datetime, date
from exceptions.custom_exceptions import InvalidInputException

def validate_not_empty(value, field_name):
    if not value or not str(value).strip():
        raise InvalidInputException(f"❌ {field_name} cannot be empty.")
    return str(value).strip()

def validate_email(email):
    email = str(email).strip()
    pattern = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(pattern, email):
        raise InvalidInputException("❌ Invalid email format.")
    return email

def validate_numeric(value, field_name):
    value = str(value).strip()
    if not value.isdigit():
        raise InvalidInputException(f"❌ {field_name} must be numeric.")
    return value

def validate_float(value, field_name):
    value = str(value).strip()
    try:
        return float(value)
    except ValueError:
        raise InvalidInputException(f"❌ {field_name} must be a valid number.")

def validate_date(date_input, field_name):
    if isinstance(date_input, date):
        return date_input
    try:
        return datetime.strptime(date_input.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise InvalidInputException(f"❌ {field_name} must be in YYYY-MM-DD format.")

def validate_positive_number(value, field_name="Amount"):
    try:
        number = float(str(value).strip())
        if number < 0:
            raise InvalidInputException(f"❌ {field_name} must be non-negative.")
        return number
    except ValueError:
        raise InvalidInputException(f"❌ {field_name} must be a valid number.")

def validate_alpha_name(value, field_name):
    value = str(value).strip()
    if not value:
        raise InvalidInputException(f"❌ {field_name} cannot be empty.")
    if not value.replace(" ", "").isalpha():
        raise InvalidInputException(f"❌ {field_name} must contain only letters.")
    return value