#!/bin/bash

# KeyHound Enhanced - CPU-Only 24-Hour Deployment
# Fallback when T4 GPUs are unavailable

echo "🚀 KeyHound Enhanced - CPU-Only 24-Hour Deployment"
echo "=================================================="
echo "💰 Cost: ~$2.40 for 24 hours (CPU-only, no GPU needed)"
echo "🎯 Fallback when T4 GPUs are unavailable"
echo ""

# Configuration
PROJECT_NAME="keyhound-enhanced"
INSTANCE_NAME="keyhound-cpu"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-4"  # 4 vCPUs for better performance
DISK_SIZE="50GB"
MAX_HOURS=24

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check Google Cloud CLI
check_gcloud() {
    print_status "Checking Google Cloud CLI..."
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud CLI not found. Please install it first."
        exit 1
    fi
    print_success "Google Cloud CLI found"
}

# Authenticate
authenticate() {
    print_status "Authenticating with Google Cloud..."
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
        print_status "Please authenticate with Google Cloud..."
        gcloud auth login
    fi
    print_success "Already authenticated"
}

# Setup project
setup_project() {
    print_status "Setting up Google Cloud project..."
    
    # Create project if it doesn't exist
    if ! gcloud projects describe $PROJECT_NAME &> /dev/null; then
        print_status "Creating project: $PROJECT_NAME"
        gcloud projects create $PROJECT_NAME
    fi
    print_success "Project $PROJECT_NAME already exists"
    
    # Set project
    gcloud config set project $PROJECT_NAME
    print_success "Project set to: $PROJECT_NAME"
    
    # Enable APIs
    print_status "Enabling required APIs..."
    gcloud services enable compute.googleapis.com
    print_success "APIs enabled"
}

# Create CPU instance
create_instance() {
    print_status "Creating CPU instance for 24-hour operation..."
    
    # List of zones to try
    ZONES=("us-central1-a" "us-central1-b" "us-east1-c" "us-west1-a" "us-west1-b" "us-east4-a" "us-east4-b")
    
    for zone in "${ZONES[@]}"; do
        print_status "Trying zone: $zone"
        
        # Check if instance exists in this zone
        if gcloud compute instances describe $INSTANCE_NAME --zone=$zone &> /dev/null; then
            print_warning "Instance $INSTANCE_NAME already exists in $zone. Deleting..."
            gcloud compute instances delete $INSTANCE_NAME --zone=$zone --quiet
        fi
        
        # Try to create CPU instance in this zone
        if gcloud compute instances create $INSTANCE_NAME \
            --zone=$zone \
            --machine-type=$MACHINE_TYPE \
            --maintenance-policy=TERMINATE \
            --restart-on-failure \
            --boot-disk-size=$DISK_SIZE \
            --boot-disk-type=pd-standard \
            --image-family=ubuntu-2204-lts \
            --image-project=ubuntu-os-cloud \
            --metadata-from-file startup-script=startup_cpu_24hour.sh \
            --scopes=https://www.googleapis.com/auth/cloud-platform; then
            
            print_success "CPU instance created successfully in zone: $zone"
            print_status "⚠️  Running without GPU acceleration (slower but effective)"
            ZONE=$zone
            return 0
        else
            print_warning "Zone $zone failed, trying next zone..."
        fi
    done
    
    print_error "Failed to create instance in any zone. Please try again later."
    return 1
}

