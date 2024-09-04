from celery import shared_task
from habits.services import telegram_message
from django.conf import settings
import pytz
from datetime import datetime, timedelta
from habits.models import Habit


@shared_task()
def telegram_message_list():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(zone)
    current_time_less = current_time - timedelta(minutes=5)
    # habits = Habit.objects.filter(time__lte=current_time.time(), time__gte=current_time_less.time())
    habits = Habit.objects.all()
    for habit in habits:
        user_tg = habit.user.tg_chat_id
        if user_tg:
            message = f"я буду {habit.action} в {habit.habit_time} в {habit.location}"
            telegram_message(user_tg, message)
