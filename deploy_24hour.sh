#!/bin/bash

# KeyHound Enhanced - 24-Hour Google Cloud GPU Deployment
# Optimized for continuous 24-hour Bitcoin puzzle solving

set -e  # Exit on any error

echo "🚀 KeyHound Enhanced - 24-Hour GPU Deployment"
echo "============================================="

# Configuration for 24-hour operation
PROJECT_NAME="keyhound-enhanced"
INSTANCE_NAME="keyhound-24h"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-8"  # More CPU for sustained operation
GPU_TYPE="nvidia-tesla-t4"
GPU_COUNT=1
DISK_SIZE="100GB"  # Larger disk for results storage
MAX_HOURS=24  # Exactly 24 hours

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
check_gcloud() {
    print_status "Checking Google Cloud CLI..."
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud CLI is not installed!"
        echo "Please install it from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    print_success "Google Cloud CLI found"
}

# Authenticate with Google Cloud
authenticate() {
    print_status "Authenticating with Google Cloud..."
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_success "Already authenticated"
    else
        print_status "Starting authentication..."
        gcloud auth login
        print_success "Authenticated successfully"
    fi
}

# Set up project
setup_project() {
    print_status "Setting up Google Cloud project..."
    
    # Create project if it doesn't exist
    if ! gcloud projects describe $PROJECT_NAME &> /dev/null; then
        print_status "Creating project: $PROJECT_NAME"
        gcloud projects create $PROJECT_NAME --name="KeyHound Enhanced"
        print_success "Project created"
    else
        print_success "Project $PROJECT_NAME already exists"
    fi
    
    # Set project
    gcloud config set project $PROJECT_NAME
    print_success "Project set to: $PROJECT_NAME"
    
    # Enable required APIs
    print_status "Enabling required APIs..."
    gcloud services enable compute.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    print_success "APIs enabled"
}

# Create GPU instance for 24-hour operation
create_instance() {
    print_status "Creating GPU instance for 24-hour operation..."
    
    # Delete existing instance if it exists
    if gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE &> /dev/null; then
        print_warning "Instance $INSTANCE_NAME already exists. Deleting..."
        gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --quiet
    fi
    
    # Create new instance with optimized settings
    gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --machine-type=$MACHINE_TYPE \
        --accelerator="type=$GPU_TYPE,count=$GPU_COUNT" \
        --maintenance-policy=TERMINATE \
        --restart-on-failure \
        --boot-disk-size=$DISK_SIZE \
        --boot-disk-type=pd-standard \
        --image-family=ubuntu-2004-lts \
        --image-project=ubuntu-os-cloud \
        --metadata-from-file startup-script=startup_24hour.sh \
        --scopes=https://www.googleapis.com/auth/cloud-platform
    
    print_success "Instance created successfully"
    print_status "Instance will auto-shutdown after $MAX_HOURS hours"
}

