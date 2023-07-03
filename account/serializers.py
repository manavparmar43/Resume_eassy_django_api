from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User, Role


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ("name", "username", "email", "password", "is_staff", "is_superuser")

    def validate(self, data):
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        if email and username and password:
            user = User.objects.filter(email=email).first()
            if user:
                raise ValidationError({"email": "This Email already exists"}, code=401)
        return data


class RoleSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")
