from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import (
    PresentValidator,
    RelatedHabitValidator,
    PeriodicityTimeValidator,
    NaceHabitValidator,
    CompleteTimeValidator,
)


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            PresentValidator(field1="present", field2="related_habit"),
            RelatedHabitValidator(field="related_habit"),
            CompleteTimeValidator(field="complete_time"),
            NaceHabitValidator(field="is_nice"),
            PeriodicityTimeValidator(field1="periodicity_quantity", field2="periodicity_init"),
        ]
