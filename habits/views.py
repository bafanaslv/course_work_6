from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from habits.models import Habit
from habits.paginations import HabitsPaginator
from users.permissions import IsOwner
from habits.serializers import HabitSerializer


@method_decorator(
    name="list", decorator=swagger_auto_schema(operation_description="Список привычек")
)
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    # permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitsPaginator
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ("action",)
    # ordering_fields = ("habit_time",)

    def get_queryset(self):
        # return Habit.objects.filter(user=self.request.user.pk).order_by("id")
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()

    def get_permissions(self):
        print(self.action)
        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated, IsOwner,
            )
        return super().get_permissions()

class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = HabitsPaginator
