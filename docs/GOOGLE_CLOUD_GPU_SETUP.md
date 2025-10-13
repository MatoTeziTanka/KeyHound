# 🚀 KeyHound Enhanced - Google Cloud GPU Setup Guide

## 🎯 **Overview**
This guide will help you deploy KeyHound Enhanced to Google Cloud with GPU acceleration, utilizing your **30 free hours per week** student credits.

## 📊 **Expected Performance Boost**
- **CPU Performance**: 387K operations/second (proven in Codespace)
- **GPU Performance**: 10-100x faster = **3.8M - 38.7M operations/second**
- **Puzzle #66**: 0.001% coverage in **2.3 - 23 years** (vs 234 years)
- **Puzzle #71**: 0.001% coverage in **75 - 750 years** (vs 7,487 years)

## 🛠️ **Prerequisites**
- ✅ Google Cloud account with student credits
- ✅ 30 free hours per week available
- ✅ KeyHound Enhanced working locally (✅ DONE!)

## 🚀 **Step 1: Google Cloud Setup**

### **1.1 Create Google Cloud Project**
```bash
# Install Google Cloud CLI (if not already installed)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login to Google Cloud
gcloud auth login

# Create new project
gcloud projects create keyhound-enhanced --name="KeyHound Enhanced"

# Set project
gcloud config set project keyhound-enhanced

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### **1.2 Configure GPU Quotas**
```bash
# Request GPU quota increase (you may need to wait for approval)
gcloud compute project-info describe --format="value(quotas[].limit)" --filter="quotas.metric=GPUS_ALL_REGIONS"

# Enable billing (required for GPU instances)
# Go to: https://console.cloud.google.com/billing
```

## 🖥️ **Step 2: GPU Instance Setup**

### **2.1 Create GPU-Enabled Instance**
```bash
# Create GPU instance with CUDA support
gcloud compute instances create keyhound-gpu \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-standard \
    --maintenance-policy=TERMINATE \
    --restart-on-failure \
    --metadata=startup-script='#!/bin/bash
        apt-get update
        apt-get install -y python3 python3-pip git curl
        curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
        mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
        apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
        add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
        apt-get update
        apt-get install -y cuda
        echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bashrc
        echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH" >> ~/.bashrc'
```

### **2.2 Connect to Instance**
```bash
# SSH into the instance
gcloud compute ssh keyhound-gpu --zone=us-central1-a

# Install CUDA drivers (if not already installed)
sudo apt-get update
sudo apt-get install -y nvidia-driver-470
sudo reboot
```

## 🐍 **Step 3: Python Environment Setup**

### **3.1 Install Python Dependencies**
```bash
# Update system
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev

# Install CUDA-enabled packages
pip3 install --upgrade pip
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install cupy-cuda11x
pip3 install numba[cuda]

# Install KeyHound Enhanced dependencies
pip3 install requests colorama cryptography psutil numpy scikit-learn nltk
pip3 install flask flask-socketio werkzeug
pip3 install redis pyzmq
```

### **3.2 Clone KeyHound Enhanced**
```bash
# Clone repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Make scripts executable
chmod +x *.sh
```

## ⚡ **Step 4: GPU-Accelerated Version**

### **4.1 Create GPU-Optimized KeyHound**
```bash
# Create GPU version (we'll create this)
python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA devices: {torch.cuda.device_count()}')
if torch.cuda.is_available():
    print(f'Current device: {torch.cuda.current_device()}')
    print(f'Device name: {torch.cuda.get_device_name()}')
"
```

## 🧪 **Step 5: Performance Testing**

### **5.1 Run GPU Benchmark**
```bash
# Test GPU performance
python3 keyhound_gpu.py --benchmark 60

# Expected results:
# CPU: ~387K operations/second
# GPU: ~3.8M - 38.7M operations/second (10-100x faster)
```

### **5.2 Test Real Puzzle Solving**
```bash
# Test Puzzle #66 with GPU acceleration
python3 keyhound_gpu.py --puzzle 66 --max-keys 10000000

# Expected: 10-100x faster key testing
```

## 💰 **Step 6: Cost Management**

### **6.1 Monitor Usage**
```bash
# Check current usage
gcloud billing accounts list
gcloud billing budgets list

# Set up budget alerts
# Go to: https://console.cloud.google.com/billing/budgets
```

### **6.2 Optimize for Free Tier**
```bash
# Use preemptible instances (up to 80% cheaper)
gcloud compute instances create keyhound-gpu-preemptible \
    --zone=us-central1-a \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --preemptible \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud

# Schedule automatic shutdown
gcloud compute instances add-metadata keyhound-gpu \
    --metadata=shutdown-script='#!/bin/bash
        shutdown -h now' \
    --zone=us-central1-a
```

## 🎯 **Step 7: Production Deployment**

### **7.1 Set Up Monitoring**
```bash
# Install monitoring tools
pip3 install google-cloud-monitoring

# Set up performance monitoring
python3 setup_gpu_monitoring.py
```

### **7.2 Configure Auto-Scaling**
```bash
# Create instance template
gcloud compute instance-templates create keyhound-gpu-template \
    --machine-type=n1-standard-4 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --preemptible

# Create managed instance group
gcloud compute instance-groups managed create keyhound-gpu-group \
    --template=keyhound-gpu-template \
    --size=1 \
    --zone=us-central1-a
```

## 📊 **Expected Results**

### **Performance Comparison:**
| Environment | Operations/sec | Puzzle #66 (0.001%) | Puzzle #71 (0.001%) |
|-------------|----------------|---------------------|---------------------|
| **Codespace (CPU)** | 387K | 234 years | 7,487 years |
| **Google Cloud GPU** | 3.8M - 38.7M | 2.3 - 23 years | 75 - 750 years |

### **Cost Analysis:**
- **GPU Instance**: ~$0.35/hour (T4 GPU)
- **30 free hours/week**: ~$10.50/week value
- **Monthly value**: ~$42/month in free credits

## 🚨 **Important Notes**

### **Free Tier Limitations:**
- ⚠️ GPU instances are NOT included in free tier
- ✅ You'll use your student credits
- ✅ 30 hours/week = ~4.3 hours/day
- ✅ Can run continuously or in bursts

### **Best Practices:**
1. **Start with small tests** to verify everything works
2. **Monitor costs** closely
3. **Use preemptible instances** when possible
4. **Set up automatic shutdown** to prevent overage
5. **Schedule runs** during off-peak hours

## 🎉 **Success Metrics**

You'll know it's working when you see:
- ✅ **10-100x performance improvement**
- ✅ **GPU utilization >80%**
- ✅ **Puzzle solving at millions of keys/second**
- ✅ **Cost within your 30-hour budget**

## 🚀 **Next Steps**

1. **Set up Google Cloud project**
2. **Create GPU instance**
3. **Deploy KeyHound Enhanced**
4. **Run GPU benchmarks**
5. **Test real puzzle solving**
6. **Scale to production**

**Ready to achieve 10-100x performance boost? Let's go!** 🐕‍🦺🚀✨


