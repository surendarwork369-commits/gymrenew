from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from members.models import Member
from .models import Reminder
from .services import create_member_reminder, determine_member_reminder_type


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

    reminder = create_member_reminder(member)
    if reminder is None:
        messages.info(request, 'A reminder was already sent today for this member.')
    elif reminder.status == 'SENT':
        messages.success(request, f'Reminder sent to {member.name}.')
    else:
        messages.error(request, f'Failed to send reminder to {member.name}.')

    return redirect('members:detail', member_id=member.id)
