# 📧📱 KeyHound Notification Setup Guide

## 🚨 **FOUND ADDRESSES WITH BALANCES**

Based on the latest scan, KeyHound found **2 addresses** with unexpected balances:

### **Address #1 - Challenge #69**
- **Address**: `1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3`
- **Current Balance**: **$61.09** (0.0005379 BTC)
- **Original Prize**: 6.9 BTC
- **Solved Date**: 2023-05-15
- **Status**: ⚠️ **HAS BALANCE** - This is unexpected!

### **Address #2 - Challenge #71**
- **Address**: `1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2`
- **Current Balance**: **$564.42** (0.00496944 BTC)
- **Original Prize**: 7.1 BTC
- **Solved Date**: 2023-08-15
- **Status**: ⚠️ **HAS BALANCE** - This is unexpected!

**Total Value Found**: **$625.51** (0.00550734 BTC)

---

## 📧 **EMAIL NOTIFICATION SETUP**

### **Step 1: Gmail App Password**
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. **Security** → **2-Step Verification** (enable if not already)
3. **App passwords** → **Generate**
4. Select **"Mail"** and generate password
5. Copy the **16-character password**

### **Step 2: Set Environment Variables**
Add to your `.env` file or set as environment variables:

```bash
# Email Configuration
SMTP_PASSWORD=your_16_character_gmail_app_password
```

### **Step 3: Pre-configured Email Settings**
The following are already configured:
- **SMTP Server**: smtp.gmail.com
- **Port**: 587
- **From Email**: lightspeedup.smtp@gmail.com
- **Admin Email**: sethpizzaboy@gmail.com
- **Friend Email**: ddeturk@gmail.com

---

## 📱 **SMS NOTIFICATION SETUP**

### **Step 1: Twilio Account**
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your **Account SID** and **Auth Token**
3. Buy a phone number for SMS

### **Step 2: Install Twilio Library**
```bash
pip install twilio
```

### **Step 3: Set Environment Variables**
```bash
# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=+1234567890  # Your Twilio phone number
ADMIN_PHONE=+1234567890   # Your phone number to receive SMS
```

---

## 🔗 **WEBHOOK NOTIFICATION SETUP**

### **Step 1: Slack Webhook**
1. Go to your Slack workspace
2. **Apps** → **Incoming Webhooks**
3. Create webhook for your channel
4. Copy the webhook URL

### **Step 2: Discord Webhook**
1. Go to your Discord server
2. **Server Settings** → **Integrations** → **Webhooks**
3. Create webhook
4. Copy the webhook URL

### **Step 3: Set Environment Variable**
```bash
# Webhook Configuration
WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
# OR
WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/DISCORD/WEBHOOK
```

---

## 🧪 **TEST NOTIFICATIONS**

### **Run the Working Notification System**
```bash
cd KeyHound
python core/working_notification_system.py
```

This will:
1. ✅ Test email notifications to both admin and friend
2. ✅ Test SMS notifications to admin phone
3. ✅ Test webhook notifications to Slack/Discord
4. ✅ Send notifications for the 2 found addresses

### **Expected Results**
If configured correctly, you should receive:
- **2 emails** (admin + friend) for each found address
- **2 SMS messages** (admin phone) for each found address  
- **2 webhook messages** (Slack/Discord) for each found address

---

## 📊 **FOUND ADDRESSES LOCATION**

### **JSON Results Files**
Found addresses are saved in these files:
- `KeyHound/bitcoin_challenge_monitor_20251013_234038.json` (latest)
- `KeyHound/bitcoin_challenge_monitor_20251013_233743.json` (previous)

### **Key Information**
- **Addresses**: The Bitcoin addresses with balances
- **Balances**: Current BTC and USD values
- **Original Prizes**: What the challenges originally offered
- **Status**: Whether notifications were triggered
- **Timestamps**: When the addresses were checked

---

## 🔍 **WHAT THIS MEANS**

### **Monitoring vs Solving**
- These are **monitoring** addresses, not **solved** addresses
- We're checking if previously solved challenges have unexpected balances
- The **private keys** for these addresses are **unknown** to us
- We're **monitoring** for security research purposes

### **Why Balances Exist**
Possible reasons for unexpected balances:
1. **Transaction fees** left behind
2. **Dust attacks** (small amounts sent to addresses)
3. **Mining rewards** sent to old addresses
4. **Other activity** on these addresses

### **Next Steps**
1. **Set up notifications** to get real-time alerts
2. **Investigate** why these addresses have balances
3. **Monitor** for new activity on these addresses
4. **Research** the Bitcoin challenge ecosystem

---

## 🚀 **QUICK START**

### **1. Email Only (Easiest)**
```bash
# Set email password
export SMTP_PASSWORD="your_gmail_app_password"

# Test notifications
python core/working_notification_system.py
```

### **2. Email + SMS (Recommended)**
```bash
# Set all variables
export SMTP_PASSWORD="your_gmail_app_password"
export TWILIO_ACCOUNT_SID="your_twilio_sid"
export TWILIO_AUTH_TOKEN="your_twilio_token"
export TWILIO_PHONE="+1234567890"
export ADMIN_PHONE="+1234567890"

# Install Twilio
pip install twilio

# Test notifications
python core/working_notification_system.py
```

### **3. Full Setup (Email + SMS + Webhook)**
```bash
# Set all variables
export SMTP_PASSWORD="your_gmail_app_password"
export TWILIO_ACCOUNT_SID="your_twilio_sid"
export TWILIO_AUTH_TOKEN="your_twilio_token"
export TWILIO_PHONE="+1234567890"
export ADMIN_PHONE="+1234567890"
export WEBHOOK_URL="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

# Install dependencies
pip install twilio

# Test notifications
python core/working_notification_system.py
```

---

## ✅ **SUCCESS INDICATORS**

You'll know it's working when you receive:
- **Email notifications** in your inbox
- **SMS messages** on your phone
- **Slack/Discord messages** in your channel
- **Console output** showing "SUCCESS" messages

The system will send notifications for the **2 found addresses** with balances totaling **$625.51**.
