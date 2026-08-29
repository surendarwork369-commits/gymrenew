from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Member
from .forms import MemberForm


@login_required
def member_list(request):
    """
    List all members of the logged-in user's gym.
    
    Features:
    - Search by name or phone
    - Pagination (10 members per page)
    
    Security: Only show members belonging to user's gym.
    """
    try:
        gym = request.user.gym
    except:
        messages.error(request, 'Please create a gym profile first.')
        return redirect('gyms:profile')

    # Get members belonging to this gym
    members_query = Member.objects.filter(gym=gym)

    # Search by name or phone
    search_query = request.GET.get('search', '')
    if search_query:
        members_query = members_query.filter(
            Q(name__icontains=search_query) | Q(phone__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(members_query, 10)
    page_number = request.GET.get('page', 1)
    members = paginator.get_page(page_number)

    context = {
        'members': members,
        'search_query': search_query,
        'gym': gym,
    }
    return render(request, 'members/list.html', context)


@login_required
def member_add(request):
    """
    Add a new member to the gym.
    
    GET: Show form
    POST: Save member to database
    
    Security: Member is automatically associated with user's gym.
    """
    try:
        gym = request.user.gym
    except:
        messages.error(request, 'Please create a gym profile first.')
        return redirect('gyms:profile')

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.gym = gym
            member.save()
            messages.success(request, f'{member.name} added successfully!')
            return redirect('members:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MemberForm()

    context = {'form': form, 'gym': gym}
    return render(request, 'members/form.html', context)


@login_required
def member_detail(request, member_id):
    """
    Display member details.
    
    Security: Only show member if they belong to user's gym.
    If user tries to access another gym's member, return 404.
    """
    try:
        gym = request.user.gym
    except:
        return redirect('gyms:profile')

    member = get_object_or_404(Member, id=member_id, gym=gym)
    context = {'member': member}
    return render(request, 'members/detail.html', context)


@login_required
def member_edit(request, member_id):
    """
    Edit a member's information.
    
    Security: Only allow editing own gym's members.
    """
    try:
        gym = request.user.gym
    except:
        return redirect('gyms:profile')

    member = get_object_or_404(Member, id=member_id, gym=gym)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully!')
            return redirect('members:detail', member_id=member.id)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MemberForm(instance=member)

    context = {'form': form, 'member': member}
    return render(request, 'members/form.html', context)


@login_required
def member_delete(request, member_id):
    """
    Delete a member.
    
    GET: Show confirmation page
    POST: Actually delete the member
    
    Security: Only allow deleting own gym's members.
    """
    try:
        gym = request.user.gym
    except:
        return redirect('gyms:profile')

    member = get_object_or_404(Member, id=member_id, gym=gym)

    if request.method == 'POST':
        member_name = member.name
        member.delete()
        messages.success(request, f'{member_name} has been deleted.')
        return redirect('members:list')

    context = {'member': member}
    return render(request, 'members/confirm_delete.html', context)

