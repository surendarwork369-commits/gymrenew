from django.utils import timezone

from core.services.whatsapp import send_whatsapp_message
from .models import Reminder


def determine_member_reminder_type(member):
    """Map the member date to the reminder type used by the automation job."""
    days_left = member.days_until_expiry

    if days_left < 0:
        return 'MEMBERSHIP_EXPIRED'
    if days_left <= 7:
        return 'MEMBERSHIP_EXPIRING'
    return None


def build_membership_reminder_message(member, reminder_type):
    """Create a simple WhatsApp-style reminder message."""
    expiry_date = member.membership_end_date.strftime('%d %b %Y')

    if reminder_type == 'MEMBERSHIP_EXPIRED':
        return (
            f"Hi {member.name}, your membership expired on {expiry_date}. "
            "Please renew your membership to continue using the gym."
        )

    days_left = member.days_until_expiry
    if days_left == 0:
        return (
            f"Hi {member.name}, your membership expires today ({expiry_date}). "
            "Please renew today to avoid interruption."
        )

    return (
        f"Hi {member.name}, your membership expires in {days_left} days "
        f"({expiry_date}). Please renew soon."
    )


def send_member_reminder(reminder):
    """Send a reminder through the mock WhatsApp provider and update status."""
    result = send_whatsapp_message(reminder.member.phone, reminder.message)

    if result.get('success'):
        reminder.status = 'SENT'
        reminder.sent_at = timezone.now()
        reminder.provider_message_id = result.get('provider_message_id')
        reminder.error_message = ''
        reminder.save(update_fields=['status', 'sent_at', 'provider_message_id', 'error_message', 'updated_at'])
        return reminder

    reminder.status = 'FAILED'
    reminder.error_message = result.get('error', 'Unknown error while sending reminder.')
    reminder.save(update_fields=['status', 'error_message', 'updated_at'])
    return reminder


def create_member_reminder(member):
    """Create a reminder if the member is within the expiry window and no duplicate exists today."""
    reminder_type = determine_member_reminder_type(member)
    if reminder_type is None:
        return None

    today = timezone.now().date()
    duplicate_exists = Reminder.objects.filter(
        member=member,
        reminder_type=reminder_type,
        created_at__date=today,
        status='SENT'
    ).exists()

    if duplicate_exists:
        return None

    message = build_membership_reminder_message(member, reminder_type)
    reminder = Reminder.objects.create(
        gym=member.gym,
        member=member,
        reminder_type=reminder_type,
        message=message,
        status='PENDING',
        scheduled_at=timezone.now(),
    )

    return send_member_reminder(reminder)


def generate_membership_reminders_for_gym(gym):
    """Check all members in a gym and trigger expiry reminders if needed."""
    created_count = 0

    for member in gym.members.all():
        reminder_type = determine_member_reminder_type(member)
        if reminder_type is None:
            continue

        today = timezone.now().date()
        already_sent = Reminder.objects.filter(
            member=member,
            reminder_type=reminder_type,
            created_at__date=today,
            status='SENT'
        ).exists()

        if already_sent:
            continue

        message = build_membership_reminder_message(member, reminder_type)
        reminder = Reminder.objects.create(
            gym=gym,
            member=member,
            reminder_type=reminder_type,
            message=message,
            status='PENDING',
            scheduled_at=timezone.now(),
        )
        send_member_reminder(reminder)
        created_count += 1

    return created_count
