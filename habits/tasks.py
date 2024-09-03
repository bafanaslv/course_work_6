import datetime
from habits.models import Habit
from django.utils import timezone

from celery import shared_task

from habits.utils import telegram_message
from config import settings

settings.timedelta()


@shared_task
def telegram_message():
    """Функция проверки отправки сообщений с ориентированнием на последнее отправленное сообщение.
    """

    datetime_now = timezone.now()

    habits = [Habit.objects.all()]
    for habit in habits:
        last_try_date = habit.last_try or datetime_now - datetime.timedelta(
            days=999
        )
        send_message = False

        if habit.periodicity == Habit.PERIOD_DAILY:
            send_message = (datetime_now - last_try_date).days >= 1
        elif habit.periodicity == Habit.EVERY_OTHER_DAYS:
            send_message = (datetime_now - last_try_date).days >= 2
        elif habit.periodicity == Habit.WEEKEND:
            send_message = (
                    datetime_now.weekday() in (6, 7)
                    and (datetime_now - last_try_date).days >= 1
            )

        if send_message and (datetime_now.time() >= habit.time):
            chat_id = habit.user.tg_nick
            massage = habit.action
            telegram_message(chat_id, massage)
            habit.last_try = datetime_now
            habit.save()
