from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            HabitValidator(
                field1="present",
                field2="related_habit",
                field3="is_nice",
                field4="complete_time",
                field5="period",
                field6="id",
            )
        ]
