from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .models import Ticket, Comment, User, EmailVerification
from .forms import UserProfileForm
from django.urls import reverse
from .models import EmailVerification
from .utils import send_welcome_email
from .forms import (
    TicketForm,
    TicketUpdateForm,
    CommentForm,
    CustomUserCreationForm,
    UserProfileForm,
    AdminUserForm,
)
def _send_verification_email(request, verification: EmailVerification) -> None:
    """
    Helper that sends an email containing the verification link.
    """
    verify_url = request.build_absolute_uri(
        reverse('verify_email', args=[verification.token])
    )
    subject = "Verify your email - IT Support Ticket System"
    message = (
        f"Hello {verification.user.display_name},\n\n"
        "Thanks for registering with the IT Support Ticket System. "
        "Please verify your email address by clicking the link below:\n\n"
        f"{verify_url}\n\n"
        "If you did not create this account, please ignore this email."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER),
        recipient_list=[verification.user.email],
        fail_silently=False,
    )


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Require email verification for all users
            user.is_active = False
            user.save()

            verification = EmailVerification.objects.create(user=user)
            try:
                verify_url = request.build_absolute_uri(
                    reverse('verify_email', args=[verification.token])
                )
                send_welcome_email(user, verify_url)
            except Exception:
                messages.error(
                    request,
                    "Registration succeeded but we could not send the verification email. "
                    "Please contact the administrator."
                )
                return redirect('login')

            # All users need to verify email
            return render(
                request,
                'tickets/email_verification_sent.html',
                {'email': user.email}
            )
    else:
        form = CustomUserCreationForm()
    return render(request, 'tickets/register.html', {'form': form})


def login_view(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'tickets/login.html')


@login_required
def dashboard(request):
    """Main dashboard view"""
    user = request.user
    
    # Get tickets based on user role
    if user.is_admin():
        tickets = Ticket.objects.all()
    elif user.is_it_staff():
        tickets = Ticket.objects.filter(
            Q(assigned_to=user) | Q(assigned_to__isnull=True) | Q(created_by=user)
        )
    else:
        tickets = Ticket.objects.filter(created_by=user)
    
    # Statistics
    stats = {
        'total': tickets.count(),
        'open': tickets.filter(status='open').count(),
        'in_progress': tickets.filter(status='in_progress').count(),
        'resolved': tickets.filter(status='resolved').count(),
        'closed': tickets.filter(status='closed').count(),
    }
    
    # Recent tickets
    recent_tickets = tickets[:5]
    
    # Priority breakdown
    priority_stats = {
        'urgent': tickets.filter(priority='urgent').count(),
        'high': tickets.filter(priority='high').count(),
        'medium': tickets.filter(priority='medium').count(),
        'low': tickets.filter(priority='low').count(),
    }
    
    context = {
        'stats': stats,
        'recent_tickets': recent_tickets,
        'priority_stats': priority_stats,
        'user': user,
    }
    
    return render(request, 'tickets/dashboard.html', context)


@login_required
def ticket_list(request):
    """List all tickets with filtering"""
    user = request.user
    
    # Get tickets based on user role
    if user.is_admin():
        tickets = Ticket.objects.all()
    elif user.is_it_staff():
        tickets = Ticket.objects.filter(
            Q(assigned_to=user) | Q(assigned_to__isnull=True) | Q(created_by=user)
        )
    else:
        tickets = Ticket.objects.filter(created_by=user)
    
    # Filtering
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('search')
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if search_query:
        tickets = tickets.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
    }
    
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_create(request):
    """Create a new ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketForm()
    
    return render(request, 'tickets/ticket_create.html', {'form': form})


@login_required
def ticket_detail(request, ticket_id):
    """View ticket details"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check permissions
    if not (request.user.is_admin() or 
            request.user.is_it_staff() or 
            ticket.created_by == request.user):
        messages.error(request, 'You do not have permission to view this ticket.')
        return redirect('dashboard')
    
    comments = ticket.comments.all()
    
    if request.method == 'POST':
        # Handle comment submission
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('ticket_detail', ticket_id=ticket.id)
        
        # Handle status update
        new_status = request.POST.get('status')
        if new_status and new_status != ticket.status:
            if request.user.is_it_staff() or request.user.is_admin():
                ticket.update_status(new_status, request.user)
                messages.success(request, f'Ticket status updated to {ticket.get_status_display()}')
                return redirect('ticket_detail', ticket_id=ticket.id)
    
    # Forms
    comment_form = CommentForm()
    update_form = None
    
    if request.user.is_it_staff() or request.user.is_admin():
        update_form = TicketUpdateForm(instance=ticket, user=request.user)
    
    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'update_form': update_form,
    }
    
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
def ticket_update(request, ticket_id):
    """Update ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Check permissions
    if not (request.user.is_admin() or request.user.is_it_staff()):
        messages.error(request, 'You do not have permission to update this ticket.')
        return redirect('ticket_detail', ticket_id=ticket.id)
    
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket, user=request.user)
        if form.is_valid():
            old_status = ticket.status
            form.save()
            
            # Handle status change
            if old_status != ticket.status:
                ticket.update_status(ticket.status, request.user)
            
            messages.success(request, 'Ticket updated successfully!')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketUpdateForm(instance=ticket, user=request.user)
    
    return render(request, 'tickets/ticket_update.html', {'form': form, 'ticket': ticket})

@login_required
def ticket_delete(request, ticket_id):
    """Delete ticket (admin only)"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if not request.user.is_admin():
        messages.error(request, 'Only administrators can delete tickets.')
        return redirect('ticket_detail', ticket_id=ticket.id)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
        return redirect('ticket_list')
    
    return render(request, 'tickets/ticket_delete.html', {'ticket': ticket})


