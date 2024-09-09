
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from habits.services import telegram_message


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
        """Создаем привычку и отправляем сообщение пользователю в Телеграм."""
        habit = serializer.save()
        habit.user = self.request.user
        habit = serializer.save()
        habit.save()
        if habit.user.tg_chat_id:
            telegram_message(habit.user.tg_chat_id, "Создана новая привычка !")


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

    def perform_update(self, serializer):
        """Перед сохраннием привычки проверяем не ссылается связанная привычка на саму себя."""
        habit = serializer.save()
        if not habit.is_nice and habit.related_habit and habit.id == habit.related_habit.id:
            raise ValidationError(
                f"Связанная привычка не может быть ссылкой на саму себя !"
            )
        habit.save()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки."""
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
