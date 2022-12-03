from rest_framework import serializers


def is_not_zero(value):
    if value == 0:
        raise serializers.ValidationError('Value cannot be 0.')

    if value < 0:
        raise serializers.ValidationError("Value cannot be a negative number!")
