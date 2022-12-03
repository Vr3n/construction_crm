from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class MobileNumberQuerySet(models.QuerySet):

    def unverified(self):
        """
        The Unverified numbers are filtered.
        """
        return self.filter(is_verified=False)

    def unverified_secondary_numbers(self):
        """
        Returns the unverified secondary numbers added by users.
        """
        return self.filter(is_verified=False, is_primary=False) 



class MobileNumberManager(models.Manager):

    def get_queryset(self):
        return MobileNumberQuerySet(self.model, using=self._db)

    def unverified(self):
        """
        The Unverified Primary numbers are filtered.
        """
        return self.get_queryset().unverified()

    def unverified_secondary_numbers(self):
        """
        Returns the unverified secondary numbers added by users.
        """

        return self.get_queryset().unverified_secondary_numbers()

    def can_add_mobile(self, user):
        count = self.filter(user=user).count()
        if user.max_mobile_numbers < count:
            return False
        return True

    def add_mobile(self, request, user, mobile_number, confirm=False, signup=False):
        mobile_number, created = self.get_or_create(
            user=user, mobile_number__iexact=mobile_number,
            defaults={"mobile_number": mobile_number}
        )
        
    def get_primary(self, user):
        try:
            return self.get(user=user, primary=True)
        except self.model.DoesNotExist:
            return None

    def fill_cache_for_user(self, user, addresses):
        """
        In a mullti-db setup, inserting records and re-reading them later
        on may result in not being able to find newly inserted records.
        Therefore, we maintain a cache for the user so that we can avoid
        database access when we need to re-read.
        """

        user._mobile_cache = addresses

    def get_for_user(self, user, mobile_number):
        cache_key = '_mobile_cache'
        addresses = getattr(user, cache_key, None)
        if addresses is None:
            ret = self.get(user=user, mobile_number__iexact=mobile_number)
            ret.user = user
            return ret

        else:
            for address in addresses:
                if address.email.lower() == email.lower():
                    return address
            raise self.model.DoesNotExist()