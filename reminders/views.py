from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from urllib.parse import quote

from members.models import Member
from .models import Reminder
from .services import build_membership_reminder_message, determine_member_reminder_type


@login_required
def reminder_list(request):
    try:
        gym = request.user.gym
    except Exception:
        messages.error(request, 'Please create a gym profile first.')
        return redirect('gyms:profile')

    reminders = Reminder.objects.filter(gym=gym).select_related('member')
    context = {'reminders': reminders, 'gym': gym}
    return render(request, 'reminders/list.html', context)


@login_required
def send_member_reminder(request, member_id):
    try:
        gym = request.user.gym
    except Exception:
        return redirect('gyms:profile')

    member = get_object_or_404(Member, id=member_id, gym=gym)

    if request.method != 'POST':
        return redirect('members:detail', member_id=member.id)

    reminder_type = determine_member_reminder_type(member)
    if reminder_type is None:
        messages.info(request, 'This member is not currently in the reminder window.')
        return redirect('members:detail', member_id=member.id)

    phone_number = ''.join(character for character in member.phone if character.isdigit())
    if phone_number.startswith('0'):
        phone_number = phone_number[1:]
    if len(phone_number) == 10:
        phone_number = f'91{phone_number}'
    if not phone_number:
        messages.error(request, 'This member does not have a valid phone number.')
        return redirect('members:detail', member_id=member.id)

    message = build_membership_reminder_message(member, reminder_type)
    whatsapp_url = f'https://wa.me/{phone_number}?text={quote(message)}'
    return HttpResponseRedirect(whatsapp_url)
