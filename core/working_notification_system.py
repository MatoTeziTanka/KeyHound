#!/usr/bin/env python3
"""
KeyHound Enhanced - Working Notification System
Actually sends email and SMS notifications for found addresses.
"""

import os
import sys
import smtplib
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class WorkingNotificationSystem:
    """Actually sends email and SMS notifications."""
    
    def __init__(self):
        # Email configuration (using your existing setup from FamilyFork)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = "lightspeedup.smtp@gmail.com"
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        # Recipients
        # Comma-separated list in ALERT_EMAILS env var overrides defaults
        default_recipients = [
            "sethpizzaboy@aol.com",
            "sethpizzaboy@gmail.com",
            "setsch0666@students.ecpi.edu",
        ]
        env_recipients = os.environ.get('ALERT_EMAILS', '')
        if env_recipients.strip():
            self.recipients = [e.strip() for e in env_recipients.split(',') if e.strip()]
        else:
            self.recipients = default_recipients
        
        # SMS configuration (Twilio)
        self.twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
        self.twilio_phone = os.environ.get('TWILIO_PHONE', '')
        self.admin_phone = os.environ.get('ADMIN_PHONE', '')
        
        print(f"Working Notification System initialized")
        print(f"Email: {'Configured' if self.smtp_password else 'NOT CONFIGURED'}")
        print(f"SMS: {'Configured' if self.twilio_account_sid else 'NOT CONFIGURED'}")
    
    def send_email_notification(self, subject: str, body: str, to_email: str = None) -> bool:
        """Actually send email notification."""
        if not self.smtp_password:
            print(f"[EMAIL] ERROR: SMTP_PASSWORD not configured")
            print(f"[EMAIL] Please set SMTP_PASSWORD environment variable")
            return False
        
        if to_email is None:
            # Send to all configured recipients
            results = []
            for addr in self.recipients:
                results.append(self.send_email_notification(subject, body, to_email=addr))
            # If any succeeded, return True
            return any(results)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            print(f"[EMAIL] SUCCESS: Email sent to {to_email}")
            print(f"[EMAIL] Subject: {subject}")
            return True
            
        except Exception as e:
            print(f"[EMAIL] ERROR: Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_sms_notification(self, message: str, to_phone: str = None) -> bool:
        """Actually send SMS notification using Twilio."""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone]):
            print(f"[SMS] ERROR: Twilio not configured")
            print(f"[SMS] Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE environment variables")
            return False
        
        if to_phone is None:
            to_phone = self.admin_phone
        
        if not to_phone:
            print(f"[SMS] ERROR: ADMIN_PHONE not configured")
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=to_phone
            )
            
            print(f"[SMS] SUCCESS: SMS sent to {to_phone}")
            print(f"[SMS] Message: {message}")
            print(f"[SMS] Twilio SID: {message_obj.sid}")
            return True
            
        except ImportError:
            print(f"[SMS] ERROR: Twilio library not installed")
            print(f"[SMS] Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"[SMS] ERROR: Failed to send SMS to {to_phone}: {str(e)}")
            return False
    
    def send_webhook_notification(self, payload: Dict, webhook_url: str = None) -> bool:
        """Send webhook notification to Slack/Discord."""
        if not webhook_url:
            webhook_url = os.environ.get('WEBHOOK_URL', '')
        
        if not webhook_url:
            print(f"[WEBHOOK] ERROR: WEBHOOK_URL not configured")
            return False
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print(f"[WEBHOOK] SUCCESS: Webhook sent to {webhook_url}")
                return True
            else:
                print(f"[WEBHOOK] ERROR: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[WEBHOOK] ERROR: Failed to send webhook: {str(e)}")
            return False
    
    def notify_found_address(self, address_info: Dict[str, Any]) -> Dict[str, bool]:
        """Send all notifications for a found address."""
        print(f"\n[ALERT] SENDING NOTIFICATIONS FOR FOUND ADDRESS!")
        print(f"Address: {address_info['address']}")
        print(f"Balance: ${address_info['current_balance_usd']:,.2f} ({address_info['current_balance_btc']:.8f} BTC)")
        
        # Prepare notification content
        subject = f"[ALERT] KeyHound Alert: {address_info['puzzle']} Address Has Balance!"
        
        email_body = f"""
[ALERT] BITCOIN CHALLENGE ADDRESS ALERT!

Puzzle: {address_info['puzzle']} ({address_info['bits']}-bit)
Address: {address_info['address']}
Current Balance: ${address_info['current_balance_usd']:,.2f} ({address_info['current_balance_btc']:.8f} BTC)
Original Prize: {address_info['original_prize_btc']} BTC
Solved Date: {address_info['solved_date']}
Check Time: {address_info['check_timestamp']}

[WARNING] This address was previously solved but now has a balance!
[ACTION] Please investigate immediately.

KeyHound Enhanced Challenge Monitor
        """.strip()
        
        sms_message = f"[ALERT] KeyHound Alert: {address_info['puzzle']} address has ${address_info['current_balance_usd']:,.2f} balance! Address: {address_info['address'][:20]}... Check email for details."
        
        webhook_payload = {
            "text": f"[ALERT] KeyHound Alert: {address_info['puzzle']} Address Has Balance!",
            "attachments": [
                {
                    "color": "danger",
                    "fields": [
                        {"title": "Puzzle", "value": f"{address_info['puzzle']} ({address_info['bits']}-bit)", "short": True},
                        {"title": "Address", "value": address_info['address'], "short": False},
                        {"title": "Current Balance", "value": f"${address_info['current_balance_usd']:,.2f}", "short": True},
                        {"title": "BTC Balance", "value": f"{address_info['current_balance_btc']:.8f} BTC", "short": True},
                        {"title": "Original Prize", "value": f"{address_info['original_prize_btc']} BTC", "short": True},
                        {"title": "Solved Date", "value": address_info['solved_date'], "short": True}
                    ]
                }
            ]
        }
        
        # Send notifications
        results = {}
        # Send email to all configured recipients
        results['email_all'] = self.send_email_notification(subject, email_body)
        results['sms'] = self.send_sms_notification(sms_message, self.admin_phone)
        results['webhook'] = self.send_webhook_notification(webhook_payload)
        
        # Log results
        successful_notifications = sum(results.values())
        total_notifications = len(results)
        
        print(f"\n[RESULTS] Notification Summary:")
        print(f"   Email (Admin): {'[OK] Sent' if results['email'] else '[FAIL] Failed'}")
        print(f"   Email (Friend): {'[OK] Sent' if results['email_friend'] else '[FAIL] Failed'}")
        print(f"   SMS (Admin): {'[OK] Sent' if results['sms'] else '[FAIL] Failed'}")
        print(f"   Webhook: {'[OK] Sent' if results['webhook'] else '[FAIL] Failed'}")
        print(f"   Success Rate: {successful_notifications}/{total_notifications} ({successful_notifications/total_notifications*100:.1f}%)")
        
        return results

def main():
    """Test the working notification system."""
    print("=" * 80)
    print("KeyHound Enhanced - Working Notification System Test")
    print("=" * 80)
    
    # Initialize notification system
    notifier = WorkingNotificationSystem()
    
    # Test with found addresses from recent scan
    found_addresses = [
        {
            "puzzle": "Challenge #69 (Puzzle #69)",
            "bits": 69,
            "address": "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
            "current_balance_btc": 0.0005379,
            "current_balance_usd": 61.0936062,
            "original_prize_btc": 6.9,
            "solved_date": "2023-05-15",
            "check_timestamp": "2025-10-13T23:40:26.610338"
        },
        {
            "puzzle": "Challenge #71 (Puzzle #71)",
            "bits": 71,
            "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
            "current_balance_btc": 0.00496944,
            "current_balance_usd": 564.41905632,
            "original_prize_btc": 7.1,
            "solved_date": "2023-08-15",
            "check_timestamp": "2025-10-13T23:40:30.326369"
        }
    ]
    
    print(f"\n[INFO] Found {len(found_addresses)} addresses with balances:")
    for addr in found_addresses:
        print(f"   {addr['puzzle']}: ${addr['current_balance_usd']:,.2f} ({addr['current_balance_btc']:.8f} BTC)")
        print(f"   Address: {addr['address']}")
    
    # Send notifications for each found address
    print(f"\n[TEST] Sending notifications for found addresses...")
    all_results = []
    
    for i, address_info in enumerate(found_addresses, 1):
        print(f"\n--- Sending notifications for address {i}/{len(found_addresses)} ---")
        results = notifier.notify_found_address(address_info)
        all_results.append(results)
        
        # Small delay between notifications
        import time
        time.sleep(2)
    
    # Summary
    print(f"\n" + "=" * 80)
    print(f"NOTIFICATION TEST SUMMARY")
    print(f"=" * 80)
    
    total_successful = sum(sum(result.values()) for result in all_results)
    total_attempts = sum(len(result) for result in all_results)
    
    print(f"Total notifications attempted: {total_attempts}")
    print(f"Total notifications successful: {total_successful}")
    print(f"Overall success rate: {total_successful/total_attempts*100:.1f}%")
    
    if total_successful > 0:
        print(f"\n[SUCCESS] NOTIFICATIONS WORKING! You should receive emails and/or SMS messages.")
    else:
        print(f"\n[ERROR] NOTIFICATIONS FAILED! Check configuration:")
        print(f"   - Set SMTP_PASSWORD for email notifications")
        print(f"   - Set TWILIO_* variables for SMS notifications")
        print(f"   - Set WEBHOOK_URL for webhook notifications")
    
    return 0 if total_successful > 0 else 1

if __name__ == '__main__':
    sys.exit(main())
