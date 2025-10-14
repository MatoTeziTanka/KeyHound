# KeyHound Enhanced - Getting Started Tutorial

**Version**: 2.0.0  
**Difficulty**: Beginner  
**Duration**: 30 minutes

---

## 🎯 **What You'll Learn**

In this tutorial, you'll learn how to:
- Install and set up KeyHound Enhanced
- Use the basic command-line interface
- Solve a small Bitcoin puzzle
- Test brainwallet security
- Access the web interface
- Understand the results

---

## 📋 **Prerequisites**

- Basic understanding of Bitcoin and cryptography
- Python 3.8+ installed on your system
- 4GB RAM and 2GB free disk space
- Internet connection for downloading dependencies

---

## 🚀 **Step 1: Installation**

### **Download KeyHound Enhanced**
```bash
# Clone the repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Verify Python version
python --version  # Should be 3.8 or higher
```

### **Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python main.py --help
```

**Expected Output**:
```
usage: main.py [-h] [--web] [--puzzle BITS] [--brainwallet-test] [--gpu]
               [--distributed] [--config CONFIG] [--log-level {DEBUG,INFO,WARNING,ERROR}]

KeyHound Enhanced - Bitcoin Cryptography Platform

optional arguments:
  -h, --help            show this help message and exit
  --web                 Start web interface dashboard
  --puzzle BITS         Solve Bitcoin puzzle with specified bit length
  --brainwallet-test    Test brainwallet security
  --gpu                 Enable GPU acceleration
  --distributed         Enable distributed computing
  --config CONFIG       Configuration file path
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging level
```

---

## 🧪 **Step 2: Test Basic Functionality**

### **Run the Simple Test**
```bash
# Test basic functionality
python core/simple_keyhound.py
```

**Expected Output**:
```
KeyHound Enhanced - Simplified Core
========================================
Platform: Windows-10-10.0.19041-SP0
CPU Cores: 8
Memory: 16.0 GB

Testing brainwallet security...
Patterns tested: 10
Vulnerable patterns: 3

Vulnerable patterns:
  - 'password' (score: 70)
  - '123456' (score: 80)
  - 'bitcoin' (score: 60)

Testing puzzle solving (40-bit demo)...
Attempts: 100000, Rate: 1247 keys/sec
Performance: 1247 keys/sec
```

### **What Just Happened?**
- KeyHound checked your system capabilities
- Tested 10 common brainwallet patterns for security vulnerabilities
- Attempted to solve a 40-bit Bitcoin puzzle (demonstration only)
- Showed performance metrics

---

## 🔐 **Step 3: Brainwallet Security Testing**

### **Test Common Passwords**
```bash
# Test brainwallet security
python main.py --brainwallet-test
```

**What This Does**:
- Tests 5,000+ common brainwallet patterns
- Generates Bitcoin addresses from each pattern
- Assesses security vulnerabilities
- Reports vulnerable patterns

### **Custom Pattern Testing**
```python
# Create a custom test script
cat > test_custom_patterns.py << 'EOF'
from core.simple_keyhound import SimpleKeyHound

# Initialize KeyHound
keyhound = SimpleKeyHound(verbose=True)

# Test your own patterns
my_patterns = [
    "password123",
    "mysecretpass",
    "bitcoin2024",
    "companyname"
]

print("Testing custom brainwallet patterns...")
results = keyhound.test_brainwallet_security(my_patterns)

print(f"\nResults for {len(my_patterns)} patterns:")
for result in results:
    status = "VULNERABLE" if result.get("vulnerable") else "SECURE"
    print(f"  {status}: '{result['pattern']}' -> {result['address']}")
    if result.get("vulnerable"):
        print(f"    Private Key: {result['private_key']}")
EOF

