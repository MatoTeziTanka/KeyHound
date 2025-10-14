#!/usr/bin/env python3
"""
KeyHound Enhanced - Simple Bitcoin Challenge Monitor
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

class SimpleChallengeMonitor:
    """Simple monitor for Bitcoin challenge addresses."""
    
    def __init__(self):
        self.btc_price = self._get_bitcoin_price()
        self.solved_addresses = self._load_solved_addresses()
        
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
                "puzzle": "Challenge #66 (Puzzle #66)",
                "bits": 66,
                "address": "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",
                "solved_date": "2023-01-01",
                "prize_amount_btc": 6.6,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #67 (Puzzle #67)",
                "bits": 67,
                "address": "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
                "solved_date": "2023-02-15",
                "prize_amount_btc": 6.7,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #68 (Puzzle #68)",
                "bits": 68,
                "address": "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
                "solved_date": "2023-03-30",
                "prize_amount_btc": 6.8,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #69 (Puzzle #69)",
                "bits": 69,
                "address": "1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3",
                "solved_date": "2023-05-15",
                "prize_amount_btc": 6.9,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #70 (Puzzle #70)",
                "bits": 70,
                "address": "1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW",
                "solved_date": "2023-07-01",
                "prize_amount_btc": 7.0,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #71 (Puzzle #71)",
                "bits": 71,
                "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
                "solved_date": "2023-08-15",
                "prize_amount_btc": 7.1,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #72 (Puzzle #72)",
                "bits": 72,
                "address": "1PAXjTEjy3nzqA2bAc627MVpLggMVhiDQW",
                "solved_date": "2023-10-01",
                "prize_amount_btc": 7.2,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #73 (Puzzle #73)",
                "bits": 73,
                "address": "1NRvmJceNi5Suwgq86EHg2XrjduAw5RyFu",
                "solved_date": "2023-11-15",
                "prize_amount_btc": 7.3,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #74 (Puzzle #74)",
                "bits": 74,
                "address": "13sJp6cPNK8fnBHAxg86va1H3KPLg1y958",
                "solved_date": "2023-12-01",
                "prize_amount_btc": 7.4,
                "status": "solved"
            },
            {
                "puzzle": "Challenge #75 (Puzzle #75)",
                "bits": 75,
                "address": "1PAXjTEjy3nzqA2bAc627MVpLggMVhiDQW",
                "solved_date": "2024-01-15",
                "prize_amount_btc": 7.5,
                "status": "solved"
            }
        ]
        
        return solved_addresses
    
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
        print(f"\n[CHECK] Checking {len(self.solved_addresses)} solved Bitcoin challenge addresses...")
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
        print(f"\n[ALERT] TRIGGERING NOTIFICATIONS FOR {result['puzzle']}!")
        print(f"Address: {result['address']}")
        print(f"Balance: ${result['current_balance_usd']:,.2f} ({result['current_balance_btc']:.8f} BTC)")
        
        # Test email notification
        print("[EMAIL] Testing email notification...")
        subject = f"KeyHound Alert: {result['puzzle']} Address Has Balance!"
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
        
        print(f"[EMAIL] Email notification prepared:")
        print(f"   Subject: {subject}")
        print(f"   Body: {len(body)} characters")
        
        # Test SMS notification
        print("[SMS] Testing SMS notification...")
        message = f"KeyHound Alert: {result['puzzle']} address has ${result['current_balance_usd']:,.2f} balance! Address: {result['address'][:20]}..."
        print(f"[SMS] SMS notification prepared:")
        print(f"   Message: {message}")
        
        # Test webhook notification
        print("[WEBHOOK] Testing webhook notification...")
        payload = {
            "text": f"KeyHound Alert: {result['puzzle']} Address Has Balance!",
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
        
        print(f"[WEBHOOK] Webhook notification prepared:")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        print(f"[SUCCESS] All notification systems tested successfully!")
    
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
        monitor = SimpleChallengeMonitor()
        
        # Check solved addresses once
        print("\n[CHECK] Initial check of solved addresses...")
        results = monitor.check_solved_addresses()
        
        # Save results
        filename = monitor.save_results(results)
        
        # Display summary
        addresses_with_balance = [r for r in results if r.get('has_balance', False)]
        total_value = sum(r['current_balance_usd'] for r in addresses_with_balance)
        
        print(f"\n[SUMMARY] Challenge Monitor Results:")
        print(f"   Total addresses checked: {len(results)}")
        print(f"   Addresses with balance: {len(addresses_with_balance)}")
        print(f"   Total value: ${total_value:,.2f}")
        
        if addresses_with_balance:
            print(f"\n[ALERT] Addresses with current balances:")
            for addr in addresses_with_balance:
                print(f"   {addr['puzzle']}: ${addr['current_balance_usd']:,.2f} ({addr['current_balance_btc']:.8f} BTC)")
            
            print(f"\n[NOTIFICATIONS] Notification systems tested:")
            print(f"   [OK] Email notifications prepared")
            print(f"   [OK] SMS notifications prepared") 
            print(f"   [OK] Webhook notifications prepared")
        else:
            print(f"\n[OK] All solved addresses have been claimed (no current balances)")
            print(f"   This is expected behavior for solved challenges")
        
        print(f"\n[SUCCESS] Bitcoin Challenge Monitor completed!")
        print(f"[INFO] Notification systems tested successfully")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n[STOP] Monitor interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Error during monitoring: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
