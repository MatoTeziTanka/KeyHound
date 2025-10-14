#!/usr/bin/env python3
"""
KeyHound Enhanced - Corrected Focused Brainwallet Scanner
Properly generates addresses from patterns and finds real brainwallet matches.
"""

import os
import sys
import time
import json
import requests
import hashlib
from pathlib import Path
from datetime import datetime

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_bitcoin_price():
    """Get current Bitcoin price in USD."""
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['bitcoin']['usd']
    except:
        pass
    return 50000.0  # Fallback

def get_address_balance(address):
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

def generate_brainwallet_address(pattern):
    """Generate Bitcoin address from brainwallet pattern."""
    try:
        # Generate private key from pattern using SHA256
        private_key_hex = hashlib.sha256(pattern.encode('utf-8')).hexdigest()
        
        # Import Bitcoin cryptography
        from core.bitcoin_cryptography import BitcoinCryptography
        crypto = BitcoinCryptography()
        
        # Generate address
        address = crypto.generate_bitcoin_address(private_key_hex)
        
        return address, private_key_hex
        
    except Exception as e:
        print(f"Error generating address for '{pattern}': {e}")
        return None, None

def scan_common_patterns():
    """Scan common patterns and check their balances."""
    print("Scanning common brainwallet patterns for high-value wallets...")
    print("=" * 80)
    
    # Common patterns to test
    patterns = [
        "password", "123456", "bitcoin", "wallet", "private", "key", "secret",
        "hello world", "test", "admin", "qwerty", "abc123", "password123",
        "satoshi", "nakamoto", "blockchain", "crypto", "mining", "hash"
    ]
    
    btc_price = get_bitcoin_price()
    high_value_wallets = []
    
    for i, pattern in enumerate(patterns, 1):
        print(f"[{i:2d}/{len(patterns)}] Testing '{pattern}'", end=" ... ")
        
        try:
            address, private_key = generate_brainwallet_address(pattern)
            
            if address:
                balance_satoshi, balance_btc = get_address_balance(address)
                balance_usd = balance_btc * btc_price
                
                if balance_usd > 0:
                    print(f"${balance_usd:,.2f} ({balance_btc:.8f} BTC)")
                    
                    if balance_usd >= 100:
                        high_value_wallets.append({
                            'pattern': pattern,
                            'address': address,
                            'private_key': private_key,
                            'balance_btc': balance_btc,
                            'balance_usd': balance_usd
                        })
                        print(f"    *** HIGH VALUE FOUND! >= $100 ***")
                else:
                    print("No balance")
            else:
                print("Failed to generate address")
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Error: {e}")
    
    return high_value_wallets, btc_price

def main():
    """Main entry point."""
    print("=" * 80)
    print("KeyHound Enhanced - Corrected Focused Brainwallet Scanner")
    print("=" * 80)
    print("Scanning common patterns for high-value brainwallet addresses")
    print("Use responsibly for legitimate security research only.")
    print("=" * 80)
    
    try:
        # Scan common patterns
        high_value_wallets, btc_price = scan_common_patterns()
        
        # Results
        print("\n" + "=" * 80)
        print("SCAN RESULTS")
        print("=" * 80)
        print(f"Bitcoin Price: ${btc_price:,.2f}")
        print(f"High-value wallets found: {len(high_value_wallets)}")
        
        if high_value_wallets:
            print(f"\nHIGH-VALUE WALLETS (>= $100):")
            print("-" * 80)
            
            # Sort by balance
            high_value_wallets.sort(key=lambda x: x['balance_usd'], reverse=True)
            
            for i, wallet in enumerate(high_value_wallets, 1):
                print(f"\n{i}. Pattern: '{wallet['pattern']}'")
                print(f"   Address: {wallet['address']}")
                print(f"   Balance: ${wallet['balance_usd']:,.2f} ({wallet['balance_btc']:.8f} BTC)")
                print(f"   Private Key: {wallet['private_key']}")
            
            # Focus on the highest value wallet
            if high_value_wallets:
                top_wallet = high_value_wallets[0]
                print(f"\n" + "=" * 80)
                print("TARGET WALLET FOR FOCUSED SCANNING")
                print("=" * 80)
                print(f"Pattern: '{top_wallet['pattern']}'")
                print(f"Address: {top_wallet['address']}")
                print(f"Balance: ${top_wallet['balance_usd']:,.2f} ({top_wallet['balance_btc']:.8f} BTC)")
                print(f"Private Key: {top_wallet['private_key']}")
                print("=" * 80)
        else:
            print(f"\nNo high-value wallets found with >= $100 balance.")
            print("This is good news for Bitcoin security!")
        
        # Save results
        results = {
            'scan_timestamp': datetime.now().isoformat(),
            'bitcoin_price_usd': btc_price,
            'high_value_wallets': high_value_wallets,
            'total_patterns_scanned': 20
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"corrected_scan_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        print("=" * 80)
        print("Ready for live KeyHound testing!")
        print("=" * 80)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError during scan: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
