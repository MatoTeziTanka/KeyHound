#!/usr/bin/env python3
"""
KeyHound Enhanced - Found Keys Verification Tool

This script helps verify and check Bitcoin private keys found by KeyHound Enhanced.
It provides comprehensive verification, balance checking, and wallet import guidance.

Features:
- Verify private key format and derivation
- Check Bitcoin address balance
- Validate key-address pairs
- Generate wallet import instructions
- Security warnings and best practices
- Multiple blockchain explorer support
"""

import os
import sys
import json
import requests
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import argparse

# Import KeyHound modules
try:
    from bitcoin_cryptography import BitcoinCryptography
    from result_persistence import ResultPersistenceManager, ResultType
except ImportError:
    print("Warning: KeyHound modules not found. Using basic verification only.")
    BitcoinCryptography = None
    ResultPersistenceManager = None

@dataclass
class KeyVerificationResult:
    """Result of private key verification."""
    private_key: str
    bitcoin_address: str
    address_type: str
    is_valid: bool
    balance_btc: float
    balance_usd: float
    transaction_count: int
    first_seen: Optional[str]
    last_activity: Optional[str]
    verification_time: str
    explorer_urls: Dict[str, str]

class BitcoinKeyVerifier:
    """Bitcoin private key verification and balance checking."""
    
    def __init__(self):
        """Initialize the verifier."""
        self.crypto = BitcoinCryptography() if BitcoinCryptography else None
        self.explorers = {
            'blockchain_info': 'https://blockchain.info/rawaddr/{address}',
            'blockstream': 'https://blockstream.info/api/address/{address}',
            'blockcypher': 'https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance'
        }
    
    def verify_private_key(self, private_key: str) -> KeyVerificationResult:
        """
        Verify a Bitcoin private key and check its balance.
        
        Args:
            private_key: Private key in hex format
            
        Returns:
            KeyVerificationResult with verification details
        """
        print(f"🔍 Verifying private key: {private_key[:16]}...")
        
        # Basic format validation
        if not self._validate_private_key_format(private_key):
            return KeyVerificationResult(
                private_key=private_key,
                bitcoin_address="INVALID",
                address_type="invalid",
                is_valid=False,
                balance_btc=0.0,
                balance_usd=0.0,
                transaction_count=0,
                first_seen=None,
                last_activity=None,
                verification_time=datetime.now().isoformat(),
                explorer_urls={}
            )
        
        # Derive Bitcoin address
        if self.crypto:
            try:
                public_key = self.crypto.private_to_public(private_key)
                bitcoin_address = self.crypto.public_to_address(public_key, "legacy")
                address_type = "legacy"
            except Exception as e:
                print(f"❌ Error deriving address: {e}")
                bitcoin_address = "DERIVATION_ERROR"
                address_type = "error"
        else:
            bitcoin_address = "CRYPTO_MODULE_UNAVAILABLE"
            address_type = "error"
        
        print(f"📍 Derived Bitcoin address: {bitcoin_address}")
        
        # Check balance
        balance_info = self._check_address_balance(bitcoin_address)
        
        # Generate explorer URLs
        explorer_urls = self._generate_explorer_urls(bitcoin_address)
        
        result = KeyVerificationResult(
            private_key=private_key,
            bitcoin_address=bitcoin_address,
            address_type=address_type,
            is_valid=True,
            balance_btc=balance_info['balance_btc'],
            balance_usd=balance_info['balance_usd'],
            transaction_count=balance_info['transaction_count'],
            first_seen=balance_info['first_seen'],
            last_activity=balance_info['last_activity'],
            verification_time=datetime.now().isoformat(),
            explorer_urls=explorer_urls
        )
        
        return result
    
    def _validate_private_key_format(self, private_key: str) -> bool:
        """Validate private key format."""
        # Remove any whitespace
        private_key = private_key.strip()
        
        # Check if it's a valid hex string
        if len(private_key) != 64:
            print(f"❌ Invalid private key length: {len(private_key)} (expected 64)")
            return False
        
        try:
            int(private_key, 16)
        except ValueError:
            print(f"❌ Invalid hex format")
            return False
        
        # Check if key is in valid range (less than secp256k1 order)
        key_int = int(private_key, 16)
        secp256k1_order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        
        if key_int >= secp256k1_order:
            print(f"❌ Private key exceeds secp256k1 order")
            return False
        
        if key_int == 0:
            print(f"❌ Private key cannot be zero")
            return False
        
        print(f"✅ Private key format is valid")
        return True
    
    def _check_address_balance(self, address: str) -> Dict:
        """Check Bitcoin address balance from multiple sources."""
        print(f"💰 Checking balance for address: {address}")
        
        balance_info = {
            'balance_btc': 0.0,
            'balance_usd': 0.0,
            'transaction_count': 0,
            'first_seen': None,
            'last_activity': None
        }
        
        # Try multiple explorers
        for explorer_name, explorer_url in self.explorers.items():
            try:
                if explorer_name == 'blockchain_info':
                    result = self._check_blockchain_info(address)
                elif explorer_name == 'blockstream':
                    result = self._check_blockstream(address)
                elif explorer_name == 'blockcypher':
                    result = self._check_blockcypher(address)
                else:
                    continue
                
                if result:
                    balance_info.update(result)
                    print(f"✅ Balance found via {explorer_name}: {result['balance_btc']} BTC")
                    break
                    
            except Exception as e:
                print(f"⚠️  {explorer_name} failed: {e}")
                continue
        
        if balance_info['balance_btc'] == 0.0:
            print(f"💰 Address balance: 0.0 BTC (no funds found)")
        else:
            print(f"💰 Address balance: {balance_info['balance_btc']} BTC")
            if balance_info['balance_usd'] > 0:
                print(f"💵 USD value: ${balance_info['balance_usd']:,.2f}")
        
        return balance_info
    
    def _check_blockchain_info(self, address: str) -> Optional[Dict]:
        """Check balance using Blockchain.info API."""
        try:
            url = f"https://blockchain.info/rawaddr/{address}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'balance_btc': data['final_balance'] / 100000000,  # Convert satoshis to BTC
                'transaction_count': data['n_tx'],
                'first_seen': datetime.fromtimestamp(data['first_seen']).isoformat() if data['first_seen'] else None,
                'last_activity': datetime.fromtimestamp(data['last_seen']).isoformat() if data['last_seen'] else None
            }
        except Exception as e:
            print(f"Blockchain.info API error: {e}")
            return None
    
    def _check_blockstream(self, address: str) -> Optional[Dict]:
        """Check balance using Blockstream API."""
        try:
            url = f"https://blockstream.info/api/address/{address}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'balance_btc': data['chain_stats']['funded_txo_sum'] / 100000000 - data['chain_stats']['spent_txo_sum'] / 100000000,
                'transaction_count': data['chain_stats']['tx_count'],
                'first_seen': None,  # Blockstream doesn't provide first_seen
                'last_activity': None  # Blockstream doesn't provide last_activity
            }
        except Exception as e:
            print(f"Blockstream API error: {e}")
            return None
    
    def _check_blockcypher(self, address: str) -> Optional[Dict]:
        """Check balance using BlockCypher API."""
        try:
            url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'balance_btc': data['balance'] / 100000000,  # Convert satoshis to BTC
                'transaction_count': data['n_tx'],
                'first_seen': None,  # BlockCypher doesn't provide first_seen
                'last_activity': None  # BlockCypher doesn't provide last_activity
            }
        except Exception as e:
            print(f"BlockCypher API error: {e}")
            return None
    
    def _generate_explorer_urls(self, address: str) -> Dict[str, str]:
        """Generate blockchain explorer URLs for the address."""
        return {
            'blockchain_info': f"https://blockchain.info/address/{address}",
            'blockstream': f"https://blockstream.info/address/{address}",
            'blockcypher': f"https://live.blockcypher.com/btc/address/{address}",
            'btc_com': f"https://btc.com/{address}"
        }
    
    def load_found_keys(self, results_dir: str = "./results") -> List[Dict]:
        """Load found keys from KeyHound results."""
        found_keys = []
        
        # Try to load from result persistence
        if ResultPersistenceManager:
            try:
                persistence = ResultPersistenceManager()
                results = persistence.list_results(limit=1000)
                for result in results:
                    if hasattr(result, 'private_key') and hasattr(result, 'bitcoin_address'):
                        found_keys.append({
                            'private_key': result.private_key,
                            'bitcoin_address': result.bitcoin_address,
                            'puzzle_id': getattr(result, 'puzzle_id', None),
                            'timestamp': getattr(result, 'timestamp', None),
                            'type': getattr(result, 'type', 'unknown')
                        })
            except Exception as e:
                print(f"Warning: Could not load from result persistence: {e}")
        
        # Try to load from JSON file
        json_file = os.path.join(results_dir, "found_keys.json")
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        found_keys.extend(data)
                    elif isinstance(data, dict) and 'found_keys' in data:
                        found_keys.extend(data['found_keys'])
            except Exception as e:
                print(f"Warning: Could not load from JSON file: {e}")
        
        return found_keys

