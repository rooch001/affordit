# core/views.py
import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from scrapers.models import Service
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm, UserUpdateForm
from .models import UserSubscription, Profile


def home_view(request):
    return render(request, 'home.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save profile data
            user.profile.monthly_income = form.cleaned_data.get('monthly_income')
            user.profile.hours_worked_weekly = form.cleaned_data.get('hours_worked_weekly')
            user.profile.save()
            login(request, user)
            return redirect('dashboard')  # <-- Corrected redirect
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # <-- Corrected redirect
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    # This line ensures a profile exists for the logged-in user.
    profile, created = Profile.objects.get_or_create(user=request.user)

    all_services = Service.objects.order_by('name')
    user_subscriptions = UserSubscription.objects.filter(profile=profile).select_related('plan', 'plan__service')

    context = {
        'all_services': all_services,
        'user_subscriptions_json': json.dumps([
            {
                'id': sub.id,
                'service_name': sub.plan.service.name,
                'plan_name': sub.plan.plan_name,
                'price': float(sub.plan.price),
                'category': sub.plan.service.category
            } for sub in user_subscriptions
        ]),
        'user_profile_json': json.dumps({
            'income': float(profile.monthly_income or 0),
            'hours': int(profile.hours_worked_weekly or 0)
        })
    }
    return render(request, 'dashboard.html', context)


@login_required
@require_POST
def add_user_subscription_api(request):
    """
    API endpoint for a user to add a subscription with manually entered details.
    """
    try:
        data = json.loads(request.body)
        service_id = data.get('service_id')
        plan_name = data.get('plan_name')
        price = data.get('price')
        currency = data.get('currency')

        # Basic validation
        if not all([service_id, plan_name, price, currency]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        service = Service.objects.get(id=service_id)

        # Create the new user subscription with user-provided data
        user_sub, created = UserSubscription.objects.get_or_create(
            profile=request.user.profile,
            service=service,
            plan_name=plan_name,
            defaults={'price': price, 'currency': currency}
        )

        if not created:
            return JsonResponse({'status': 'error', 'message': 'You have already added this subscription plan.'},
                                status=400)

        # Return the newly created object's data for the frontend
        return JsonResponse({
            'status': 'success',
            'subscription': {
                'id': user_sub.id,
                'service_name': service.name,
                'plan_name': user_sub.plan_name,
                'price': float(user_sub.price),
                'category': service.category
            }
        })
    except Service.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Selected service not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def remove_user_subscription_api(request, user_sub_id):
    try:
        sub = UserSubscription.objects.get(id=user_sub_id, profile=request.user.profile)
        sub.delete()
        return JsonResponse({'status': 'success'})
    except UserSubscription.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Subscription not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def calculator_view(request):
    services = Service.objects.order_by('name')
    context = {'services': services}
    return render(request, 'calculator.html', context)


@login_required
def profile_settings_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile_settings.html', context)
