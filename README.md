# KeyHound Enhanced - Comprehensive Bitcoin Cryptographic Tool

A powerful cross-platform Python application designed to tackle Bitcoin puzzle challenges, conduct brainwallet security testing, perform academic research, and benchmark cryptographic performance. Built with efficiency and flexibility in mind, it supports CPU and optional GPU acceleration, letting you harness the full power of your hardware to process cryptographic computations at scale.

## 🚀 Features

### **Bitcoin Puzzle Solving**
- **Original 1000 Bitcoin Puzzles**: Solve the remaining Bitcoin puzzle challenges
- **Private Key Puzzles**: Target specific puzzles from [privatekeys.pw](https://privatekeys.pw/puzzles/bitcoin-puzzle-tx)
- **High-Priority Focus**: Puzzle #71 (narrowest key space) and #135 (exposed public key)
- **Multiple Algorithms**: Brute force and BSGS (Baby-step Giant-step) algorithms
- **Real-Time Progress**: Live progress tracking and performance metrics

### **Brainwallet Security Testing**
- **Vulnerability Assessment**: Test Bitcoin addresses against common weak patterns
- **Pattern Library**: Comprehensive database of weak passphrases and patterns
- **Custom Patterns**: Add your own patterns for specialized testing
- **Security Reports**: Detailed vulnerability analysis and recommendations

### **Academic Research & Penetration Testing**
- **Entropy Analysis**: Study entropy patterns in private keys
- **Pattern Analysis**: Analyze patterns in Bitcoin addresses and keys
- **Collision Studies**: Research hash collisions in cryptographic operations
- **Vulnerability Research**: Academic-grade security assessment tools

### **Performance Benchmarking**
- **Speed Testing**: Measure cryptographic operations per second
- **Hardware Optimization**: CPU and GPU performance analysis
- **Competitive Benchmarking**: Compare against other tools like Brainflayer
- **Performance Reports**: Detailed performance metrics and optimization suggestions

### **Enterprise Features**
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multi-Threading**: Efficient CPU-based cryptographic computations
- **GPU Acceleration**: Optional GPU support for faster processing
- **Professional Documentation**: Comprehensive guides and API documentation
- **Results Export**: Save findings to JSON for analysis and reporting

## 📊 Current Bitcoin Puzzle Status

Based on [privatekeys.pw data](https://privatekeys.pw/puzzles/bitcoin-puzzle-tx):
- **Total Prize**: 988.498 BTC (916.5 BTC remaining)
- **Recently Solved**: Puzzles #66-69 (2024-2025)
- **High Priority**: Puzzle #71 (narrowest key space)
- **BSGS Candidates**: Puzzle #135 (exposed public key)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run KeyHound Enhanced:**
```bash
python keyhound_enhanced.py --list-puzzles
```

## 📖 Usage Examples

### **Bitcoin Puzzle Solving**
```bash
# Solve Puzzle #71 (highest priority - narrowest key space)
python keyhound_enhanced.py --puzzle 71

# Solve Puzzle #135 (BSGS algorithm - exposed public key)
python keyhound_enhanced.py --puzzle 135

# List all available puzzles
python keyhound_enhanced.py --list-puzzles
```

### **Brainwallet Security Testing**
```bash
# Test brainwallet security for specific address
python keyhound_enhanced.py --brainwallet-test 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU

# Interactive mode for multiple tests
python keyhound_enhanced.py
KeyHound> test 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU
```

### **Performance Benchmarking**
```bash
# Run 60-second performance benchmark
python keyhound_enhanced.py --benchmark 60

# Run extended benchmark
python keyhound_enhanced.py --benchmark 300
```

### **Academic Research Mode**
```bash
# Entropy analysis research
python keyhound_enhanced.py --research entropy_analysis

# Pattern analysis research
python keyhound_enhanced.py --research pattern_analysis

# Collision study research
python keyhound_enhanced.py --research collision_study
```

### **Advanced Configuration**
```bash
# Enable GPU acceleration
python keyhound_enhanced.py --puzzle 71 --gpu

# Use specific number of CPU threads
python keyhound_enhanced.py --puzzle 71 --threads 8

# Save results to file
python keyhound_enhanced.py --puzzle 71 --save-results results.json
```

## 🎯 Target Puzzles

### **High Priority (Recommended)**
- **Puzzle #71**: 270-271 bits, narrowest key space, highest success probability
- **Puzzle #72**: 271-272 bits, second narrowest key space
- **Puzzle #135**: 2134-2135 bits, exposed public key, BSGS algorithm

### **Medium Priority**
- **Puzzle #151**: 2150-2151 bits, good balance of difficulty and reward
- **Puzzle #152**: 2151-2152 bits, moderate difficulty
- **Puzzle #155**: 2154-2155 bits, exposed public key

### **Low Priority (High Difficulty)**
- **Puzzle #160**: 2159-2160 bits, highest difficulty but largest reward

## 🔧 Advanced Features

### **Interactive Mode**
```bash
python keyhound_enhanced.py
KeyHound> puzzle 71
KeyHound> test 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU
KeyHound> benchmark
KeyHound> list
KeyHound> quit
```

### **Results Export**
All results are automatically saved with timestamps:
- Found private keys and addresses
- Benchmark performance metrics
- Security test vulnerabilities
- Research analysis data

### **Performance Optimization**
- **Multi-threading**: Automatic CPU core detection and utilization
- **Memory Optimization**: Efficient key space traversal
- **Progress Tracking**: Real-time speed and progress monitoring
- **GPU Framework**: Ready for CUDA/OpenCL acceleration

## 📈 Performance Comparison

KeyHound Enhanced vs. Existing Tools:
- **vs. Brainflayer**: Modern Python implementation with active maintenance
- **vs. KeyHunt**: Enhanced user interface and comprehensive features
- **vs. Kangaroo**: Cross-platform support and educational focus
- **vs. BitCrack**: Better documentation and research capabilities

## 🔒 Security & Ethics

### **Intended Use Cases**
- ✅ **Educational Research**: Learning Bitcoin cryptography
- ✅ **Security Testing**: Testing your own brainwallets
- ✅ **Academic Studies**: Cryptographic vulnerability research
- ✅ **Performance Benchmarking**: Hardware optimization studies

### **Important Disclaimers**
- ⚠️ **Educational Purpose**: This tool is for educational and research purposes only
- ⚠️ **Legal Compliance**: Use responsibly and in accordance with applicable laws
- ⚠️ **Ethical Use**: Do not use to attack systems you don't own
- ⚠️ **No Warranty**: Use at your own risk

## 📚 Documentation

- **[VERSIONING.md](VERSIONING.md)**: Version management and release strategy
- **[CHANGELOG.md](CHANGELOG.md)**: Detailed release history and changes
- **[puzzle_data.py](puzzle_data.py)**: Bitcoin puzzle challenge data and configurations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Code formatting
black keyhound_enhanced.py

# Type checking
mypy keyhound_enhanced.py
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Brainflayer**: Inspiration from [ryancdotorg/brainflayer](https://github.com/ryancdotorg/brainflayer)
- **Bitcoin Puzzle Data**: Based on [privatekeys.pw/puzzles/bitcoin-puzzle-tx](https://privatekeys.pw/puzzles/bitcoin-puzzle-tx)
- **Cryptographic Libraries**: secp256k1, cryptography, ecdsa

---

**KeyHound Enhanced** - The ultimate Bitcoin cryptographic research and puzzle-solving tool. 🐕‍🦺🔍