# Run the custom test
python test_custom_patterns.py
```

---

## 🧩 **Step 4: Bitcoin Puzzle Solving**

### **Solve a Small Puzzle (20-bit)**
```bash
# Solve a 20-bit puzzle (safe for demonstration)
python main.py --puzzle 20
```

**What This Does**:
- Searches through ~1 million possible private keys
- Should complete in seconds to minutes
- Demonstrates the puzzle-solving process

### **Monitor Progress**
```bash
# Solve with verbose output
python main.py --puzzle 30 --log-level DEBUG
```

### **Understanding Puzzle Difficulty**
| Bits | Keyspace | Time to Solve |
|------|----------|---------------|
| 20-bit | ~1 million | Seconds |
| 30-bit | ~1 billion | Minutes |
| 40-bit | ~1 trillion | Hours |
| 50-bit | ~1 quadrillion | Days |
| 66-bit | ~73 quintillion | Months/Years |

---

## 🌐 **Step 5: Web Interface**

### **Start the Web Dashboard**
```bash
# Start web interface
python main.py --web
```

### **Access the Dashboard**
1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the KeyHound Enhanced dashboard

### **Dashboard Features**
- **System Status**: View system information and performance
- **Puzzle Solver**: Start and monitor puzzle solving
- **Brainwallet Tester**: Test patterns for vulnerabilities
- **Results**: View found keys and results
- **Configuration**: Adjust settings and parameters

### **Try the Web Interface**
1. Click on "Puzzle Solver"
2. Select "20-bit puzzle" for a quick demo
3. Click "Start Solving"
4. Watch the real-time progress

---

## 📊 **Step 6: Understanding Results**

### **Puzzle Results**
When a puzzle is solved, you'll see:
```json
{
  "private_key": "0000000000000000000000000000000000000000000000000000000000000001",
  "public_key": "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",
  "address": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
  "attempts": 1048576,
  "time_taken": 45.2,
  "keys_per_second": 23204
}
```

### **Brainwallet Results**
For brainwallet testing:
```json
{
  "pattern": "password",
  "private_key": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
  "address": "1J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
  "security_score": 70,
  "vulnerable": true
}
```

---

## 🎯 **Step 7: Next Steps**

### **Explore More Features**
```bash
# Try GPU acceleration (if available)
python main.py --puzzle 40 --gpu

# Test with different configurations
python main.py --puzzle 30 --config config/environments/production.yaml

# Run comprehensive tests
python tests/simple_functionality_test.py
```

### **Learn Advanced Usage**
- Read the [User Guide](docs/user/USER_GUIDE.md)
- Check the [API Reference](docs/api/API_REFERENCE.md)
- Explore [Examples](examples/)

### **Join the Community**
- Report issues on GitHub
- Contribute to development
- Share your results and experiences

---

## ❓ **Troubleshooting**

### **Common Issues**

#### **Import Errors**
```bash
# If you get "ModuleNotFoundError"
pip install -r requirements.txt

# If you get "No module named 'core'"
# Make sure you're in the KeyHound directory
pwd  # Should show .../KeyHound
```

#### **Permission Errors**
```bash
# On Linux/Mac, if you get permission errors
chmod +x scripts/*.sh
sudo chown -R $USER:$USER data/ results/
```

#### **Memory Issues**
```bash
# If you run out of memory, try smaller puzzles
python main.py --puzzle 20  # Instead of 40-bit
```

#### **Web Interface Won't Start**
```bash
# Check if port 5000 is in use
netstat -tlnp | grep 5000

# Try a different port
python main.py --web --port 5001
```

### **Getting Help**
- Check the [User Guide](docs/user/USER_GUIDE.md)
- Look at [Troubleshooting](docs/user/USER_GUIDE.md#troubleshooting)
- Report issues on GitHub
- Join discussions in the community

---

## 🎉 **Congratulations!**

You've successfully:
- ✅ Installed KeyHound Enhanced
- ✅ Tested basic functionality
- ✅ Explored brainwallet security testing
- ✅ Solved a Bitcoin puzzle
- ✅ Used the web interface
- ✅ Understood the results

### **What's Next?**
- Try solving larger puzzles (30-bit, 40-bit)
- Test more brainwallet patterns
- Explore the advanced features
- Learn about GPU acceleration
- Set up distributed computing

### **Resources**
- [User Guide](docs/user/USER_GUIDE.md) - Comprehensive user documentation
- [API Reference](docs/api/API_REFERENCE.md) - Technical API documentation
- [Deployment Guide](docs/deployment/DEPLOYMENT_GUIDE.md) - Production deployment
- [Development Guide](docs/development/DEVELOPMENT_GUIDE.md) - Contributing to the project

---

**KeyHound Enhanced Getting Started Tutorial v2.0.0**  
*Welcome to the world of Bitcoin cryptography!*
