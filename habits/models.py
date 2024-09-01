from django.conf import settings
from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    UNITS_OF_TIME = [
        ("minutes", "минуты"),
        ("hours", "часы"),
        ("days", "дни"),
    ]

    LOCATIONS = [
        ("home", "дом"),
        ("work", "работа"),
        ("street", "улица"),
        ("auto", "автомобиль"),
        ("fitness", "фитнес зал"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Обладатель привычки",
        **NULLABLE,
    )
    location = models.CharField(max_length=200, choices=LOCATIONS, default="home", verbose_name="Место привычки")
    habit_time = models.DateTimeField(verbose_name="Время выполнения привычки")
    action = models.CharField(max_length=200, verbose_name="Действие")
    is_nice = models.BooleanField(verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE, verbose_name="Связанная привычка"
    )
    periodicity = models.CharField(
        max_length=10,
        choices=UNITS_OF_TIME,
        default="days",
        verbose_name="Единицы измерения",
    )
    present = models.CharField(max_length=200, verbose_name="Вознаграждение", **NULLABLE)
    complete_time = models.DurationField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=True, verbose_name="Публичная привычка")

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