def print_verification_result(result: KeyVerificationResult):
    """Print formatted verification result."""
    print(f"\n{'='*80}")
    print(f"🔍 BITCOIN KEY VERIFICATION RESULT")
    print(f"{'='*80}")
    
    print(f"Private Key: {result.private_key}")
    print(f"Bitcoin Address: {result.bitcoin_address}")
    print(f"Address Type: {result.address_type}")
    print(f"Valid: {'✅ YES' if result.is_valid else '❌ NO'}")
    
    if result.is_valid:
        print(f"\n💰 BALANCE INFORMATION:")
        print(f"  Bitcoin Balance: {result.balance_btc:.8f} BTC")
        if result.balance_usd > 0:
            print(f"  USD Value: ${result.balance_usd:,.2f}")
        print(f"  Transaction Count: {result.transaction_count}")
        
        if result.first_seen:
            print(f"  First Seen: {result.first_seen}")
        if result.last_activity:
            print(f"  Last Activity: {result.last_activity}")
        
        print(f"\n🌐 BLOCKCHAIN EXPLORERS:")
        for name, url in result.explorer_urls.items():
            print(f"  {name}: {url}")
        
        if result.balance_btc > 0:
            print(f"\n🚨 IMPORTANT: This address contains {result.balance_btc:.8f} BTC!")
            print(f"   Secure the private key immediately!")
            print(f"   Use a reputable wallet to import the key")
            print(f"   Consider transaction fees before moving funds")
        else:
            print(f"\n📝 Note: Address has no balance")
    
    print(f"\nVerification Time: {result.verification_time}")
    print(f"{'='*80}")

