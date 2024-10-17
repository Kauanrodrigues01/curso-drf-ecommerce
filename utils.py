from rest_framework import serializers

def validate_string_field(field_name, value, min_length=0, max_length=200):
    """Validates a string field to ensure it meets specified length and content criteria.

    This function checks if the provided value for a string field is not empty,
    does not consist solely of digits, and adheres to the minimum and maximum length
    constraints.

    Args:
        field_name (str): The name of the field being validated, used in the error messages.
        value (str): The value of the field to validate.
        min_length (int, optional): The minimum length of the field value. Defaults to 0.
        max_length (int, optional): The maximum length of the field value. Defaults to 200.

    Raises:
        serializers.ValidationError: If the field value is empty or consists only of whitespace.
        serializers.ValidationError: If the field value consists solely of digits.
        serializers.ValidationError: If the field value is shorter than the specified minimum length.
        serializers.ValidationError: If the field value exceeds the specified maximum length.
    """
    if value is None or value.strip() == "":
        raise serializers.ValidationError({field_name: f'The {field_name} field cannot be empty'})
    if value.isdigit():
        raise serializers.ValidationError({field_name: f'The {field_name} cannot contain only numbers'})
    if len(value) < min_length:
        raise serializers.ValidationError({field_name: f'The {field_name} must be at least {min_length} characters long'})
    if len(value) > max_length:
        raise serializers.ValidationError({field_name: f'The {field_name} must have a maximum of {max_length} characters'})
