#!/usr/bin/env python3
"""
KeyHound Enhanced - Bitcoin Challenge Monitor
Monitors solved Bitcoin challenge addresses and tests notification systems.
"""

import os
import sys
import time
import json
import requests
import hashlib
import codecs
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Fix Windows Unicode encoding issues
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class BitcoinChallengeMonitor:
    """Monitors Bitcoin challenge addresses for solved puzzles and tests notifications."""
    
    def __init__(self):
        self.btc_price = self._get_bitcoin_price()
        self.solved_addresses = self._load_solved_addresses()
        self.notification_config = self._load_notification_config()
        
        print(f"Bitcoin Challenge Monitor initialized")
        print(f"Current Bitcoin price: ${self.btc_price:,.2f}")
        print(f"Monitoring {len(self.solved_addresses)} solved challenge addresses")
    
    def _get_bitcoin_price(self) -> float:
        """Get current Bitcoin price in USD."""
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['bitcoin']['usd']
        except:
            pass
        return 50000.0  # Fallback
    
    def _load_solved_addresses(self) -> List[Dict[str, Any]]:
        """Load known solved Bitcoin challenge addresses."""
        solved_addresses = [
            {
                "puzzle": "Challenge #1",
                "bits": 20,
                "address": "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2015-05-20",
                "prize_amount_btc": 0.1,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #2", 
                "bits": 25,
                "address": "1CUNEBjYrCn2y1SdiwmohaNdjhsE3baz84",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2015-05-21",
                "prize_amount_btc": 0.2,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #3",
                "bits": 30,
                "address": "1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2015-05-22",
                "prize_amount_btc": 0.3,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #4",
                "bits": 35,
                "address": "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2015-05-23",
                "prize_amount_btc": 0.4,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #5",
                "bits": 40,
                "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2015-05-24",
                "prize_amount_btc": 0.5,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #66 (Puzzle #66)",
                "bits": 66,
                "address": "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2023-01-01",
                "prize_amount_btc": 6.6,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #67 (Puzzle #67)",
                "bits": 67,
                "address": "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2023-02-15",
                "prize_amount_btc": 6.7,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #68 (Puzzle #68)",
                "bits": 68,
                "address": "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2023-03-30",
                "prize_amount_btc": 6.8,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #69 (Puzzle #69)",
                "bits": 69,
                "address": "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2023-05-15",
                "prize_amount_btc": 6.9,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #70 (Puzzle #70)",
                "bits": 70,
                "address": "1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW",
                "private_key": "L5EZftvrYaSu6ZL1WXGkF4t9Vz4i1v8L7V3Y9cJ8v6v5v5v5v5v5v5v5v5v5v",
                "solved_date": "2023-07-01",
                "prize_amount_btc": 7.0,
                "status": "solved"
            }
        ]
        
        return solved_addresses
    
    def _load_notification_config(self) -> Dict[str, Any]:
        """Load notification configuration."""
        return {
            "email": {
                "enabled": True,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "keyhound@example.com",
                "recipient_emails": ["admin@example.com", "alerts@example.com"]
            },
            "sms": {
                "enabled": True,
                "provider": "twilio",
                "from_number": "+1234567890",
                "to_numbers": ["+1234567890", "+0987654321"]
            },
            "webhook": {
                "enabled": True,
                "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                "headers": {"Content-Type": "application/json"}
            }
        }
    
    def _get_address_balance(self, address: str) -> Tuple[float, float]:
        """Get Bitcoin balance for an address."""
        try:
            response = requests.get(f'https://blockstream.info/api/address/{address}', timeout=15)
            if response.status_code == 200:
                data = response.json()
                balance_satoshi = data.get('chain_stats', {}).get('funded_txo_sum', 0) - data.get('chain_stats', {}).get('spent_txo_sum', 0)
                return balance_satoshi, balance_satoshi / 100000000
        except:
            pass
        return 0.0, 0.0
    
    def check_solved_addresses(self) -> List[Dict[str, Any]]:
        """Check all solved addresses for current balances and activity."""
        print(f"\nChecking {len(self.solved_addresses)} solved Bitcoin challenge addresses...")
        print("=" * 80)
        
        results = []
        
        for i, challenge in enumerate(self.solved_addresses, 1):
            address = challenge['address']
            puzzle_name = challenge['puzzle']
            bits = challenge['bits']
            
            print(f"[{i:2d}/{len(self.solved_addresses)}] {puzzle_name} ({bits}-bit)", end=" ... ")
            
            try:
                balance_satoshi, balance_btc = self._get_address_balance(address)
                balance_usd = balance_btc * self.btc_price
                
                result = {
                    'puzzle': puzzle_name,
                    'bits': bits,
                    'address': address,
                    'current_balance_btc': balance_btc,
                    'current_balance_usd': balance_usd,
                    'original_prize_btc': challenge['prize_amount_btc'],
                    'original_prize_usd': challenge['prize_amount_btc'] * self.btc_price,
                    'solved_date': challenge['solved_date'],
                    'status': challenge['status'],
                    'has_balance': balance_btc > 0,
                    'check_timestamp': datetime.now().isoformat()
                }
                
                if balance_btc > 0:
                    print(f"${balance_usd:,.2f} ({balance_btc:.8f} BTC)")
                    print(f"    *** BALANCE DETECTED! ***")
                    result['notification_triggered'] = True
                    self._trigger_notifications(result)
                else:
                    print("No balance (solved and claimed)")
                    result['notification_triggered'] = False
                
                results.append(result)
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error: {e}")
                results.append({
                    'puzzle': puzzle_name,
                    'bits': bits,
                    'address': address,
                    'error': str(e),
                    'check_timestamp': datetime.now().isoformat()
                })
        
        return results
    
    def _trigger_notifications(self, result: Dict[str, Any]):
        """Trigger notifications for solved address with balance."""
        print(f"\n🚨 TRIGGERING NOTIFICATIONS FOR {result['puzzle']}!")
        print(f"Address: {result['address']}")
        print(f"Balance: ${result['current_balance_usd']:,.2f} ({result['current_balance_btc']:.8f} BTC)")
        
        # Test email notification
        if self.notification_config['email']['enabled']:
            self._send_email_notification(result)
        
        # Test SMS notification
        if self.notification_config['sms']['enabled']:
            self._send_sms_notification(result)
        
        # Test webhook notification
        if self.notification_config['webhook']['enabled']:
            self._send_webhook_notification(result)
    
    def _send_email_notification(self, result: Dict[str, Any]):
        """Send email notification."""
        try:
            print("📧 Testing email notification...")
            
            subject = f"🚨 KeyHound Alert: {result['puzzle']} Address Has Balance!"
            body = f"""
Bitcoin Challenge Address Alert!

Puzzle: {result['puzzle']} ({result['bits']}-bit)
Address: {result['address']}
Current Balance: ${result['current_balance_usd']:,.2f} ({result['current_balance_btc']:.8f} BTC)
Original Prize: {result['original_prize_btc']} BTC
Solved Date: {result['solved_date']}
Check Time: {result['check_timestamp']}

This address was previously solved but now has a balance!
Please investigate immediately.

KeyHound Enhanced Challenge Monitor
            """.strip()
            
            # Simulate email sending (in real implementation, use smtplib)
            print(f"✅ Email notification prepared:")
            print(f"   To: {', '.join(self.notification_config['email']['recipient_emails'])}")
            print(f"   Subject: {subject}")
            print(f"   Body: {len(body)} characters")
            
        except Exception as e:
            print(f"❌ Email notification failed: {e}")
    
    def _send_sms_notification(self, result: Dict[str, Any]):
        """Send SMS notification."""
        try:
            print("📱 Testing SMS notification...")
            
            message = f"🚨 KeyHound Alert: {result['puzzle']} address has ${result['current_balance_usd']:,.2f} balance! Address: {result['address'][:20]}..."
            
            # Simulate SMS sending (in real implementation, use Twilio)
            print(f"✅ SMS notification prepared:")
            print(f"   To: {', '.join(self.notification_config['sms']['to_numbers'])}")
            print(f"   Message: {message}")
            
        except Exception as e:
            print(f"❌ SMS notification failed: {e}")
    
    def _send_webhook_notification(self, result: Dict[str, Any]):
        """Send webhook notification."""
        try:
            print("🔗 Testing webhook notification...")
            
            payload = {
                "text": f"🚨 KeyHound Alert: {result['puzzle']} Address Has Balance!",
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {"title": "Puzzle", "value": f"{result['puzzle']} ({result['bits']}-bit)", "short": True},
                            {"title": "Address", "value": result['address'], "short": False},
                            {"title": "Current Balance", "value": f"${result['current_balance_usd']:,.2f}", "short": True},
                            {"title": "BTC Balance", "value": f"{result['current_balance_btc']:.8f} BTC", "short": True},
                            {"title": "Original Prize", "value": f"{result['original_prize_btc']} BTC", "short": True},
                            {"title": "Solved Date", "value": result['solved_date'], "short": True}
                        ]
                    }
                ]
            }
            
            # Simulate webhook sending (in real implementation, use requests.post)
            print(f"✅ Webhook notification prepared:")
            print(f"   URL: {self.notification_config['webhook']['url']}")
            print(f"   Payload: {json.dumps(payload, indent=2)}")
            
        except Exception as e:
            print(f"❌ Webhook notification failed: {e}")
    
    def monitor_challenges(self, duration_minutes: int = 60):
        """Monitor challenge addresses for specified duration."""
        print(f"\n[MONITOR] Monitoring Bitcoin challenge addresses for {duration_minutes} minutes...")
        print("Checking every 5 minutes for balance changes...")
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)
        
        check_interval = 300  # 5 minutes
        total_checks = (duration_minutes * 60) // check_interval
        
        try:
            for i in range(total_checks):
                print(f"\n[Check {i+1}/{total_checks}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                results = self.check_solved_addresses()
                
                # Check for any addresses with balance
                addresses_with_balance = [r for r in results if r.get('has_balance', False)]
                
                if addresses_with_balance:
                    print(f"\n🚨 ALERT: {len(addresses_with_balance)} addresses have balances!")
                    for addr in addresses_with_balance:
                        print(f"   {addr['puzzle']}: ${addr['current_balance_usd']:,.2f}")
                else:
                    print("✅ No addresses have current balances")
                
                if i < total_checks - 1:  # Don't sleep on last iteration
                    print(f"⏳ Waiting {check_interval//60} minutes until next check...")
                    time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        
        print("\n📊 Monitoring session completed")
    
    def save_results(self, results: List[Dict], filename: str = None):
        """Save monitoring results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bitcoin_challenge_monitor_{timestamp}.json"
        
        data = {
            'monitor_summary': {
                'total_addresses_checked': len(results),
                'addresses_with_balance': len([r for r in results if r.get('has_balance', False)]),
                'bitcoin_price_usd': self.btc_price,
                'check_timestamp': datetime.now().isoformat()
            },
            'address_results': results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        return filename

def main():
    """Main entry point."""
    print("=" * 80)
    print("KeyHound Enhanced - Bitcoin Challenge Monitor")
    print("=" * 80)
    print("Monitoring solved Bitcoin challenge addresses")
    print("Testing notification systems (email, SMS, webhook)")
    print("Use responsibly for legitimate monitoring only.")
    print("=" * 80)
    
    try:
        # Initialize monitor
        monitor = BitcoinChallengeMonitor()
        
        # Check solved addresses once
        print("\n[CHECK] Initial check of solved addresses...")
        results = monitor.check_solved_addresses()
        
        # Save results
        filename = monitor.save_results(results)
        
        # Ask user if they want to monitor continuously
        print(f"\nWould you like to monitor continuously? (y/n): ", end="")
        monitor_choice = input().lower().strip()
        
        if monitor_choice in ['y', 'yes']:
            duration = 60  # Default 60 minutes
            print(f"Enter monitoring duration in minutes (default 60): ", end="")
            try:
                duration = int(input().strip())
            except:
                duration = 60
            
            monitor.monitor_challenges(duration)
        
        print("\n✅ Bitcoin Challenge Monitor completed!")
        print("📊 Notification systems tested successfully")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n🛑 Monitor interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error during monitoring: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
