from rest_framework import generics
from rest_framework.permissions import AllowAny

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner


class PublicListAPIView(generics.ListAPIView):
    """Выывод публичных привычек."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = (AllowAny,)
    pagination_class = HabitPaginator


class HabitListAPIView(generics.ListAPIView):
    """Просмотр привычек пользователя."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        """Привязка привычки к пользователю."""
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        message = "привычка создана"
        if user.tg_nick:
            telegram_message(user.tg_nick, message)

        return Response({"message": message})


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр подробностей привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Изменение привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        """Привязка привычки к пользователю."""
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки."""
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
