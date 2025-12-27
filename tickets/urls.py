from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_detail'),
    path('employees/', views.manage_employees, name='manage_employees'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:ticket_id>/update/', views.ticket_update, name='ticket_update'),
    path('tickets/<int:ticket_id>/delete/', views.ticket_delete, name='ticket_delete'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path("verify-email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("resend-verification/<int:user_id>/", views.resend_verification_email, name="resend_verification"),


]

