# 🔑 KeyHound Enhanced - Enterprise Bitcoin Cryptography Platform

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/sethpizzaboy/KeyHound)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

**Professional, enterprise-grade Bitcoin cryptography and puzzle solving platform with optimal organization and deployment strategies.**

## 🏗️ Optimal Structure

KeyHound Enhanced follows the **BEST OF THE BEST** organization:

```
KeyHound/
├── 📁 keyhound/                    # Main Python package
│   ├── main.py                     # Single consolidated entry point
│   ├── core/                       # Bitcoin cryptography & system management
│   ├── gpu/                        # GPU acceleration frameworks
│   ├── ml/                         # Machine learning components
│   ├── web/                        # Web interface & mobile app
│   └── distributed/                # Distributed computing
├── 📁 deployments/                 # All deployment configurations
│   ├── docker/                     # Docker deployment
│   ├── colab/                      # Google Colab integration
│   ├── cloud/                      # Cloud deployment (AWS, GCP, Azure)
│   └── local/                      # Local development
├── 📁 config/                      # Environment-specific configurations
├── 📁 tests/                       # Comprehensive testing suite
├── 📁 docs/                        # Professional documentation
├── 📁 scripts/                     # Utility and deployment scripts
├── 📁 monitoring/                  # Monitoring & observability
├── 📁 examples/                    # Usage examples and tutorials
└── 📁 data/                        # Data storage and results
```

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Install package
pip install -e .

# Run with web interface
keyhound --web

# Solve Bitcoin puzzle with GPU
keyhound --puzzle 66 --gpu

# Test brainwallet security
keyhound --brainwallet-test
```

### Google Colab (Recommended for Research)
```python
# Use the optimized notebook
# deployments/colab/KeyHound_Enhanced.ipynb
# Expected performance: 20,000-100,000+ keys/second
```

### Docker Deployment (Recommended for Production)
```bash
# Deploy with GPU support
cd deployments/docker
docker-compose up -d

# Access web interface
# http://localhost:5000
```

## 🎯 Core Features

### 🔑 Bitcoin Cryptography
- **Multi-bit puzzle support**: 40-bit to 160-bit puzzles
- **Proper Bitcoin implementation**: secp256k1, SHA-256, RIPEMD-160
- **Address generation**: Legacy, P2SH, Bech32 formats
- **Message signing**: Bitcoin message signing and verification

### ⚡ Performance & Scalability
- **GPU acceleration**: CUDA, OpenCL, Numba support
- **Distributed computing**: Multi-node coordination
- **Memory optimization**: Intelligent caching and streaming
- **Real-time monitoring**: Performance metrics and alerts

### 🧠 Advanced Features
- **Machine learning**: Pattern recognition for brainwallets
- **Web interface**: Real-time dashboard and API
- **Mobile app**: Progressive Web App companion
- **Result persistence**: Encrypted storage with backups

## 📊 Performance Expectations

| Environment | GPU | Expected Speed | Best For |
|-------------|-----|----------------|----------|
| **Google Colab** | A100 (Pro) | 100,000+ keys/sec | Research |
| **Google Colab** | T4 (Free) | 20,000+ keys/sec | Testing |
| **Docker** | NVIDIA GPU | 50,000+ keys/sec | Production |
| **Local** | CUDA GPU | 30,000+ keys/sec | Development |
| **CPU Only** | None | 1,000+ keys/sec | Fallback |

## 🔧 Configuration

KeyHound Enhanced uses environment-specific configurations:

- **Production**: `config/environments/production.yaml`
- **Development**: `config/environments/development.yaml`
- **Colab**: `config/environments/colab.yaml`
- **Testing**: `config/environments/testing.yaml`

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)**: Detailed setup instructions
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Multi-environment deployment
- **[API Reference](docs/api/)**: Programmatic interface
- **[User Guide](docs/user/)**: End-user documentation
- **[Development Guide](docs/development/)**: Developer documentation

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/           # Unit tests
pytest tests/integration/    # Integration tests
pytest tests/performance/    # Performance tests
```

## 🚀 Deployment Options

### 1. Google Colab (Research/Testing)
- **Best for**: Research, testing, GPU access without setup
- **Performance**: High with A100/T4 GPUs
- **Setup**: Use `deployments/colab/KeyHound_Enhanced.ipynb`

### 2. Docker (Production)
- **Best for**: Production servers, scalable deployment
- **Performance**: Maximum with full GPU support
- **Setup**: `cd deployments/docker && docker-compose up -d`

### 3. Local Development
- **Best for**: Development, debugging
- **Performance**: Depends on local hardware
- **Setup**: `pip install -e . && keyhound --web`

### 4. Cloud Deployment
- **Best for**: Enterprise, scalable production
- **Performance**: Maximum scalability
- **Setup**: Use deployment scripts in `scripts/deployment/`

## 🔒 Security & Compliance

- **Authentication**: Web interface authentication
- **Data encryption**: Encrypted result storage
- **Audit logging**: Complete activity tracking
- **Network security**: Firewall and access controls
- **Compliance**: Enterprise security standards

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Users are responsible for compliance with applicable laws and regulations.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/sethpizzaboy/KeyHound/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sethpizzaboy/KeyHound/discussions)

---

**KeyHound Enhanced** - The most professional, optimally organized Bitcoin cryptography platform for the modern era.
