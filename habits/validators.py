from datetime import timedelta

from rest_framework.serializers import ValidationError


class HabitValidator:
    def __init__(self, field1, field2, field3, field4, field5, field6):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.field4 = field4
        self.field5 = field5
        self.field6 = field6

    def __call__(self, value):
        val = dict(value)
        if val.get("complete_time") > timedelta(seconds=120):
            raise ValidationError("Время выполнения привычки не может быть больше 2-х минут !")
        elif val.get("period") < 1 or val.get("period") > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней !')
        elif val.get("is_nice") is False and not val.get("present") and not val.get("related_habit"):
            raise ValidationError("У поолезной привычки должно быть заполнено одно из полей: 'Вознаграждение' или 'Связанная привычка' !")
        elif val.get("is_nice") is False and val.get("present") and val.get("related_habit"):
            raise ValidationError("У полезной привычки должно быть заполнено только одно из полей: 'Вознаграждение' или 'Связанная привычка' !")
        elif val.get("is_nice") is True and val.get("related_habit"):
            raise ValidationError("Приятная привычка не должна быть связана с другой привычкой !")
        elif val.get("is_nice") is True and val.get("present"):
            raise ValidationError("У приятной привычки не должно быть вознагаждения !")
        # elif val.get("related_habit") == val.get("id"):
        #     raise ValidationError("Связанная привычка на должна ссылаться на самого себя !")


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
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        val_related_habit = dict(value).get(self.field1)
        val_is_nice = dict(value).get(self.field2)
        if val_related_habit:
            if not val_is_nice:
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
