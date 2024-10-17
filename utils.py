from rest_framework import serializers

def validate_string_field(field_name, value, min_length=0, max_length=200):
    if value is None or value.strip() == "":
        raise serializers.ValidationError({field_name: f'The {field_name} field cannot be empty'})
    if value.isdigit():
        raise serializers.ValidationError({field_name: f'The {field_name} cannot contain only numbers'})
    if len(value) < min_length:
        raise serializers.ValidationError({field_name: f'The {field_name} must be at least {min_length} characters long'})
    if len(value) > max_length:
        raise serializers.ValidationError({field_name: f'The {field_name} must have a maximum of {max_length} characters'})