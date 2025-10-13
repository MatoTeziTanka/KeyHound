# 🔑 KeyHound Enhanced - Enterprise Bitcoin Cryptography Platform

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/sethpizzaboy/KeyHound)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

**Enterprise-grade Bitcoin cryptography and puzzle solving platform with GPU acceleration, distributed computing, and machine learning capabilities.**

## 🏗️ Architecture Overview

KeyHound Enhanced follows a modular, enterprise-grade architecture:

```
KeyHound/
├── src/                          # Core application source code
│   ├── core/                     # Bitcoin cryptography & system management
│   ├── gpu/                      # GPU acceleration frameworks
│   ├── ml/                       # Machine learning components
│   ├── web/                      # Web interface & mobile app
│   └── distributed/              # Distributed computing
├── tests/                        # Comprehensive test suite
├── docs/                         # Documentation & guides
├── scripts/                      # Deployment & utility scripts
├── config/                       # Configuration files
├── templates/                    # Web interface templates
├── static/                       # Static web assets
└── main.py                       # Production entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (optional, for acceleration)
- 8GB+ RAM recommended

### Installation
```bash
# Clone repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Install dependencies
pip install -r requirements.txt

# Run with web interface
python main.py --web

# Solve Bitcoin puzzle
python main.py --puzzle 66 --gpu

# Test brainwallet security
python main.py --brainwallet-test
```

## 🔧 Core Features

### 🎯 Bitcoin Puzzle Solving
- **Multi-bit puzzle support**: 40-bit to 160-bit puzzles
- **GPU acceleration**: CUDA, OpenCL, Numba support
- **Distributed computing**: Multi-node coordination
- **Progress tracking**: Real-time statistics and recovery

### 🧠 Brainwallet Security Testing
- **Pattern recognition**: ML-powered vulnerability detection
- **Dictionary attacks**: Comprehensive password testing
- **Custom patterns**: User-defined attack vectors
- **Security reporting**: Detailed vulnerability analysis

### ⚡ Performance Features
- **Memory optimization**: Intelligent caching and streaming
- **Real-time monitoring**: CPU, GPU, memory metrics
- **Result persistence**: Encrypted storage with backups
- **Web dashboard**: Real-time progress visualization

## 📊 Usage Examples

### Command Line Interface
```bash
# Start web interface
python main.py --web

# Solve 66-bit puzzle with GPU
python main.py --puzzle 66 --gpu

# Enable distributed computing
python main.py --puzzle 40 --distributed --gpu

# Test brainwallet security
python main.py --brainwallet-test

# Custom configuration
python main.py --config config/production.yaml --puzzle 50
```

### Programmatic Usage
```python
from src.core.keyhound_enhanced import KeyHoundEnhanced

# Initialize with configuration
keyhound = KeyHoundEnhanced(config_file='config/default.yaml')

# Enable GPU acceleration
keyhound.enable_gpu_acceleration()

# Solve puzzle
result = keyhound.solve_puzzle(66)

# Test brainwallet
keyhound.test_brainwallet_security()
```

## 🔧 Configuration

KeyHound Enhanced uses YAML configuration files. See `config/default.yaml` for options:

```yaml
# GPU Settings
gpu:
  enabled: true
  framework: "cuda"
  batch_size: 10000

# Performance Settings  
performance:
  max_threads: 8
  memory_limit_gb: 16

# Web Interface
web:
  host: "0.0.0.0"
  port: 5000
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python tests/comprehensive_test.py
python tests/scaled_test.py
```

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Configuration Guide](docs/CONFIGURATION.md)** - Configuration options
- **[API Reference](docs/API.md)** - Programmatic interface
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[Found Keys Guide](docs/FOUND_KEYS_GUIDE.md)** - Key discovery workflow

## 🔒 Security Considerations

- **Private keys**: Never store unencrypted private keys
- **Network security**: Use HTTPS in production
- **Access control**: Enable authentication for web interface
- **Audit logging**: Monitor all key generation activities

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Users are responsible for compliance with applicable laws and regulations. The authors are not responsible for any misuse of this software.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/sethpizzaboy/KeyHound/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sethpizzaboy/KeyHound/discussions)

---

**KeyHound Enhanced** - Enterprise Bitcoin cryptography platform for the modern era.