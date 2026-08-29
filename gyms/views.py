from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Gym
from .forms import GymForm


@login_required
def gym_profile(request):
    """
    Display gym profile.
    
    Security: Only fetch gym where owner is the logged-in user.
    If user doesn't have a gym, show a friendly message.
    """
    try:
        gym = request.user.gym
        context = {'gym': gym}
        return render(request, 'gyms/profile.html', context)
    except Gym.DoesNotExist:
        # User hasn't created a gym yet
        context = {'gym': None}
        return render(request, 'gyms/profile.html', context)


@login_required
def gym_edit(request):
    """
    Edit gym profile or create one if it doesn't exist.
    
    GET: Show edit form
    POST: Save changes to database
    
    Security: Only allow editing own gym.
    """
    try:
        gym = request.user.gym
    except Gym.DoesNotExist:
        gym = None

    if request.method == 'POST':
        form = GymForm(request.POST, instance=gym)
        if form.is_valid():
            gym = form.save(commit=False)
            gym.owner = request.user
            gym.save()
            messages.success(request, 'Gym profile saved successfully!')
            return redirect('gyms:profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = GymForm(instance=gym)

    context = {'form': form, 'gym': gym}
    return render(request, 'gyms/edit.html', context)

