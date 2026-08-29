from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from gyms.models import Gym
from members.models import Member
from reminders.models import Reminder
from reminders.services import create_member_reminder


class ReminderServiceTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='gymowner', email='owner@example.com', password='secret123')
        self.gym = Gym.objects.create(
            owner=self.user,
            gym_name='PowerFit',
            phone='9999999999',
            email='powerfit@example.com',
            address='Main Road',
        )
        self.member = Member.objects.create(
            gym=self.gym,
            name='Rahul',
            phone='9898989898',
            email='rahul@example.com',
            membership_start_date=date.today(),
            membership_end_date=date.today() + timedelta(days=3),
            membership_amount='1500.00',
            notes='Trial member',
        )

    def test_duplicate_reminder_is_not_created_twice_for_same_day(self):
        first = create_member_reminder(self.member)
        second = create_member_reminder(self.member)

        self.assertIsNotNone(first)
        self.assertIsNone(second)
        self.assertEqual(Reminder.objects.filter(member=self.member).count(), 1)
