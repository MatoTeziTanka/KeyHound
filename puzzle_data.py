#!/usr/bin/env python3
"""
Bitcoin Puzzle Challenge Data
Based on privatekeys.pw/puzzles/bitcoin-puzzle-tx
"""

# Bitcoin Puzzle Challenge Data
BITCOIN_PUZZLES = {
    71: {
        "key_range_bits": "270...271",
        "key_range_hex": "400000000000000000:7fffffffffffffffff",
        "bitcoin_address": "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
        "status": "UNSOLVED",
        "priority": "HIGH"  # Narrowest key space
    },
    72: {
        "key_range_bits": "271...272", 
        "key_range_hex": "800000000000000000:ffffffffffffffffff",
        "bitcoin_address": "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
        "status": "UNSOLVED",
        "priority": "HIGH"
    },
    135: {
        "key_range_bits": "2134...2135",
        "key_range_hex": "8000000000000000000000000000000000000:fffffffffffffffffffffffffffffffffffff",
        "bitcoin_address": "13RGVmP4VbRE3PcKpN1F8TqGspnxyHahpt5Te8jy",
        "public_key": "03137807790ea7dc6e97901c2bc87411f45ed74a5629315c4e4b03a0a102250c49",
        "status": "UNSOLVED", 
        "priority": "HIGH"  # Exposed public key - BSGS algorithm
    },
    151: {
        "key_range_bits": "2150...2151",
        "key_range_hex": "40000000000000000000000000000000000000:7fffffffffffffffffffffffffffffffffffff",
        "bitcoin_address": "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
        "status": "UNSOLVED",
        "priority": "MEDIUM"
    },
    152: {
        "key_range_bits": "2151...2152",
        "key_range_hex": "80000000000000000000000000000000000000:ffffffffffffffffffffffffffffffffffffff",
        "bitcoin_address": "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN",
        "status": "UNSOLVED",
        "priority": "MEDIUM"
    },
    155: {
        "key_range_bits": "2154...2155",
        "key_range_hex": "400000000000000000000000000000000000000:7ffffffffffffffffffffffffffffffffffffff",
        "bitcoin_address": "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ",
        "public_key": "035cd1854cae45391ca4ec428cc7e6c7d9984424b954209a8eea197b9e364c05f6",
        "status": "UNSOLVED",
        "priority": "MEDIUM"
    },
    160: {
        "key_range_bits": "2159...2160",
        "key_range_hex": "8000000000000000000000000000000000000000:ffffffffffffffffffffffffffffffffffffffff",
        "bitcoin_address": "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv",
        "public_key": "02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673",
        "status": "UNSOLVED",
        "priority": "LOW"
    }
}

# Recently solved puzzles for reference
SOLVED_PUZZLES = {
    66: {"solved_date": "2024-09-12", "solver": "1Jvv4y", "prize": "6.6 BTC"},
    67: {"solved_date": "2025-02-21", "solver": "bc1qfk", "prize": "6.7 BTC"},
    68: {"solved_date": "2025-04-06", "solver": "bc1qfw", "prize": "6.8 BTC"},
    69: {"solved_date": "2025-04-30", "solver": "bc1qlp", "prize": "6.9 BTC"}
}

# Brainwallet patterns for security testing
BRAINWALLET_PATTERNS = [
    # Common weak patterns
    "password", "123456", "qwerty", "admin", "bitcoin",
    "wallet", "private", "key", "secret", "money",
    
    # Bitcoin-specific patterns
    "satoshi", "nakamoto", "blockchain", "mining", "hash",
    "crypto", "btc", "coin", "address", "transaction",
    
    # Common phrases
    "hello world", "test", "example", "sample", "demo",
    "my password", "secret key", "private key", "wallet key",
    
    # Numerical patterns
    "12345", "54321", "11111", "00000", "99999",
    "123456789", "987654321", "111111111", "000000000",
    
    # Date patterns
    "2024", "2025", "january", "february", "march",
    "april", "may", "june", "july", "august",
    "september", "october", "november", "december"
]

def get_puzzle_by_id(puzzle_id):
    """Get puzzle data by ID."""
    return BITCOIN_PUZZLES.get(puzzle_id)

def get_high_priority_puzzles():
    """Get high priority puzzles for solving."""
    return {k: v for k, v in BITCOIN_PUZZLES.items() if v.get("priority") == "HIGH"}

def get_puzzles_with_public_keys():
    """Get puzzles that have exposed public keys (BSGS algorithm candidates)."""
    return {k: v for k, v in BITCOIN_PUZZLES.items() if "public_key" in v}

def hex_range_to_int_range(hex_range):
    """Convert hex range string to integer tuple."""
    start_hex, end_hex = hex_range.split(":")
    return (int(start_hex, 16), int(end_hex, 16))

def calculate_key_space_size(bits_range):
    """Calculate the size of the key space."""
    start_bits, end_bits = map(int, bits_range.split("..."))
    return 2 ** (end_bits - start_bits)

def get_brainwallet_patterns():
    """Get common brainwallet patterns for security testing."""
    return BRAINWALLET_PATTERNS

if __name__ == "__main__":
    # Display puzzle information
    print("Bitcoin Puzzle Challenge Data")
    print("=" * 40)
    
    high_priority = get_high_priority_puzzles()
    print(f"\nHigh Priority Puzzles: {list(high_priority.keys())}")
    
    public_key_puzzles = get_puzzles_with_public_keys()
    print(f"Puzzles with Public Keys: {list(public_key_puzzles.keys())}")
    
    for puzzle_id, data in high_priority.items():
        print(f"\nPuzzle #{puzzle_id}:")
        print(f"  Address: {data['bitcoin_address']}")
        print(f"  Key Range: {data['key_range_bits']} bits")
        print(f"  Hex Range: {data['key_range_hex']}")
        if "public_key" in data:
            print(f"  Public Key: {data['public_key']}")
            print(f"  Algorithm: BSGS (Baby-step Giant-step)")
        else:
            print(f"  Algorithm: Brute Force")
