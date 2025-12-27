from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """
    Custom User model with role-based access and extended profile info.

    Authentication is tied to email verification via the is_active flag.
    """

    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('it_staff', 'IT Staff'),
        ('hr', 'HR'),
        ('admin', 'Administrator'),
    ]

    # Make email required & unique at the DB level
    email = models.EmailField(unique=True)

    # Additional profile fields
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_employee(self):
        return self.role == 'employee'

    def is_it_staff(self):
        return self.role == 'it_staff'

    def is_hr(self):
        return self.role == 'hr'

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def display_name(self):
        """Prefer full_name, then first/last, then username."""
        if self.full_name:
            return self.full_name
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username


class Ticket(models.Model):
    """Support Ticket model"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def update_status(self, new_status, user):
        """Update ticket status and track timestamps"""
        old_status = self.status
        self.status = new_status
        
        if new_status == 'resolved' and old_status != 'resolved':
            self.resolved_at = timezone.now()
        elif new_status == 'closed' and old_status != 'closed':
            self.closed_at = timezone.now()
        
        self.save()
        
        # Create a comment for status change
        Comment.objects.create(
            ticket=self,
            author=user,
            content=f"Status changed from {Ticket.get_status_display_from_value(old_status)} to {self.get_status_display()}",
            is_system_message=True
        )
    
    @staticmethod
    def get_status_display_from_value(value):
        """Helper to get display name from status value"""
        for choice in Ticket.STATUS_CHOICES:
            if choice[0] == value:
                return choice[1]
        return value


class Comment(models.Model):
    """Comments on tickets"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_system_message = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.ticket.title}"


# ================= EMAIL VERIFICATION MODEL =================
import uuid
from django.utils.timezone import now, timedelta

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return now() > self.created_at + timedelta(hours=24)

    @property
    def expires_at(self):
        return self.created_at + timedelta(hours=24)


