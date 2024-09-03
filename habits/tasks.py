from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.utils import telegram_message


@shared_task()
def habit():

    now = timezone.now()
    print(f"Текущее время: {now}")

    habits = Habit.objects.filter(
        time__lte=now, time__gt=now - timezone.timedelta(minutes=1)
    )

    print(f"Найдено привычек: {habits.count()}")

    for habit in habits:
        if habit.user.tg_chat_id:
            telegram_message(habit)
            if habit.frequency_unit == "days":
                habit.time = habit.time + timezone.timedelta(
                    days=habit.frequency_number
                )
            elif habit.frequency_unit == "hours":
                habit.time = habit.time + timezone.timedelta(
                    hours=habit.frequency_number
                )
            elif habit.frequency_unit == "minutes":
                habit.time = habit.time + timezone.timedelta(
                    minutes=habit.frequency_number
                )
            habit.save()
        else:
            print(f"У пользователя {habit.user} не указан Телеграм чат id!")
