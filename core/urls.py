# core/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('settings/', views.profile_settings_view, name='profile_settings'),
    path('api/add-subscription/', views.add_user_subscription_api, name='add_user_subscription'),
    path('api/remove-subscription/<int:user_sub_id>/', views.remove_user_subscription_api,
         name='remove_user_subscription'),
]
