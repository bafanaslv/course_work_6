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


class PeriodicityValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('period') < 1 or value.get('period') > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
