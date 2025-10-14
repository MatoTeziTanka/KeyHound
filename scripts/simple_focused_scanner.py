#!/usr/bin/env python3
"""
KeyHound Enhanced - Simple Focused Brainwallet Scanner
Focuses specifically on the high-value wallet: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
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

def main():
    """Main entry point."""
    print("=" * 80)
    print("KeyHound Enhanced - Simple Focused Brainwallet Scanner")
    print("=" * 80)
    print("Focusing on the high-value wallet: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2")
    print("=" * 80)
    
    # Target wallet details
    target_address = "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
    target_patterns = ["password", "bitcoin", "private"]
    
    # Get Bitcoin price
    btc_price = get_bitcoin_price()
    print(f"Current Bitcoin price: ${btc_price:,.2f}")
    
    # Check current balance
    print(f"\nChecking current balance for: {target_address}")
    balance_satoshi, balance_btc = get_address_balance(target_address)
    balance_usd = balance_btc * btc_price
    
    print(f"Current Balance: {balance_btc:.8f} BTC (${balance_usd:,.2f} USD)")
    
    # Verify patterns
    print(f"\nVerifying brainwallet patterns:")
    print("-" * 50)
    
    verified_patterns = []
    
    for pattern in target_patterns:
        print(f"Testing pattern: '{pattern}'", end=" ... ")
        
        address, private_key = generate_brainwallet_address(pattern)
        
        if address == target_address:
            print("MATCHES TARGET ADDRESS")
            verified_patterns.append({
                'pattern': pattern,
                'private_key': private_key,
                'verified': True
            })
        else:
            print(f"Different address: {address}")
            verified_patterns.append({
                'pattern': pattern,
                'private_key': private_key,
                'verified': False
            })
    
    # Summary
    print("\n" + "=" * 80)
    print("FOCUSED SCAN SUMMARY")
    print("=" * 80)
    print(f"Target Address: {target_address}")
    print(f"Current Balance: {balance_btc:.8f} BTC (${balance_usd:,.2f} USD)")
    print(f"Bitcoin Price: ${btc_price:,.2f}")
    
    verified_count = sum(1 for p in verified_patterns if p['verified'])
    print(f"Verified Patterns: {verified_count}/{len(target_patterns)}")
    
    if verified_count > 0:
        print(f"\nVERIFIED BRAINWALLET PATTERNS:")
        for pattern_info in verified_patterns:
            if pattern_info['verified']:
                print(f"  Pattern: '{pattern_info['pattern']}'")
                print(f"  Private Key: {pattern_info['private_key']}")
                print()
    
    # Save results
    results = {
        'target_address': target_address,
        'current_balance_btc': balance_btc,
        'current_balance_usd': balance_usd,
        'bitcoin_price_usd': btc_price,
        'verified_patterns': verified_patterns,
        'scan_timestamp': datetime.now().isoformat()
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"focused_scan_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {filename}")
    print("=" * 80)
    print("Ready for live KeyHound testing!")
    print("=" * 80)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
