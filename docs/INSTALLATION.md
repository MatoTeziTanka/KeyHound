# 🔧 KeyHound Enhanced - Installation Guide

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for dependencies

### Recommended for GPU Acceleration
- **GPU**: NVIDIA GPU with CUDA Compute Capability 3.5+
- **VRAM**: 4GB+ recommended
- **CUDA**: Version 11.0 or higher
- **RAM**: 16GB+ for large batch processing

### Recommended for Distributed Computing
- **CPU**: Multi-core processor (8+ cores)
- **RAM**: 16GB+
- **Network**: Low-latency connection between nodes

## 🚀 Installation Methods

### Method 1: Standard Installation

```bash
# Clone the repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

### Method 2: Development Installation

```bash
# Clone repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Method 3: Docker Installation

```bash
# Build Docker image
docker build -t keyhound-enhanced .

# Run with GPU support
docker run --gpus all -p 5000:5000 keyhound-enhanced

# Run without GPU
docker run -p 5000:5000 keyhound-enhanced
```

## 🔧 GPU Setup

### NVIDIA CUDA Setup

1. **Install NVIDIA Drivers**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install nvidia-driver-470
   
   # Reboot system
   sudo reboot
   ```

2. **Install CUDA Toolkit**
   ```bash
   # Download from NVIDIA website or use package manager
   wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
   sudo sh cuda_11.8.0_520.61.05_linux.run
   ```

3. **Verify CUDA Installation**
   ```bash
   nvidia-smi
   nvcc --version
   ```

4. **Install PyTorch with CUDA**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### AMD ROCm Setup

```bash
# Install ROCm
wget https://repo.radeon.com/amdgpu-install/5.4.2/ubuntu/jammy/amdgpu-install_5.4.2.50402-1_all.deb
sudo dpkg -i amdgpu-install_5.4.2.50402-1_all.deb
sudo amdgpu-install --usecase=rocm

# Install PyTorch with ROCm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
```

## 🐍 Python Environment Setup

### Using Conda

```bash
# Create conda environment
conda create -n keyhound python=3.9
conda activate keyhound

# Install CUDA toolkit
conda install cudatoolkit=11.8

# Install dependencies
pip install -r requirements.txt
```

### Using pyenv

```bash
# Install Python 3.9
pyenv install 3.9.16
pyenv local 3.9.16

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔍 Verification

### Test Basic Installation
```bash
# Check Python version
python --version

# Test imports
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"

# Test KeyHound
python main.py --help
```

### Test GPU Support
```bash
# Test CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Test GPU acceleration
python main.py --gpu --puzzle 40
```

### Run Test Suite
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific tests
python tests/comprehensive_test.py
python tests/scaled_test.py
```

## 🔧 Configuration

### Initial Configuration
```bash
# Copy default configuration
cp config/default.yaml config/my_config.yaml

# Edit configuration
nano config/my_config.yaml
```

### Environment Variables
```bash
# Set environment variables
export KEYHOUND_CONFIG=config/production.yaml
export KEYHOUND_LOG_LEVEL=INFO
export KEYHOUND_GPU_ENABLED=true
```

## 🚨 Troubleshooting

### Common Issues

#### 1. CUDA Not Available
```bash
# Check NVIDIA driver
nvidia-smi

# Reinstall PyTorch with CUDA
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 2. Import Errors
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 3. Memory Issues
```bash
# Reduce batch size in config
# Edit config/default.yaml:
gpu:
  batch_size: 1000  # Reduce from default
```

#### 4. Permission Issues
```bash
# Fix permissions (Linux/macOS)
chmod +x scripts/*.sh
chmod +x main.py
```

### Getting Help

1. **Check logs**: `logs/keyhound.log`
2. **Run diagnostics**: `python main.py --diagnostics`
3. **GitHub Issues**: [Create an issue](https://github.com/sethpizzaboy/KeyHound/issues)
4. **Documentation**: Check other guides in `docs/`

## 🔄 Updates

### Updating KeyHound
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Test installation
python main.py --help
```

### Updating Dependencies
```bash
# Update all packages
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade torch
```

## ✅ Next Steps

After successful installation:

1. **Read Configuration Guide**: [docs/CONFIGURATION.md](CONFIGURATION.md)
2. **Start Web Interface**: `python main.py --web`
3. **Run Tests**: `python tests/comprehensive_test.py`
4. **Deploy to Production**: [docs/DEPLOYMENT.md](DEPLOYMENT.md)

---

**Installation complete!** KeyHound Enhanced is ready for enterprise Bitcoin cryptography operations.
