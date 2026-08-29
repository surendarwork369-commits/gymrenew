from django.core.management.base import BaseCommand

from gyms.models import Gym
from reminders.services import generate_membership_reminders_for_gym


class Command(BaseCommand):
    help = 'Check all gym members and send membership expiry reminders.'

    def handle(self, *args, **options):
        total = 0
        for gym in Gym.objects.all():
            sent_count = generate_membership_reminders_for_gym(gym)
            total += sent_count
            self.stdout.write(self.style.SUCCESS(f'{gym.gym_name}: {sent_count} reminder(s) sent.'))

        self.stdout.write(self.style.SUCCESS(f'Finished. Total reminders sent: {total}'))