def generate_wallet_import_instructions(result: KeyVerificationResult):
    """Generate wallet import instructions."""
    if not result.is_valid:
        return
    
    print(f"\n🔐 WALLET IMPORT INSTRUCTIONS:")
    print(f"{'='*50}")
    
    print(f"\n📱 Electrum Wallet (Recommended):")
    print(f"  1. Download Electrum from https://electrum.org/")
    print(f"  2. Create new wallet or open existing")
    print(f"  3. Go to Wallet → Private Keys → Import")
    print(f"  4. Paste this private key: {result.private_key}")
    print(f"  5. Wallet will show balance and allow transactions")
    
    print(f"\n💻 Bitcoin Core:")
    print(f"  1. Open Bitcoin Core wallet")
    print(f"  2. Go to Help → Debug Window → Console")
    print(f"  3. Run: importprivkey {result.private_key} \"KeyHound Found\"")
    
    print(f"\n⚠️  SECURITY WARNINGS:")
    print(f"  - Never share your private key with anyone")
    print(f"  - Use reputable wallet software only")
    print(f"  - Test with small amounts first")
    print(f"  - Create secure backups")
    print(f"  - Consider hardware wallet for large amounts")

def main():
    """Main function for key verification."""
    parser = argparse.ArgumentParser(description="Verify Bitcoin private keys found by KeyHound Enhanced")
    parser.add_argument("--private-key", help="Private key to verify")
    parser.add_argument("--address", help="Bitcoin address to check balance")
    parser.add_argument("--load-results", action="store_true", help="Load and verify all found keys")
    parser.add_argument("--results-dir", default="./results", help="Results directory path")
    
    args = parser.parse_args()
    
    print("🔍 KeyHound Enhanced - Bitcoin Key Verification Tool")
    print("=" * 60)
    
    verifier = BitcoinKeyVerifier()
    
    if args.private_key:
        # Verify specific private key
        result = verifier.verify_private_key(args.private_key)
        print_verification_result(result)
        generate_wallet_import_instructions(result)
        
    elif args.address:
        # Check specific address balance
        balance_info = verifier._check_address_balance(args.address)
        print(f"\n💰 Address: {args.address}")
        print(f"Balance: {balance_info['balance_btc']:.8f} BTC")
        print(f"Transactions: {balance_info['transaction_count']}")
        
    elif args.load_results:
        # Load and verify all found keys
        found_keys = verifier.load_found_keys(args.results_dir)
        
        if not found_keys:
            print(f"❌ No found keys found in {args.results_dir}")
            return
        
        print(f"🔍 Found {len(found_keys)} keys to verify...")
        
        for i, key_data in enumerate(found_keys, 1):
            print(f"\n[{i}/{len(found_keys)}] Verifying key...")
            
            private_key = key_data.get('private_key', '')
            if not private_key:
                print(f"❌ No private key found in record")
                continue
            
            result = verifier.verify_private_key(private_key)
            print_verification_result(result)
            
            if result.balance_btc > 0:
                print(f"🚨 FOUND BALANCE: {result.balance_btc:.8f} BTC!")
                generate_wallet_import_instructions(result)
            
            # Small delay to avoid rate limiting
            time.sleep(1)
    
    else:
        # Interactive mode
        print(f"\n🔍 Interactive Key Verification")
        print(f"Enter a Bitcoin private key (64 hex characters) or 'quit' to exit:")
        
        while True:
            private_key = input("\nPrivate Key: ").strip()
            
            if private_key.lower() in ['quit', 'exit', 'q']:
                break
            
            if not private_key:
                continue
            
            result = verifier.verify_private_key(private_key)
            print_verification_result(result)
            
            if result.balance_btc > 0:
                generate_wallet_import_instructions(result)
    
    print(f"\n🎉 Verification complete!")

if __name__ == "__main__":
    main()
