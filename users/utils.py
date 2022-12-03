from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist, ValidationError
from allauth.account.utils import _unicode_ci_compare

def user_field(user, field, *args):
    """
    Gets or sets (optional) user model fields. No-op if fields do not exist.
    """

    if not field:
        return
    User = get_user_model()
    try:
        field_meta = User._meta.get_field(field)
        max_length = field_meta.max_length
    except FieldDoesNotExist:
        if not hasattr(user, field):
            return
        max_length = None

    if args:
        # Setter
        v = args[0]
        if v:
            v = v[0:max_length]
        setattr(user, field, v)
    else:
        # Getter
        return getattr(user, field)


def user_mobile(user, *args):
    return user_field(user, 'mobile_number', *args)

def filter_users_by_mobile(mobile, is_active=None):
    """Return list of users by mobile numbers.

    Typically one, at most just a few in length. First we look through
    MobileNumber table, than customisable User model table. Add results
    together avoiding SQL joins and deduplicate.
    """

    from .models import MobileNumber

    User = get_user_model()
    numbers = MobileNumber.objects.filter(mobile_number__iexact=mobile)
    if is_active is not None:
        numbers = numbers.filter(user__is_active=is_active)
    users = []
    for m in numbers.prefetch_related("user"):
        if _unicode_ci_compare(m.mobile_number, mobile):
            users.append(m.user)
    q_dict = { 'mobile_number__iexact': mobile  }
    user_qs = User.objects.filter(**q_dict)
    if is_active is not None:
        user_qs = user_qs.filter(is_active=is_active)
    for user in user_qs.iterator():
        user_mobile = getattr(user, 'mobile_number')
        if _unicode_ci_compare(user_mobile, mobile):
            users.append(user)
    return list(set(users))

