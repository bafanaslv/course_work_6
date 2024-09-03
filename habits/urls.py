from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from habits.apps import HabitsConfig
from habits.views import (
    HabitListAPIView,
    HabitCreateAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    PublicListAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habits"),
    path("public/", PublicListAPIView.as_view(), name="public"),
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="retrieve"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="delete"),
]

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Подписка на курсы обучения.",
        terms_of_service="http://localhost:8000/courses/",
        contact=openapi.Contact(email="foxship@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
