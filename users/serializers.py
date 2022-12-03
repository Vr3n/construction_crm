import re
import pdb
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import exceptions
from django.urls import exceptions as url_exceptions
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from .models import CustomUser, MobileNumber
from .validators import unique_mobile_validator, character_only_validator, digits_only_validator

# Create your serializers here.

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    mobile_number = serializers.CharField(
        required=True, max_length=10, validators=[unique_mobile_validator])
    first_name = serializers.CharField(required=True, validators=[
                                       character_only_validator])
    last_name = serializers.CharField(required=True, validators=[
                                      character_only_validator])
    password1 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    regex_patterns = {
        'digit_only_regex': re.compile(r'^[0-9]*$'),
        'chars_only_regex': re.compile(r'^[A-Za-z]*$')
    }

    def validate_mobile_number(self, mobile_number):
        if not bool(re.search(self.regex_patterns['digit_only_regex'], mobile_number)):
            raise serializers.ValidationError(
                "Mobile Number should only consist Numbers."
            )

        if len(mobile_number) != 10:
            raise serializers.ValidationError(
                "Mobile number should be 10 digits."
            )

        return mobile_number

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.mobile_number = self.data.get('mobile_number')
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        MobileNumber.objects.create(
            user=user, mobile_number=user.mobile_number, is_primary=True)
        return user


class CustomLoginSerializer(LoginSerializer):
    mobile_number = serializers.CharField(required=False, allow_blank=True)

    def _validate_mobile_number_username_email(self, username, email, mobile_number, password):
        if mobile_number and password:
            user = self.authenticate(
                mobile_number=mobile_number, password=password)
        elif email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _(
                "Must include either 'username' or 'email' or 'mobile number' and password")
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, username, email, mobile_number, password):
        return self._validate_mobile_number_username_email(username, email, mobile_number, password)

    def get_auth_user_using_orm(self, username, email, mobile_number, password):
        if mobile_number:
            try:
                username = User.objects.get(
                    mobile_number__iexact=mobile_number).get_username()
            except User.DoesNotExist:
                if email:
                    try:
                        username = User.objects.get(
                            email__iexact=email).get_username()
                    except User.DoesNotExist:
                        pass

        if username:
            return self._validate_username_email(username, '', password)

        return None

    def get_auth_user(self, username, email, mobile_number, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.
        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if 'allauth' in settings.INSTALLED_APPS:

            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, mobile_number, password)
            except url_exceptions.NoReverseMatch:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, mobile_number, password)

    @staticmethod
    def validate_mobile_verification_status(user):
        mobile_number = user.mobilenumber_set.get(
            mobile_number=user.mobile_number)
        if not mobile_number.is_verified:
            raise serializers.ValidationError(_('Mobile number not verified'))

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get("username")
        user = self.get_auth_user(username, email, mobile_number, password)

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        self.validate_auth_user_status(user)

        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)
            # self.validate_mobile_verification_status(user)

        attrs['user'] = user
        return attrs
