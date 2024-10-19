from collections import defaultdict
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def validate_string_field(field_name, value, min_length=False, max_length=False, list_of_errors=defaultdict(list)):
    """Validates a string field to ensure it meets specified length and content criteria.

    Args:
        field_name (str): The name of the field being validated, used in the error messages.
        value (str): The value of the field to validate.
        min_length (int, optional): The minimum length of the field value. Defaults to 0.
        max_length (int, optional): The maximum length of the field value. Defaults to 200.

    Returns:
        list: A list of error messages, if any.

    Raises:
        serializers.ValidationError: If the field value is invalid.
    """
    if value is not None:
        if value is None or value.strip() == "":
            list_of_errors[field_name].append(f'The {field_name} field cannot be empty')
        if not isinstance(value, str):
            list_of_errors[field_name].append(f'The {field_name} field must be a string')
        if value.isdigit():
            list_of_errors[field_name].append(f'The {field_name} cannot contain only numbers')
        if min_length is not False and len(value) < min_length:
            list_of_errors[field_name].append(f'The {field_name} must be at least {min_length} characters long')
        if max_length is not False and len(value) > max_length:
            list_of_errors[field_name].append(f'The {field_name} must have a maximum of {max_length} characters')
    
    return list_of_errors

def validate_email_field(email):
    """Validates an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.

    Raises:
        ValidationError: If the email address is not valid, a ValidationError is raised.
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validate_password_strength(password, list_of_errors=[]):
    """Validates the strength of a password.

    Args:
        password (str): The password to validate.

    Returns:
        list: A list of error messages if the password is weak.

    Raises:
        serializers.ValidationError: If the password does not meet the strength criteria.
    """
    if len(password) < 6:
        list_of_errors['password'].append("Password must be at least 6 characters long.")
    
    if not re.search(r'\d', password):
        list_of_errors['password'].append("Password must contain at least one number.")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        list_of_errors['password'].append("Password must contain at least one special character.")

    return list_of_errors