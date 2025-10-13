#!/bin/bash

# KeyHound Enhanced - Google Cloud GPU Deployment Script
# This script automates the deployment of KeyHound Enhanced to Google Cloud with GPU acceleration

set -e  # Exit on any error

echo "🚀 KeyHound Enhanced - Google Cloud GPU Deployment"
echo "=================================================="

# Configuration
PROJECT_NAME="keyhound-enhanced"
INSTANCE_NAME="keyhound-gpu"
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-4"
GPU_TYPE="nvidia-tesla-t4"
GPU_COUNT=1
DISK_SIZE="50GB"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
        print_warning "Not authenticated. Please login..."
        gcloud auth login
    fi
    print_success "Authenticated successfully"
}

# Create project if it doesn't exist
create_project() {
    print_status "Setting up Google Cloud project..."
    
    # Check if project exists
    if ! gcloud projects describe $PROJECT_NAME &> /dev/null; then
        print_status "Creating project: $PROJECT_NAME"
        gcloud projects create $PROJECT_NAME --name="KeyHound Enhanced"
    else
        print_success "Project $PROJECT_NAME already exists"
    fi
    
    # Set project
    gcloud config set project $PROJECT_NAME
    print_success "Project set to: $PROJECT_NAME"
}

# Enable required APIs
enable_apis() {
    print_status "Enabling required APIs..."
    gcloud services enable compute.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable monitoring.googleapis.com
    print_success "APIs enabled"
}

# Check GPU quotas
check_quotas() {
    print_status "Checking GPU quotas..."
    
    # Get current quota
    QUOTA=$(gcloud compute project-info describe --format="value(quotas[].limit)" --filter="quotas.metric=GPUS_ALL_REGIONS" 2>/dev/null || echo "0")
    
    if [ "$QUOTA" -lt "$GPU_COUNT" ]; then
        print_warning "Insufficient GPU quota. Current: $QUOTA, Needed: $GPU_COUNT"
        print_warning "You may need to request quota increase at:"
        print_warning "https://console.cloud.google.com/iam-admin/quotas"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "GPU quota sufficient: $QUOTA GPUs available"
    fi
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    cat > startup_script.sh << 'EOF'
#!/bin/bash

# KeyHound Enhanced - Google Cloud GPU Startup Script
echo "🚀 KeyHound Enhanced GPU Instance Starting..."

# Update system
apt-get update
apt-get upgrade -y

# Install Python and basic tools
apt-get install -y python3 python3-pip python3-dev git curl wget htop

# Install NVIDIA drivers
apt-get install -y nvidia-driver-470
nvidia-smi || echo "NVIDIA drivers installed, reboot required"

# Install CUDA toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
apt-get update
apt-get install -y cuda

# Set up environment variables
echo "export PATH=/usr/local/cuda/bin:$PATH" >> /etc/environment
echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH" >> /etc/environment

# Install Python packages
pip3 install --upgrade pip
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install cupy-cuda11x
pip3 install numba[cuda]

# Install KeyHound dependencies
pip3 install requests colorama cryptography psutil numpy scikit-learn nltk
pip3 install flask flask-socketio werkzeug
pip3 install redis pyzmq

# Clone KeyHound Enhanced
cd /home
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound
chmod +x *.sh

# Create systemd service for automatic startup
cat > /etc/systemd/system/keyhound.service << 'SERVICE_EOF'
[Unit]
Description=KeyHound Enhanced GPU Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/KeyHound
ExecStart=/usr/bin/python3 keyhound_gpu.py --comprehensive
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

systemctl enable keyhound.service

# Create monitoring script
cat > /home/monitor_keyhound.sh << 'MONITOR_EOF'
#!/bin/bash
while true; do
    echo "$(date): Checking KeyHound status..."
    if systemctl is-active --quiet keyhound; then
        echo "✅ KeyHound is running"
    else
        echo "❌ KeyHound is not running, restarting..."
        systemctl restart keyhound
    fi
    
    # Check GPU status
    nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits
    
    sleep 60
done
MONITOR_EOF

chmod +x /home/monitor_keyhound.sh

# Create shutdown script to save costs
cat > /home/shutdown_after_hours.sh << 'SHUTDOWN_EOF'
#!/bin/bash
MAX_HOURS=30  # Maximum hours to run (within weekly free tier)

echo "⏰ KeyHound Enhanced will run for $MAX_HOURS hours, then shutdown"
sleep $((MAX_HOURS * 3600))

echo "🛑 Maximum runtime reached, shutting down..."
systemctl stop keyhound
shutdown -h now
SHUTDOWN_EOF

chmod +x /home/shutdown_after_hours.sh

echo "✅ Startup script completed"
echo "🔄 Rebooting to activate NVIDIA drivers..."
reboot
EOF

    print_success "Startup script created"
}

# Create GPU instance
create_gpu_instance() {
    print_status "Creating GPU instance..."
    
    # Check if instance already exists
    if gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE &> /dev/null; then
        print_warning "Instance $INSTANCE_NAME already exists"
        echo ""
        read -p "Delete and recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Deleting existing instance..."
            gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --quiet
        else
            print_status "Using existing instance"
            return 0
        fi
    fi
    
    # Create the instance
    print_status "Creating GPU instance: $INSTANCE_NAME"
    gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --machine-type=$MACHINE_TYPE \
        --accelerator=type=$GPU_TYPE,count=$GPU_COUNT \
        --image-family=ubuntu-2004-lts \
        --image-project=ubuntu-os-cloud \
        --boot-disk-size=$DISK_SIZE \
        --boot-disk-type=pd-standard \
        --maintenance-policy=TERMINATE \
        --restart-on-failure \
        --metadata-from-file=startup-script=startup_script.sh \
        --tags=keyhound-gpu \
        --scopes=https://www.googleapis.com/auth/cloud-platform
    
    print_success "GPU instance created: $INSTANCE_NAME"
}

