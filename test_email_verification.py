import os
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tickets.models import EmailVerification

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_system.settings')
django.setup()

User = get_user_model()

def test_email_verification_for_all_users():
    """Test that email verification is required for all user roles"""
    client = Client()

    # Test data for different user roles
    test_users = [
        {
            'username': 'testadmin',
            'email': 'admin@test.com',
            'full_name': 'Test Admin',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'admin'
        },
        {
            'username': 'teststaff',
            'email': 'staff@test.com',
            'full_name': 'Test Staff',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'it_staff'
        },
        {
            'username': 'testemployee',
            'email': 'employee@test.com',
            'full_name': 'Test Employee',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'employee'
        }
    ]

    for user_data in test_users:
        print(f"\n--- Testing {user_data['role']} registration ---")

        # Make POST request to register
        response = client.post('/register/', user_data)
        print(f"Registration response status: {response.status_code}")

        # Check if user was created
        user = User.objects.filter(username=user_data['username']).first()
        if user:
            print(f"✓ User created: {user.username}, email: {user.email}, is_active: {user.is_active}, role: {user.role}")

            # Check if EmailVerification was created
            verification = EmailVerification.objects.filter(user=user).first()
            if verification:
                print(f"✓ EmailVerification created with token: {verification.token}")

                # Test login attempt (should fail)
                login_response = client.post('/login/', {
                    'username': user_data['username'],
                    'password': 'testpass123'
                })
                print(f"Login attempt status: {login_response.status_code}")
                if login_response.status_code == 200 and 'Invalid username or password' in str(login_response.content):
                    print("✓ Login correctly blocked for unverified user")
                else:
                    print("✗ Login was not blocked for unverified user")

                # Simulate email verification
                verify_url = f"/verify-email/{verification.token}/"
                verify_response = client.get(verify_url)
                print(f"Verification response status: {verify_response.status_code}")

                # Refresh user from database
                user.refresh_from_db()
                print(f"After verification - is_active: {user.is_active}")

                # Test login after verification
                login_response2 = client.post('/login/', {
                    'username': user_data['username'],
                    'password': 'testpass123'
                })
                print(f"Login after verification status: {login_response2.status_code}")
                if login_response2.status_code == 302:  # Redirect to dashboard
                    print("✓ Login successful after verification")
                else:
                    print("✗ Login failed after verification")

            else:
                print("✗ No EmailVerification found")
        else:
            print("✗ User not created")

        # Clean up
        if user:
            user.delete()

if __name__ == '__main__':
    test_email_verification_for_all_users()
