from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import HabitValidator
# from habits.validators import (
#     PresentValidator,
#     RelatedHabitValidator,
#     PeriodicityValidator,
#     NaceHabitValidator,
#     CompleteTimeValidator,
# )


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [HabitValidator(field1="present", field2="related_habit",
                                     field3="is_nice", field4="complete_time",
                                     field5="period")]


# class HabitSerializer(ModelSerializer):
#     class Meta:
#         model = Habit
#         fields = "__all__"
#         validators = [
#             PresentValidator(field1="present", field2="related_habit"),
#             RelatedHabitValidator(field1="related_habit", field2="is_nice"),
#             CompleteTimeValidator(field="complete_time"),
#             NaceHabitValidator(field="is_nice"),
#             PeriodicityValidator(field="period"),
#         ]
#
