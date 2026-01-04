import requests
import time
import re

BASE_URL = "http://127.0.0.1:8000"

def test_registration_and_verification():
    """Manually test the email verification process"""

    print("=== Testing Email Verification for All Users ===\n")

    # Test data
    user_data = {
        'username': 'testuser123',
        'email': 'testuser123@example.com',
        'full_name': 'Test User',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'role': 'employee'  # Test with employee role
    }

    # Step 1: Register a new user
    print("1. Registering new user...")
    session = requests.Session()

    # Get CSRF token first
    response = session.get(f"{BASE_URL}/register/")
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)

    if not csrf_token:
        print("❌ Could not get CSRF token")
        return

    # Add CSRF token to data
    user_data['csrfmiddlewaretoken'] = csrf_token

    # Register the user
    response = session.post(f"{BASE_URL}/register/", data=user_data)
    print(f"Registration response status: {response.status_code}")

    if response.status_code == 200:
        if "email_verification_sent" in response.url or "Verification email sent" in response.text:
            print("✅ Registration successful - verification email sent")
        else:
            print("❌ Registration may have failed - check response")
            print("Response content:", response.text[:500])
            return
    else:
        print(f"❌ Registration failed with status {response.status_code}")
        return

    # Step 2: Check console for email (we can't directly access it, but we know it's sent)
    print("\n2. Check the Django console for the verification email content")
    print("   The email should contain a verification link like:")
    print("   http://127.0.0.1:8000/verify-email/[token]/")

    # For manual testing, we'll simulate finding the token
    print("\n3. MANUAL STEP: Copy the verification URL from the console and paste it here")
    verify_url = input("Enter the verification URL: ").strip()

    if verify_url:
        # Step 3: Verify the email
        print("4. Verifying email...")
        response = session.get(verify_url)
        print(f"Verification response status: {response.status_code}")

        if response.status_code == 200 and "verified_success" in response.url:
            print("✅ Email verification successful")
        else:
            print("❌ Email verification failed")
            print("Response content:", response.text[:500])

        # Step 4: Try logging in
        print("\n5. Testing login after verification...")
        login_data = {
            'username': user_data['username'],
            'password': 'testpass123',
            'csrfmiddlewaretoken': csrf_token
        }

        response = session.post(f"{BASE_URL}/login/", data=login_data)
        print(f"Login response status: {response.status_code}")

        if response.status_code == 302 and 'dashboard' in response.headers.get('Location', ''):
            print("✅ Login successful after verification")
        else:
            print("❌ Login failed after verification")
            print("Response content:", response.text[:500])
    else:
        print("Skipping verification test - no URL provided")

    print("\n=== Test Complete ===")

if __name__ == '__main__':
    test_registration_and_verification()
