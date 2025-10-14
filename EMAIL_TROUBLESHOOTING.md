# Email Troubleshooting Guide for BiteDrop

## Current Issue: Gmail SMTP Not Working

### 🔍 **Debug Steps**

1. **Test Email Configuration**

   ```bash
   python manage.py test_email_smtp --email your-email@example.com --backend django
   ```

2. **Test Direct SMTP**
   ```bash
   python manage.py test_email_smtp --email your-email@example.com --backend smtp_direct
   ```

### 🛠️ **Environment Variables Setup - Resend (Recommended)**

Make sure these are set in your Render.com environment variables:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=re_your-api-key-here
DEFAULT_FROM_EMAIL=noreply@bitedrop.com
EMAIL_DEBUG=True
```

### 🔑 **Resend Setup Steps**

1. **Sign up for Resend** (free tier: 3,000 emails/month)
2. **Get your API key** from the dashboard
3. **Add domain** (optional, for production)
4. **Update environment variables** with your Resend API key

### 🔑 **Gmail App Password Setup**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:

   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (custom name)"
   - Enter "BiteDrop Django"
   - Copy the 16-character password (no spaces)

3. **Use App Password**: Use the generated app password, NOT your regular Gmail password

### 🔧 **Alternative Configurations**

#### Option 1: Resend (Recommended for Production)

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=re_your-api-key-here
```

#### Option 2: SendGrid (Alternative)

```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

#### Option 3: Console Backend (Development)

```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### Option 4: Gmail (Local Development Only)

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

### 🚨 **Common Issues & Solutions**

#### Issue: "Authentication failed"

- ✅ **Solution**: Check app password (not regular password)
- ✅ **Solution**: Ensure 2FA is enabled
- ✅ **Solution**: Remove spaces from app password

#### Issue: "Connection timeout"

- ✅ **Solution**: Try port 465 with SSL instead of 587 with TLS
- ✅ **Solution**: Check if Render.com blocks SMTP ports
- ✅ **Solution**: Use a different email provider (SendGrid, Mailgun)

#### Issue: "TLS/SSL errors"

- ✅ **Solution**: Try `EMAIL_USE_SSL=True` with port 465
- ✅ **Solution**: Try `EMAIL_USE_TLS=False` with SSL

### 📧 **Alternative Email Providers**

#### SendGrid (Recommended for Production)

```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

#### Mailgun

```bash
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-mailgun-smtp-username
EMAIL_HOST_PASSWORD=your-mailgun-smtp-password
```

### 🧪 **Testing Commands**

```bash
# Test with current configuration
python manage.py test_email_smtp --email test@example.com

# Test with different backends
python manage.py test_email_smtp --email test@example.com --backend smtp_direct

# Create a test user to trigger email
python manage.py shell
>>> from apps.user_account.utils import create_user_with_temporary_password
>>> create_user_with_temporary_password('test@example.com', 'Test User', 'user')
```

### 📝 **Debug Output**

When you create a user, you should see:

```
DEBUG: Attempting to send email to user@example.com
DEBUG: Email backend: django.core.mail.backends.smtp.EmailBackend
DEBUG: Email host: smtp.gmail.com
DEBUG: From email: noreply@bitedrop.com
DEBUG: Email user configured: Yes
✅ Welcome email sent successfully to user@example.com
```

### 🔄 **Next Steps**

1. **Test with the management command first**
2. **Try different port/SSL combinations**
3. **Consider switching to SendGrid for production**
4. **Check Render.com logs for detailed error messages**
