from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Ticket, Comment, EmailVerification
from .models import EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

    def has_delete_permission(self, request, obj=None):
        # Prevent admin from deleting himself
        if obj and obj == request.user:
            return False
        return request.user.is_superuser


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at', 'closed_at')
    fieldsets = (
        ('Ticket Information', {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at', 'closed_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'is_system_message', 'created_at')
    list_filter = ('is_system_message', 'created_at')
    search_fields = ('content', 'ticket__title', 'author__username')

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at']
    list_filter = ['created_at']  # cannot use expires_at here
admin.site.register(EmailVerification, EmailVerificationAdmin)



