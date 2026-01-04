import os
import django
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from tickets.models import EmailVerification

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_system.settings')
django.setup()

User = get_user_model()

def test_admin_registration_email():
    """Test that admin registration sends verification email"""
    client = Client()

    # Test data for admin user
    data = {
        'username': 'testadmin',
        'email': 'test@example.com',
        'full_name': 'Test Admin',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'role': 'admin'
    }

    # Make POST request to register
    response = client.post('/register/', data)

    # Check if registration was successful (should redirect or show success)
    print(f"Registration response status: {response.status_code}")

    # Check if user was created
    user = User.objects.filter(username='testadmin').first()
    if user:
        print(f"User created: {user.username}, email: {user.email}, is_active: {user.is_active}")

        # Check if EmailVerification was created
        verification = EmailVerification.objects.filter(user=user).first()
        if verification:
            print(f"EmailVerification created with token: {verification.token}")
        else:
            print("No EmailVerification found")
    else:
        print("User not created")

if __name__ == '__main__':
    test_admin_registration_email()