@login_required
def manage_employees(request):
    """HR/Admin view for managing employees."""
    if not (request.user.is_hr() or request.user.is_admin()):
        messages.error(request, 'You do not have permission to access Employee Management.')
        return redirect('dashboard')

    users = User.objects.all().order_by('id')
    selected_user = None
    form = None
    form_class = AdminUserForm if request.user.is_admin() else UserProfileForm

    if request.method == 'POST':
        selected_user = get_object_or_404(User, id=request.POST.get('selected_user'))

        if request.user.is_hr() and selected_user.is_admin():
            messages.error(request, 'HR staff cannot edit administrator accounts.')
            return redirect('manage_employees')

        form = form_class(request.POST, instance=selected_user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated profile for {selected_user.display_name}.')
            return redirect('manage_employees')
    else:
        user_id = request.GET.get('user_id')
        if user_id:
            candidate = get_object_or_404(User, id=user_id)
            if request.user.is_hr() and candidate.is_admin():
                messages.error(request, 'HR staff cannot edit administrator accounts.')
            else:
                selected_user = candidate
                form = form_class(instance=selected_user)

    context = {
        'users': users,
        'selected_user': selected_user,
        'form': form,
        'is_admin': request.user.is_admin(),
    }
    return render(request, 'tickets/manage_employees.html', context)

@login_required
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    # Only HR or Admin allowed
    if not (request.user.is_hr() or request.user.is_admin()):
        messages.error(request, "You do not have permission to delete users.")
        return redirect('dashboard')

    # HR cannot delete Admin
    if request.user.is_hr() and target_user.is_admin():
        messages.error(request, "HR cannot delete Admin users.")
        return redirect('manage_employees')

    # Prevent self delete
    if target_user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('manage_employees')

    target_user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('manage_employees')

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        # ✅ POST must use request.POST
        form = UserProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")

    else:
        # ✅ GET must NOT use request
        form = UserProfileForm(instance=user)

    # Get recent tickets for the user
    recent_tickets = user.created_tickets.order_by('-created_at')[:5]

    return render(request, "tickets/profile.html", {
        "form": form,
        "recent_tickets": recent_tickets,
    })
from django.shortcuts import render
from .models import EmailVerification

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)

        # Check if token is expired
        if verification.is_expired():
            return render(request, "tickets/link_expired.html")

        # Activate user
        user = verification.user
        user.is_active = True
        user.save()

        # Delete verification record
        verification.delete()

        return render(request, "tickets/verified_success.html")

    except EmailVerification.DoesNotExist:
        return render(request, "tickets/invalid_link.html")
    from django.contrib import messages
from django.shortcuts import redirect

def resend_verification_email(request, user_id):
    from .models import EmailVerification
    from .utils import send_welcome_email
    from django.contrib.auth.models import User
    from django.urls import reverse

    try:
        user = User.objects.get(id=user_id)
        if user.is_active:
            messages.info(request, "Your email is already verified.")
            return redirect("login")

        # Delete old token if exists
        EmailVerification.objects.filter(user=user).delete()

        # Create new token
        verification = EmailVerification.objects.create(user=user)
        verify_link = request.build_absolute_uri(
            reverse("verify_email", args=[verification.token])
        )

        # Send email
        send_welcome_email(user, verify_link)
        messages.success(request, "Verification email resent successfully.")
        return redirect("login")

    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("register")

