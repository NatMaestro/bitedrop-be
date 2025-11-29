# Resend Setup Guide for BiteDrop

## 🚀 **Quick Setup (3 minutes)**

### Step 1: Create Resend Account

1. Go to [resend.com](https://resend.com)
2. Sign up for free account (3,000 emails/month free)
3. Verify your email address

### Step 2: Get API Key

1. **Login to Resend Dashboard**
2. **Go to API Keys section**
3. **Click "Create API Key"**
4. **Copy your API key** (starts with `re_`)

### Step 3: Add Domain (Optional)

1. **Go to Domains section**
2. **Add your domain** (e.g., `bitedrop.com`)
3. **Add DNS records** as instructed
4. **Verify domain** (takes a few minutes)

### Step 4: Update Render.com Environment Variables

In your Render.com dashboard, add these environment variables:

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

**Note**: Replace `re_your-api-key-here` with your actual Resend API key.

### Step 5: Test Email Sending

1. **Deploy to Render.com**
2. **Create a test user** through your app
3. **Check Resend dashboard** for email logs
4. **Check user's inbox** for welcome email

## 🎯 **Why Resend is Great for Developers**

- ✅ **Simple setup**: Just an API key, no complex SMTP config
- ✅ **Great deliverability**: Emails reach inbox, not spam
- ✅ **Developer-friendly**: Clean API and dashboard
- ✅ **Free tier**: 3,000 emails/month
- ✅ **Fast**: Optimized for cloud platforms
- ✅ **Reliable**: Built specifically for developers

## 📧 **Resend Dashboard Features**

- **Email Logs**: See all sent emails in real-time
- **Delivery Stats**: Track delivery rates and bounces
- **API Usage**: Monitor your email usage
- **Webhooks**: Get real-time delivery notifications
- **Domains**: Manage your sending domains

## 🔧 **Environment Variables Reference**

```bash
# Required
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=re_your-api-key-here

# Optional
DEFAULT_FROM_EMAIL=noreply@bitedrop.com
EMAIL_DEBUG=True
```

## 🚨 **Troubleshooting**

### Issue: "Authentication failed"

- ✅ Check API key format: should start with `re_`
- ✅ Ensure API key is copied correctly (no extra spaces)
- ✅ Verify API key is active in Resend dashboard

### Issue: "Domain not verified"

- ✅ Use default Resend domain for testing
- ✅ Add and verify custom domain for production
- ✅ Wait for DNS propagation (up to 24 hours)

### Issue: Emails going to spam

- ✅ Add SPF record: `v=spf1 include:_spf.resend.com ~all`
- ✅ Add DKIM record (provided by Resend)
- ✅ Set up DMARC policy

## 💰 **Pricing**

- **Free Tier**: 3,000 emails/month
- **Pro Plan**: $20/month for 50,000 emails
- **No credit card required** for free tier

## 🔄 **Migration from Gmail/Mailgun**

If you're migrating from another email service:

1. **Keep old service running** during transition
2. **Set up Resend** with new environment variables
3. **Test thoroughly** before switching
4. **Monitor delivery** in Resend dashboard
5. **Update DNS records** if using custom domain

## 📞 **Support**

- **Resend Documentation**: [resend.com/docs](https://resend.com/docs)
- **Resend Support**: Available through dashboard
- **Discord Community**: [discord.gg/resend](https://discord.gg/resend)

## 🎉 **Next Steps**

1. **Sign up for Resend** (2 minutes)
2. **Get your API key** (1 minute)
3. **Update Render.com environment variables**
4. **Deploy and test email sending**
5. **Monitor email delivery** in Resend dashboard

**Resend is the perfect email service for BiteDrop - simple, reliable, and developer-friendly!** 🚀

