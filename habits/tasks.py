from celery import shared_task
from habits.services import telegram_message
from django.conf import settings
import pytz
from datetime import datetime, timedelta
from habits.models import Habit
from django.utils import timezone


@shared_task()
def telegram_message_list():
    """Функция за 10 минут до начала выполнения привычки предупреждает и переносит дату следующего
    выполнения на количество дней в зависимости от периодичности выполнения привычки (habit.period)."""
    timezone.activate(pytz.timezone(settings.CELERY_TIMEZONE))
    zone = pytz.timezone(settings.CELERY_TIMEZONE)
    now = datetime.now(zone)  # текущее дата_время
    habits = Habit.objects.all()

    for habit in habits:
        if not habit.related_habit:
            user_tg = habit.user.tg_chat_id
            if user_tg and now < habit.habit_time - timedelta(minutes=10) and now.date() == habit.habit_time.date():
                message = f"Не забудь {habit.action} в {habit.habit_time} в {habit.location}"
                telegram_message(user_tg, message)
                habit.habit_time += timedelta(days=habit.period)
                if habit.present:
                    telegram_message(user_tg, f"Молодец! Ты залужил награду: {habit.present}")
                elif habit.related_habit:
                    rel_habit = Habit.objects.filter(pk=habit.related_habit)
                    telegram_message(user_tg, rel_habit.action)
                habit.save()
