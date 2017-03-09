import re
import json
from rest_framework import serializers

def password_validation_check(value):
    value = value.strip()
    pattern = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
    match = pattern.match(value)
    return match

def list_validation_check(value):
    try:
        value = json.loads(value)
    except Exception as e:
        raise serializers.ValidationError('JSON FORMAT ERROR: %s' % e)
    if not isinstance(value, list):
        raise serializers.ValidationError('Input data should be a list')
    return value
