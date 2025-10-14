# KeyHound Enhanced - User Guide

**Version**: 2.0.0  
**Last Updated**: October 13, 2025

---

## 📖 **Table of Contents**

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Bitcoin Puzzle Solving](#bitcoin-puzzle-solving)
4. [Brainwallet Security Testing](#brainwallet-security-testing)
5. [Web Interface](#web-interface)
6. [Command Line Interface](#command-line-interface)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- GPU with CUDA support (optional, for acceleration)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

### **Quick Test**
```bash
# Test basic functionality
python core/simple_keyhound.py

# Start web interface
python main.py --web
```

---

## 💻 **Basic Usage**

### **Command Line Interface**

#### **Web Interface**
```bash
# Start web dashboard
python main.py --web

# Start with specific configuration
python main.py --web --config config/environments/production.yaml
```

#### **Puzzle Solving**
```bash
# Solve 40-bit Bitcoin puzzle
python main.py --puzzle 40

# Solve with GPU acceleration
python main.py --puzzle 66 --gpu

# Solve with timeout
python main.py --puzzle 40 --timeout 3600
```

#### **Brainwallet Testing**
```bash
# Test common brainwallet patterns
python main.py --brainwallet-test

# Test specific patterns
python main.py --brainwallet-test --patterns "password123,bitcoin,123456"
```

### **Python API Usage**

#### **Basic Import and Setup**
```python
from core.simple_keyhound import SimpleKeyHound

# Initialize KeyHound
keyhound = SimpleKeyHound(verbose=True)

# Get system information
system_info = keyhound.get_system_info()
print(f"System: {system_info}")
```

#### **Bitcoin Cryptography**
```python
from core.bitcoin_cryptography import BitcoinCryptography

# Initialize cryptography module
crypto = BitcoinCryptography()

# Generate private key
private_key = crypto.generate_private_key()
print(f"Private Key: {private_key}")

# Generate Bitcoin address
address = crypto.generate_bitcoin_address(private_key)
print(f"Address: {address}")

# Validate address
is_valid = crypto.validate_bitcoin_address(address)
print(f"Valid: {is_valid}")
```

---

## 🧩 **Bitcoin Puzzle Solving**

### **Available Puzzles**
KeyHound Enhanced supports solving Bitcoin puzzles of various bit lengths:

- **40-bit**: ~1 trillion keys (solvable in hours)
- **50-bit**: ~1 quadrillion keys (solvable in days)
- **66-bit**: ~73 quintillion keys (solvable in months/years)
- **Higher bits**: Requires distributed computing

### **Solving Strategies**

#### **Random Search**
```python
# Basic random search
result = keyhound.solve_puzzle(
    bits=40,
    max_attempts=1000000,
    timeout=3600  # 1 hour
)

if result:
    print(f"Found! Private Key: {result['private_key']}")
    print(f"Address: {result['address']}")
    print(f"Attempts: {result['attempts']}")
```

#### **Targeted Search**
```python
# Search for specific address
result = keyhound.solve_puzzle(
    bits=40,
    target_address="1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    max_attempts=10000000
)
```

### **Performance Optimization**

#### **GPU Acceleration**
```python
# Enable GPU acceleration
keyhound = KeyHoundEnhanced(use_gpu=True, gpu_framework="cuda")
result = keyhound.solve_puzzle(bits=50, max_attempts=100000000)
```

#### **Distributed Computing**
```python
# Enable distributed computing
keyhound = KeyHoundEnhanced(distributed=True)
result = keyhound.solve_puzzle(bits=66, max_attempts=1000000000)
```

---

## 🔐 **Brainwallet Security Testing**

### **What are Brainwallets?**
Brainwallets are Bitcoin wallets where the private key is derived from a memorable passphrase using cryptographic hash functions.

### **Security Testing**
```python
# Test common patterns
patterns = [
    "password",
    "123456",
    "bitcoin",
    "wallet",
    "crypto"
]

results = keyhound.test_brainwallet_security(patterns)

for result in results:
    if result.get("vulnerable"):
        print(f"VULNERABLE: '{result['pattern']}' -> {result['address']}")
        print(f"Private Key: {result['private_key']}")
```

### **Pattern Library**
KeyHound Enhanced includes a comprehensive library of 5,000+ common brainwallet patterns:

- **Common passwords**: password, 123456, admin
- **Bitcoin-related**: bitcoin, wallet, crypto, blockchain
- **Dates and years**: 2009, 2010, 2020, 2021
- **Combinations**: password123, bitcoin2020
- **Phrases**: "my bitcoin wallet", "satoshi nakamoto"

---

## 🌐 **Web Interface**

### **Dashboard Features**
- **Real-time Monitoring**: Live performance metrics
- **Puzzle Progress**: Visual progress tracking
- **Results Management**: View and export found keys
- **Configuration**: Easy settings management
- **Logs**: Real-time log viewing

### **Accessing the Web Interface**
1. Start the web server: `python main.py --web`
2. Open browser to: `http://localhost:5000`
3. Use default credentials or configure authentication

### **Web Interface Components**

#### **Main Dashboard**
- System status and performance metrics
- Active puzzle solving progress
- Recent results and discoveries

#### **Puzzle Solver**
- Interactive puzzle selection
- Real-time progress monitoring
- Performance statistics

#### **Brainwallet Tester**
- Pattern library browser
- Security assessment results
- Vulnerability reports

#### **Configuration**
- Environment settings
- Performance tuning
- Security options

---

## ⚙️ **Configuration**

### **Configuration Files**
KeyHound Enhanced uses YAML configuration files:

- `config/default.yaml` - Default settings
- `config/environments/production.yaml` - Production settings
- `config/environments/docker.yaml` - Docker settings
- `config/environments/colab.yaml` - Google Colab settings

### **Key Configuration Options**

#### **Performance Settings**
```yaml
performance:
  max_threads: 4
  memory_limit_gb: 8
  cache_size: 1000
  save_interval_minutes: 15
```

#### **GPU Settings**
```yaml
gpu:
  enabled: true
  framework: "cuda"
  batch_size: 5000
  max_memory_usage: 0.8
```

#### **Security Settings**
```yaml
security:
  enable_authentication: true
  session_timeout_minutes: 30
  max_login_attempts: 3
```

### **Environment Variables**
```bash
# Security
export SECRET_KEY="your-secret-key"
export SESSION_SECRET="your-session-secret"

# Performance
export MAX_THREADS=8
export MEMORY_LIMIT_GB=16

# GPU
export GPU_ENABLED=true
export GPU_FRAMEWORK=cuda
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Install dependencies
pip install -r requirements.txt

# Error: CUDA not found
# Solution: Install CUDA toolkit or disable GPU
python main.py --puzzle 40  # Without --gpu flag
```

#### **Memory Issues**
```bash
# Error: Out of memory
# Solution: Reduce memory usage
# Edit config/default.yaml:
performance:
  max_threads: 2
  memory_limit_gb: 4
```

#### **Permission Errors**
```bash
# Error: Permission denied
# Solution: Check file permissions
chmod +x scripts/*.sh
chmod 755 data/ results/
```

### **Performance Issues**

#### **Slow Performance**
1. **Check CPU usage**: Use `htop` or Task Manager
2. **Enable GPU**: Use `--gpu` flag if available
3. **Optimize threads**: Adjust `max_threads` in config
4. **Check memory**: Ensure sufficient RAM available

#### **GPU Not Working**
1. **Verify CUDA**: Run `nvidia-smi`
2. **Install PyTorch**: `pip install torch torchvision torchaudio`
3. **Check drivers**: Update NVIDIA drivers
4. **Test GPU**: Run GPU test script

### **Getting Help**

#### **Logs**
```bash
# View logs
tail -f logs/keyhound.log

# Check error logs
grep "ERROR" logs/keyhound.log
```

#### **Debug Mode**
```bash
# Enable debug logging
python main.py --web --log-level DEBUG
```

---

## 📋 **Best Practices**

### **Security**
1. **Use strong passwords** for web interface
2. **Enable authentication** in production
3. **Use HTTPS** for web access
4. **Regular backups** of important results
5. **Keep dependencies updated**

### **Performance**
1. **Start small**: Begin with 40-bit puzzles
2. **Monitor resources**: Watch CPU, memory, and GPU usage
3. **Use GPU acceleration** when available
4. **Optimize configuration** for your hardware
5. **Save progress regularly**

### **Development**
1. **Use version control** for custom modifications
2. **Test thoroughly** before production use
3. **Document custom configurations**
4. **Follow coding standards**
5. **Regular security reviews**

### **Production Deployment**
1. **Use Docker** for consistent deployment
2. **Enable monitoring** and alerting
3. **Implement backup strategies**
4. **Use environment variables** for secrets
5. **Regular security updates**

---

## 🎯 **Examples and Tutorials**

### **Tutorial 1: First Puzzle Solve**
```bash
# Step 1: Test basic functionality
python core/simple_keyhound.py

# Step 2: Solve a small puzzle
python main.py --puzzle 40 --max-attempts 100000

# Step 3: Check results
ls results/puzzle_solutions/
```

### **Tutorial 2: Brainwallet Security Audit**
```python
from core.simple_keyhound import SimpleKeyHound

keyhound = SimpleKeyHound()

# Test your own patterns
my_patterns = ["mysecretpass", "companyname2024"]
results = keyhound.test_brainwallet_security(my_patterns)

for result in results:
    print(f"Pattern: {result['pattern']}")
    print(f"Security Score: {result['security_score']}")
    print(f"Vulnerable: {result['vulnerable']}")
```

### **Tutorial 3: Web Interface Setup**
```bash
# Step 1: Start web server
python main.py --web

# Step 2: Access dashboard
# Open http://localhost:5000 in browser

# Step 3: Configure settings
# Go to Settings tab and adjust configuration

# Step 4: Start puzzle solving
# Use the web interface to start solving puzzles
```

---

## 📞 **Support and Community**

### **Getting Help**
- **Documentation**: Check this user guide and API reference
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions
- **Security**: Report security issues privately

### **Contributing**
- **Code**: Submit pull requests for improvements
- **Documentation**: Help improve guides and examples
- **Testing**: Report bugs and test new features
- **Feedback**: Share your experience and suggestions

---

**KeyHound Enhanced User Guide v2.0.0**  
*Professional Bitcoin Cryptography Platform*
