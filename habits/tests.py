from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import Users


class HabitTestCase(APITestCase):
    """Тестирование CRUD привычек."""

    def setUp(self):
        self.user = Users.objects.create(email="foxship@yandex.ru")
        self.habit = Habit.objects.create(
            user=self.user,
            location="дома",
            habit_time="2024-09-05T14:31:00+03:00",
            action="сделать отжимание 50 раз",
            is_nice="False",
            period=1,
            present="Null",
            complete_time="00:02:00",
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        url = reverse("habits:habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create(self):
        url = reverse("habits:create")
        data = {
            "user": self.user.pk,
            "location": "дома",
            "habit_time": "2024-09-05T14:32:00+03:00",
            "action": "выпить чашечку кофе",
            "is_nice": "True",
            "period": 1,
            "complete_time": "00:02:00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_retrieve(self):
        url = reverse("habits:retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("period"), self.habit.period)

    def test_habit_update(self):
        url = reverse("habits:update", args=(self.habit.pk,))
        data = {
            "location": "на улице",
            "habit_time": "2024-09-05T16:32:00+03:00",
            "action": "выпить чашечку кофе",
            "is_nice": "True",
            "period": 1,
            "complete_time": "00:02:00",
        }
        response = self.client.patch(url, data)
        data = response.json()
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("location"), "на улице")

    def test_habit_delete(self):
        url = reverse("habits:delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_public_list(self):
        url = reverse("habits:public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
