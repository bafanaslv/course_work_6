from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from habits.apps import HabitsConfig
from rest_framework.routers import SimpleRouter
from habits.views import HabitViewSet, PublicHabitListAPIView


app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet, basename="habits")

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="public"),
] + router.urls

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
