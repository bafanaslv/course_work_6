from datetime import timedelta

from rest_framework.serializers import ValidationError


class HabitValidator:

    def __init__(self, field1, field2, field3, field4, field5, field6):
        self.field1 = field1  # вознаграждение за полезную привычку
        self.field2 = field2  # связанная привычка (только для полезных)
        self.field3 = field3  # признак приятной привычки
        self.field4 = field4  # время выполнения привычки
        self.field5 = field5  # периодичность выполнения привычки в днях (от 1 до 7)
        self.field6 = field6  # id привычки

    def __call__(self, value):
        val = dict(value)  # конвертируем QuerySet в словарь

        if val.get("complete_time") > timedelta(seconds=120):
            raise ValidationError(
                "Время выполнения привычки не может быть больше 2-х минут !"
            )

        elif int(val.get("period")) < 1 or int(val.get("period")) > 7:
            raise ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней !"
            )

        elif (
            val.get("is_nice") is False
            and not val.get("present")
            and not val.get("related_habit")
        ):
            raise ValidationError(
                "У полезной привычки должно быть заполнено одно из полей: 'Вознаграждение' или 'Связанная привычка' !"
            )

        elif (
            val.get("is_nice") is False
            and val.get("present")
            and val.get("related_habit")
        ):
            raise ValidationError(
                "У полезной привычки может быть заполнено только одно из полей: "
                "'Вознаграждение' или 'Связанная привычка' !"
            )

        elif val.get("is_nice") is True and val.get("related_habit"):
            raise ValidationError(
                "У приятной привычки не может быть связаная привычка !"
            )

        elif val.get("is_nice") is True and val.get("present"):
            raise ValidationError("У приятной привычки не может быть вознаграждения !")

        # elif val.get("related_habit") == val.get("id"):
        #     raise ValidationError("Связанная привычка на должна ссылаться на самого себя !")