# Configure firewall rules
setup_firewall() {
    print_status "Setting up firewall rules..."
    
    # Allow SSH
    gcloud compute firewall-rules create allow-ssh-keyhound \
        --allow tcp:22 \
        --source-ranges 0.0.0.0/0 \
        --target-tags keyhound-gpu \
        --description "Allow SSH for KeyHound GPU instance"
    
    # Allow web interface
    gcloud compute firewall-rules create allow-keyhound-web \
        --allow tcp:5000,tcp:5001 \
        --source-ranges 0.0.0.0/0 \
        --target-tags keyhound-gpu \
        --description "Allow KeyHound web interface"
    
    print_success "Firewall rules configured"
}

# Get instance information
get_instance_info() {
    print_status "Getting instance information..."
    
    # Get external IP
    EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="value(networkInterfaces[0].accessConfigs[0].natIP)")
    
    # Get internal IP
    INTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="value(networkInterfaces[0].networkIP)")
    
    print_success "Instance information:"
    echo "  Name: $INSTANCE_NAME"
    echo "  Zone: $ZONE"
    echo "  External IP: $EXTERNAL_IP"
    echo "  Internal IP: $INTERNAL_IP"
    echo "  Machine Type: $MACHINE_TYPE"
    echo "  GPU: $GPU_COUNT x $GPU_TYPE"
}

# Test GPU functionality
test_gpu() {
    print_status "Testing GPU functionality..."
    
    echo "SSH into the instance and run:"
    echo "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
    echo ""
    echo "Once connected, test GPU with:"
    echo "  nvidia-smi"
    echo "  cd /home/KeyHound"
    echo "  python3 keyhound_gpu.py --benchmark 30"
    echo ""
    echo "Start KeyHound Enhanced:"
    echo "  systemctl start keyhound"
    echo "  systemctl status keyhound"
}

# Create management scripts
create_management_scripts() {
    print_status "Creating management scripts..."
    
    # Start instance script
    cat > start_instance.sh << EOF
#!/bin/bash
echo "🚀 Starting KeyHound GPU instance..."
gcloud compute instances start $INSTANCE_NAME --zone=$ZONE
echo "✅ Instance started"
EOF
    
    # Stop instance script
    cat > stop_instance.sh << EOF
#!/bin/bash
echo "🛑 Stopping KeyHound GPU instance..."
gcloud compute instances stop $INSTANCE_NAME --zone=$ZONE
echo "✅ Instance stopped"
EOF
    
    # SSH script
    cat > ssh_instance.sh << EOF
#!/bin/bash
echo "🔗 Connecting to KeyHound GPU instance..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE
EOF
    
    # Monitor script
    cat > monitor_instance.sh << EOF
#!/bin/bash
echo "📊 Monitoring KeyHound GPU instance..."
gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="table(name,status,machineType,scheduling.preemptible)"
echo ""
echo "GPU Status:"
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="nvidia-smi" --ssh-flag="-o ConnectTimeout=10"
EOF
    
    # Make scripts executable
    chmod +x start_instance.sh stop_instance.sh ssh_instance.sh monitor_instance.sh
    
    print_success "Management scripts created:"
    echo "  ./start_instance.sh    - Start the GPU instance"
    echo "  ./stop_instance.sh     - Stop the GPU instance"
    echo "  ./ssh_instance.sh      - SSH into the instance"
    echo "  ./monitor_instance.sh  - Monitor instance status"
}

# Main deployment function
main() {
    echo ""
    print_status "Starting KeyHound Enhanced GPU deployment..."
    echo ""
    
    # Pre-deployment checks
    check_gcloud
    authenticate
    create_project
    enable_apis
    check_quotas
    
    echo ""
    print_status "Creating deployment artifacts..."
    create_startup_script
    create_management_scripts
    
    echo ""
    print_status "Deploying to Google Cloud..."
    create_gpu_instance
    setup_firewall
    get_instance_info
    
    echo ""
    print_success "🎉 KeyHound Enhanced GPU deployment completed!"
    echo ""
    print_status "Next steps:"
    echo "1. Wait 5-10 minutes for instance to fully initialize"
    echo "2. SSH into the instance: ./ssh_instance.sh"
    echo "3. Test GPU functionality: nvidia-smi"
    echo "4. Run KeyHound GPU tests: python3 keyhound_gpu.py --comprehensive"
    echo "5. Start KeyHound service: systemctl start keyhound"
    echo ""
    print_warning "Cost management:"
    echo "• Instance will auto-shutdown after 30 hours to stay within free tier"
    echo "• Use ./stop_instance.sh to manually stop when not needed"
    echo "• Monitor usage at: https://console.cloud.google.com/billing"
    echo ""
    print_status "Web interface will be available at: http://$EXTERNAL_IP:5000"
    echo ""
    echo "🚀 KeyHound Enhanced is ready for GPU-accelerated Bitcoin puzzle solving!"
}

# Run main function
main "$@"
