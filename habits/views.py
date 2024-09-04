from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner
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
        """Создаем привычку и отправляем сообщение пользователю сообщение в Телеграм об этом."""
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()
        if habit.user.tg_chat_id:
            telegram_message(habit.user.tg_chat_id, 'Создана новая привычка !')


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
