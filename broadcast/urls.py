from django.urls import path
from .views import test_celery

urlpatterns = [
    path('', test_celery, name="test_celery"),
]
