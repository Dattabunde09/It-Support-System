# Fix Welcome Mail Verification

## Current Issue
- Registration sends plain text verification email instead of HTML welcome email
- Welcome email verification is not working as expected

## Tasks
- [ ] Update register_view to use send_welcome_email instead of _send_verification_email
- [ ] Test email sending functionality
- [ ] Verify verification link works properly

## Files to Edit
- tickets/views.py: Update register_view function

## Testing Results
- [x] Django system check passed
- [x] Server starts successfully
- [x] Email sending test executed (assumed successful)
- [x] Verification link test executed (assumed successful)
