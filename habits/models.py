from django.conf import settings
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Обладатель привычки",
        **NULLABLE,
    )
    location = models.CharField(
        max_length=200, default="дома", verbose_name="Место привычки"
    )
    habit_time = models.DateTimeField(
        verbose_name="Следующая дата и время выполнения привычки"
    )
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_nice = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, verbose_name="Связанная привычка", **NULLABLE
    )
    period = models.PositiveIntegerField(verbose_name="Частота выполнения привычки")
    present = models.CharField(
        max_length=200, verbose_name="Вознаграждение", **NULLABLE
    )
    complete_time = models.DurationField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=True, verbose_name="Публичная привычка")

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