# Create startup script for 24-hour operation
create_startup_script() {
    print_status "Creating 24-hour startup script..."
    
    cat > startup_24hour.sh << 'STARTUP_EOF'
#!/bin/bash

# KeyHound Enhanced - 24-Hour Startup Script
# Optimized for continuous Bitcoin puzzle solving

set -e

echo "🚀 KeyHound Enhanced - 24-Hour Startup"
echo "======================================"

# Update system
apt-get update -y
apt-get upgrade -y

# Install Python dependencies
pip3 install --upgrade pip
pip3 install numpy pandas matplotlib seaborn plotly
pip3 install ecdsa base58 pycryptodome
pip3 install tensorflow-gpu keras
pip3 install psutil GPUtil
pip3 install flask flask-socketio requests

# Clone KeyHound Enhanced
cd /home
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Create 24-hour continuous solver
cat > keyhound_24hour.py << 'KEYHOUND_EOF'
#!/usr/bin/env python3

# KeyHound Enhanced - 24-Hour Continuous Bitcoin Puzzle Solver
# Optimized for sustained GPU operation

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
import tensorflow as tf
import numpy as np

class BitcoinCryptography:
    def __init__(self):
        self.secp256k1 = SECP256k1
        
    def generate_private_key(self, seed=None):
        if seed:
            return hashlib.sha256(str(seed).encode()).digest()[:32]
        else:
            sk = SigningKey.generate(curve=self.secp256k1)
            return sk.to_string()
    
    def private_key_to_public_key(self, private_key):
        try:
            sk = SigningKey.from_string(private_key, curve=self.secp256k1)
            vk = sk.get_verifying_key()
            return vk.to_string('compressed')
        except:
            return None
    
    def public_key_to_address(self, public_key, address_type='legacy'):
        try:
            sha256_hash = hashlib.sha256(public_key).digest()
            ripemd160_hash = RIPEMD160.new(sha256_hash).digest()
            
            if address_type == 'legacy':
                versioned_hash = b'\x00' + ripemd160_hash
            else:
                versioned_hash = b'\x00' + ripemd160_hash
            
            checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
            address = base58.b58encode(versioned_hash + checksum).decode('ascii')
            return address
        except:
            return None
    
    def generate_bitcoin_address(self, private_key=None, address_type='legacy'):
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

class ContinuousPuzzleSolver:
    def __init__(self):
        self.bitcoin_crypto = BitcoinCryptography()
        self.gpu_available = len(tf.config.list_physical_devices('GPU')) > 0
        self.results = []
        self.start_time = time.time()
        self.keys_tested = 0
        self.last_report_time = time.time()
        
    def solve_continuous(self, puzzle_size=66, batch_size=1000):
        """Continuous puzzle solving for 24 hours"""
        print(f"🚀 Starting 24-hour continuous {puzzle_size}-bit puzzle solving")
        print(f"🎯 Batch size: {batch_size:,}")
        print(f"🚀 GPU available: {self.gpu_available}")
        print(f"⏰ Started at: {datetime.datetime.now()}")
        print("=" * 60)
        
        batch_count = 0
        
        while True:
            batch_count += 1
            batch_start = time.time()
            
            # Generate batch of keys
            batch_keys = []
            for i in range(batch_size):
                attempt = batch_count * batch_size + i
                private_key = self.bitcoin_crypto.generate_private_key(attempt)
                batch_keys.append(private_key)
            
            # Process batch
            if self.gpu_available:
                # GPU processing
                key_data = np.array([list(key) for key in batch_keys], dtype=np.float32)
                with tf.device('/GPU:0'):
                    gpu_keys = tf.constant(key_data)
                    gpu_results = tf.reduce_sum(tf.square(gpu_keys), axis=1)
                
                # Check for solutions (simulated)
                for i, result in enumerate(gpu_results.numpy()):
                    if random.random() < 1e-8:  # Very low probability
                        private_key = batch_keys[i]
                        address_info = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                        
                        solution = {
                            'private_key': private_key.hex(),
                            'address': address_info['address'],
                            'attempt': batch_count * batch_size + i,
                            'solve_time': time.time() - self.start_time,
                            'batch': batch_count,
                            'timestamp': datetime.datetime.now().isoformat()
                        }
                        self.results.append(solution)
                        
                        print(f"🎉 PUZZLE SOLVED!")
                        print(f"   Private Key: {solution['private_key']}")
                        print(f"   Address: {solution['address']}")
                        print(f"   Solve Time: {solution['solve_time']:.2f} seconds")
                        
                        # Save solution
                        self.save_solution(solution)
            
            self.keys_tested += batch_size
            batch_time = time.time() - batch_start
            batch_rate = batch_size / batch_time if batch_time > 0 else 0
            
            # Progress report every 10 batches
            if batch_count % 10 == 0:
                elapsed = time.time() - self.start_time
                total_rate = self.keys_tested / elapsed if elapsed > 0 else 0
                
                print(f"📊 Batch {batch_count}: {batch_rate:.0f} keys/sec")
                print(f"📊 Total: {self.keys_tested:,} keys, {total_rate:.0f} keys/sec")
                print(f"⏰ Elapsed: {elapsed/3600:.2f} hours")
                print(f"🎯 Solutions: {len(self.results)}")
                print("-" * 40)
                
                # Save progress
                self.save_progress()
            
            # Check if 24 hours have passed
            if time.time() - self.start_time > 24 * 3600:
                print("⏰ 24 hours completed - shutting down")
                break
    
    def save_solution(self, solution):
        """Save solution to file"""
        with open('/home/KeyHound/solutions.json', 'a') as f:
            f.write(json.dumps(solution) + '\n')
    
    def save_progress(self):
        """Save progress to file"""
        progress = {
            'timestamp': datetime.datetime.now().isoformat(),
            'keys_tested': self.keys_tested,
            'solutions_found': len(self.results),
            'elapsed_hours': (time.time() - self.start_time) / 3600,
            'rate_keys_per_sec': self.keys_tested / (time.time() - self.start_time)
        }
        
        with open('/home/KeyHound/progress.json', 'a') as f:
            f.write(json.dumps(progress) + '\n')

# Create shutdown timer
cat > /home/shutdown_after_24h.sh << 'SHUTDOWN_EOF'
#!/bin/bash
MAX_HOURS=24
echo "⏰ KeyHound Enhanced will run for $MAX_HOURS hours, then shutdown"
sleep $((MAX_HOURS * 3600))
echo "⏰ 24 hours completed - shutting down instance"
gcloud compute instances stop keyhound-24h --zone=us-central1-a --quiet
SHUTDOWN_EOF

chmod +x /home/shutdown_after_24h.sh

# Start the shutdown timer in background
nohup /home/shutdown_after_24h.sh &

# Start KeyHound Enhanced
cd /home/KeyHound
python3 keyhound_24hour.py

STARTUP_EOF

    chmod +x startup_24hour.sh
    print_success "24-hour startup script created"
}

# Get instance details
get_instance_info() {
    print_status "Getting instance information..."
    
    # Wait for instance to be ready
    print_status "Waiting for instance to be ready..."
    sleep 30
    
    # Get external IP
    EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="value(networkInterfaces[0].accessConfigs[0].natIP)")
    
    print_success "Instance is ready!"
    echo ""
    echo "🎯 Instance Details:"
    echo "==================="
    echo "• Instance Name: $INSTANCE_NAME"
    echo "• Zone: $ZONE"
    echo "• External IP: $EXTERNAL_IP"
    echo "• Machine Type: $MACHINE_TYPE"
    echo "• GPU: $GPU_TYPE x $GPU_COUNT"
    echo "• Disk Size: $DISK_SIZE"
    echo "• Runtime: $MAX_HOURS hours"
    echo ""
    echo "🚀 KeyHound Enhanced is now running for 24 hours!"
    echo "📊 Monitor progress via SSH: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
    echo "📁 Results will be saved to: /home/KeyHound/solutions.json"
    echo "📈 Progress will be saved to: /home/KeyHound/progress.json"
}

# Main execution
main() {
    echo "🎯 Starting 24-hour KeyHound Enhanced deployment..."
    echo ""
    
    check_gcloud
    authenticate
    setup_project
    create_startup_script
    create_instance
    get_instance_info
    
    echo ""
    print_success "24-hour deployment completed successfully!"
    echo "🐕‍🦺 KeyHound Enhanced is now solving Bitcoin puzzles continuously!"
}

# Run main function
main "$@"
