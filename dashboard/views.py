from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from gyms.models import Gym
from members.models import Member


@login_required
def dashboard(request):
    """Display gym dashboard with member health summary and expiring memberships."""
    try:
        gym = request.user.gym
    except Gym.DoesNotExist:
        messages.info(request, 'Create your gym profile before viewing the dashboard.')
        return redirect('gyms:edit')

    all_members = Member.objects.filter(gym=gym)

    search_query = request.GET.get('search', '').strip()
    filtered_members = all_members
    if search_query:
        filtered_members = filtered_members.filter(
            Q(name__icontains=search_query) | Q(phone__icontains=search_query)
        )

    status_filter = request.GET.get('status', 'all').lower()
    matching_members = []
    for member in filtered_members:
        status = member.membership_status
        if status_filter == 'all' or status.lower() == status_filter:
            matching_members.append(member)

    matching_members.sort(key=lambda member: member.membership_end_date)

    total_members = all_members.count()
    active_members = sum(1 for member in all_members if member.membership_status == 'ACTIVE')
    expiring_soon_members = [member for member in all_members if member.membership_status == 'EXPIRING_SOON']
    expired_members = sum(1 for member in all_members if member.membership_status == 'EXPIRED')

    context = {
        'page_title': 'Dashboard',
        'gym': gym,
        'members': matching_members,
        'total_members': total_members,
        'active_members': active_members,
        'expiring_soon_count': len(expiring_soon_members),
        'expired_members': expired_members,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/dashboard.html', context)

