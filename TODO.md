# Email Verification for All Users

## Tasks
- [ ] Modify register_view in tickets/views.py to require email verification for all users
- [ ] Set user.is_active = False for all users initially
- [ ] Create EmailVerification for all users during registration
- [ ] Call send_welcome_email for all users
- [ ] Update registration flow to show verification sent page for all users
- [ ] Test registration process for different user roles
- [ ] Verify emails are sent to all users
- [ ] Confirm users cannot login until email is verified
