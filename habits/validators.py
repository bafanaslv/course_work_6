from datetime import timedelta

from rest_framework.serializers import ValidationError


class PresentValidator:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        val_present = dict(value).get(self.field1)
        val_related_habit = dict(value).get(self.field2)
        if val_present and val_related_habit:
            raise ValidationError("Одновеременное заполнение полей 'Вознаграждение' и 'Связанная привычка' запрещена!")


class RelatedHabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        val_related_habit = dict(value).get(self.field)
        if val_related_habit and val_related_habit.is_nice is False:
            raise ValidationError("Связанная привычка может быть только приятной привычкой!")


class CompleteTimeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if dict(value).get(self.field) > timedelta(seconds=120):
            raise ValidationError("Время выполнения привычки не может быть больше 2-х минут!")


class NaceHabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if dict(value).get(self.field):
            our_value = dict(value)
            if our_value.get("present") or our_value.get("related_habit"):
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки!")


class PeriodicityTimeValidator:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        frequency_in_days = 0
        num = dict(value).get(self.field1)
        unit = dict(value).get(self.field2)

        if num:
            if unit == "minutes":
                frequency_in_days = num / (60 * 24)
            elif unit == "hours":
                frequency_in_days = num / 24
            elif unit == "days":
                frequency_in_days = num

        if frequency_in_days > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней!")
