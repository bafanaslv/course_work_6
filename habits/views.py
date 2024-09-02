from rest_framework import generics
from rest_framework.permissions import AllowAny

from habits.models import Habit
from habits.paginations import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner
# from habits.services import send_telegram_message
from rest_framework.response import Response


class HomeListAPIView(generics.ListAPIView):
    """
    Класс вывода привычек с флагом публичные.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = (AllowAny,)
    pagination_class = HabitPaginator


class HabitListAPIView(generics.ListAPIView):
    """
    Класс просмотра привычек пользователя.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Класс создания привычки.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        """
        Привязка привычки к пользователю.
        :param serializer:
        :return:
        """
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    # def post(self, request, *args, **kwargs):
    #     user = self.request.user
    #     message = "привычка создана"
    #     if user.tg_nick:
    #         send_telegram_message(user.tg_nick, message)
    #
    #     return Response({"message": message})


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Класс просмотра подробностей привычки.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Класс изменения привычки.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        """
        Привязка привычки к пользователю.
        :param serializer:
        :return:
        """
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Класс удаления привычки.
    """

    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