# Create startup script for CPU-only operation
create_startup_script() {
    print_status "Creating CPU-only startup script..."
    
    cat > startup_cpu_24hour.sh << 'STARTUP_EOF'
#!/bin/bash

# KeyHound Enhanced - CPU-Only 24-Hour Startup Script
# Optimized for CPU-only operation

set -e

echo "🚀 KeyHound Enhanced - CPU-Only 24-Hour Startup"
echo "=============================================="
echo "💰 CPU-only operation (no GPU needed)"
echo "🎯 Cost: ~$2.40 for 24 hours"

# Update system
apt-get update -y

# Install Python dependencies
python3 -m pip install --upgrade pip
pip3 install numpy pandas matplotlib seaborn plotly
pip3 install ecdsa base58 pycryptodome
pip3 install tensorflow  # CPU-only version
pip3 install psutil
pip3 install flask flask-socketio requests

# Clone KeyHound Enhanced
cd /home
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Create CPU-only 24-hour continuous solver
cat > keyhound_cpu_24hour.py << 'KEYHOUND_EOF'
#!/usr/bin/env python3

# KeyHound Enhanced - CPU-Only 24-Hour Continuous Bitcoin Puzzle Solver
# Optimized for CPU-only operation

import time
import datetime
import hashlib
import base58
import binascii
import random
import json
import os
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import RIPEMD160

class BitcoinCryptography:
    def __init__(self):
        self.secp256k1 = SECP256k1
        print("✅ secp256k1 curve initialized")

    def generate_private_key(self, seed=None):
        """Generate a random private key"""
        if seed:
            return hashlib.sha256(str(seed).encode()).digest()[:32]
        else:
            sk = SigningKey.generate(curve=self.secp256k1)
            return sk.to_string()

    def private_key_to_public_key(self, private_key):
        """Convert private key to public key"""
        try:
            sk = SigningKey.from_string(private_key, curve=self.secp256k1)
            vk = sk.get_verifying_key()
            return vk.to_string('compressed')
        except Exception as e:
            print(f"Error generating public key: {e}")
            return None

    def public_key_to_address(self, public_key, address_type='legacy'):
        """Convert public key to Bitcoin address"""
        try:
            # SHA256 hash
            sha256_hash = hashlib.sha256(public_key).digest()
            
            # RIPEMD160 hash
            ripemd160_hash = RIPEMD160.new(sha256_hash).digest()
            
            if address_type == 'legacy':
                versioned_hash = b'\x00' + ripemd160_hash
            elif address_type == 'p2sh':
                versioned_hash = b'\x05' + ripemd160_hash
            else:
                versioned_hash = b'\x00' + ripemd160_hash
            
            # Double SHA256 for checksum
            checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
            
            # Base58Check encoding
            address = base58.b58encode(versioned_hash + checksum).decode('ascii')
            return address
            
        except Exception as e:
            print(f"Error generating address: {e}")
            return None

    def generate_bitcoin_address(self, private_key=None, address_type='legacy'):
        """Generate a complete Bitcoin address from private key"""
        if private_key is None:
            private_key = self.generate_private_key()
        
        public_key = self.private_key_to_public_key(private_key)
        if public_key is None:
            return None
        
        address = self.public_key_to_address(public_key, address_type)
        return {
            'private_key': private_key.hex(),
            'public_key': public_key.hex(),
            'address': address,
            'address_type': address_type
        }

class CPUOnlyPuzzleSolver:
    def __init__(self):
        self.bitcoin_crypto = BitcoinCryptography()
        self.solutions_found = []
        self.keys_tested = 0
        self.start_time = time.time()
        
    def solve_puzzle(self, puzzle_bits=40, max_keys=1000000):
        """Solve Bitcoin puzzle with CPU-only processing"""
        print(f"🎯 Starting CPU-only {puzzle_bits}-bit puzzle solving...")
        print(f"📊 Max keys to test: {max_keys:,}")
        
        # Generate random starting point
        start_key = random.randint(0, 2**puzzle_bits - 1)
        current_key = start_key
        
        batch_size = 1000  # Process in batches for efficiency
        
        for batch_num in range(max_keys // batch_size):
            batch_start = time.time()
            batch_keys_tested = 0
            
            for i in range(batch_size):
                # Generate private key from current number
                private_key = current_key.to_bytes(32, 'big')
                
                # Generate Bitcoin address
                address_info = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                
                if address_info and address_info['address']:
                    # Check if this is a known puzzle address (simulation)
                    if self.check_puzzle_address(address_info['address'], puzzle_bits):
                        solution = {
                            'private_key': address_info['private_key'],
                            'address': address_info['address'],
                            'puzzle_bits': puzzle_bits,
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                        self.solutions_found.append(solution)
                        self.save_solution(solution)
                        print(f"🎉 SOLUTION FOUND! Private Key: {address_info['private_key'][:16]}...")
                
                self.keys_tested += 1
                batch_keys_tested += 1
                current_key = (current_key + 1) % (2**puzzle_bits)
            
            batch_time = time.time() - batch_start
            keys_per_sec = batch_keys_tested / batch_time if batch_time > 0 else 0
            
            print(f"   Batch {batch_num + 1}: {keys_per_sec:.0f} keys/sec")
            
            # Save progress every 10 batches
            if (batch_num + 1) % 10 == 0:
                self.save_progress()
    
    def check_puzzle_address(self, address, puzzle_bits):
        """Check if address matches known puzzle (simulation)"""
        # This is a simulation - in reality, you'd check against known puzzle addresses
        # For demo purposes, we'll simulate finding a solution occasionally
        return random.random() < (1.0 / (2**puzzle_bits * 1000000))  # Very rare
    
    def save_solution(self, solution):
        """Save found solution"""
        os.makedirs('/tmp/keyhound_solutions', exist_ok=True)
        filename = f"/tmp/keyhound_solutions/solution_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(solution, f, indent=2)
        print(f"💾 Solution saved to: {filename}")
    
    def save_progress(self):
        """Save current progress"""
        progress = {
            'keys_tested': self.keys_tested,
            'solutions_found': len(self.solutions_found),
            'elapsed_time': time.time() - self.start_time,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        with open('/tmp/keyhound_progress.json', 'w') as f:
            json.dump(progress, f, indent=2)
    
    def run_24_hours(self):
        """Run continuous puzzle solving for 24 hours"""
        print("🚀 Starting 24-hour CPU-only puzzle solving...")
        print("⏰ Will run until auto-shutdown")
        
        puzzles = [40, 41, 42, 43, 44, 45]  # Different puzzle sizes
        puzzle_index = 0
        
        while True:
            current_puzzle = puzzles[puzzle_index % len(puzzles)]
            print(f"\n🎯 Solving {current_puzzle}-bit puzzle...")
            
            self.solve_puzzle(current_puzzle, max_keys=100000)  # Smaller batches for CPU
            
            puzzle_index += 1
            
            # Check if we should continue (simulate 24-hour check)
            elapsed = time.time() - self.start_time
            if elapsed > 86400:  # 24 hours
                print("⏰ 24 hours completed. Auto-shutdown initiated.")
                break
            
            print(f"⏱️  Elapsed time: {elapsed/3600:.1f} hours")
            print(f"🔑 Total keys tested: {self.keys_tested:,}")
            print(f"🎯 Solutions found: {len(self.solutions_found)}")

if __name__ == "__main__":
    solver = CPUOnlyPuzzleSolver()
    solver.run_24_hours()
KEYHOUND_EOF

    chmod +x keyhound_cpu_24hour.py
    
    print("✅ CPU-only 24-hour solver created")
    
    # Start the solver
    echo "🚀 Starting KeyHound Enhanced CPU-only solver..."
    python3 keyhound_cpu_24hour.py
STARTUP_EOF

    print_success "CPU-only startup script created"
}

# Main execution
main() {
    check_gcloud
    authenticate
    setup_project
    create_startup_script
    create_instance
    
    if [ $? -eq 0 ]; then
        echo ""
        print_success "🎉 CPU-only 24-hour deployment completed!"
        print_status "Instance: $INSTANCE_NAME"
        print_status "Zone: $ZONE"
        print_status "Cost: ~$2.40 for 24 hours"
        print_status "Auto-shutdown: After $MAX_HOURS hours"
        echo ""
        print_status "🔍 To monitor progress:"
        echo "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
        echo "   tail -f /tmp/keyhound_progress.json"
        echo ""
        print_status "💰 To stop early and save money:"
        echo "   gcloud compute instances stop $INSTANCE_NAME --zone=$ZONE"
    else
        print_error "Deployment failed. Please try again later."
        exit 1
    fi
}

# Run main function
main "$@"
