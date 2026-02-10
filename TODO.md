# TODO: Replace Email Verification Link with OTP Code

## Completed Tasks
- [x] Create TODO.md file
- [x] Update EmailVerification model in models.py (change token to code, add generation method)
- [x] Create migration for model change
- [x] Add CodeVerificationForm in forms.py
- [x] Update send_welcome_email in utils.py to send code
- [x] Update welcome_verify.html template to display code
- [x] Update email_verification_sent.html template to mention code
- [x] Update verify_email view in views.py to accept code input via form
- [x] Update register_view in views.py to send code
- [x] Update resend_verification_email in views.py to send code
- [x] Update urls.py to remove token parameter from verify_email URL
- [x] Create verify_email.html template

## Pending Tasks
- [ ] Set up SendGrid account and API key
- [ ] Update DEFAULT_FROM_EMAIL with verified sender email
- [ ] Test email sending with SendGrid
