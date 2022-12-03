from threading import local
from allauth.account.auth_backends import AuthenticationBackend as AllAuthBackend
from .utils import filter_users_by_mobile

_stash = local()

class AuthenticationBackend(AllAuthBackend):
    def authenticate(self, request, **credentials):
        ret = None

        if credentials.get('mobile_number'):
            ret = self._authenticate_by_mobile(**credentials)

        if not ret:
            ret = super().authenticate(request, **credentials)

        return ret 

    def _authenticate_by_mobile(self, **credentials):
        mobile = credentials.get("mobile_number", credentials.get('username'))
        if mobile:
            for user in filter_users_by_mobile(mobile):
                if self._check_password(user, credentials["password"]):
                    return user
        return None
