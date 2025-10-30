# 🔑 KeyHound Enhanced - Enterprise Bitcoin Cryptography Platform

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/sethpizzaboy/KeyHound)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
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

### CPU-only mode (current default)

At present, GPU acceleration may be unavailable on some legacy GPUs (e.g., GRID K1/Kepler). You can run CPU-only mode reliably:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Minimal output, writes progress to run.log
PYTHONWARNINGS=ignore python3 main.py --puzzle 66 --log-level WARNING > run.log 2>&1 &

# Monitor progress
tail -f run.log
```

When a supported NVIDIA GPU and driver are available, enable acceleration with:

```bash
python3 main.py --puzzle 66 --gpu --log-level INFO | tee run_gpu.log
```

### Dashboard and notifications

Run a real-time dashboard (port 8080 by default):

```bash
pip install flask flask-socketio
python3 web/remote_stats_server.py --host 0.0.0.0 --port 8080
# Open http://<vm-ip>:8080
```

Operations runbook: see `OPERATIONS.md` for services, ports, backups, and reboot flow.

## 🧭 Runbook (VM191)

1) Start/stop solver workers
```bash
sudo systemctl enable --now keyhound-solver@1.service
sudo systemctl enable --now keyhound-solver@2.service
sudo systemctl enable --now keyhound-solver@3.service
sudo systemctl enable --now keyhound-solver@4.service
```
2) Dashboard and throughput
```bash
sudo systemctl enable --now keyhound-dashboard.service
sudo systemctl enable --now keyhound-throughput.service
# Dashboard: http://<vm-ip>:5050  |  Throughput JSON: http://<vm-ip>:5051/api/throughput
```
3) Email alerts
```bash
export SMTP_PASSWORD='<gmail_app_password>'
export ALERT_EMAILS='sethpizzaboy@aol.com,sethpizzaboy@gmail.com,setsch0666@students.ecpi.edu'
```
4) Checkpoints
```bash
sudo systemctl enable --now keyhound-checkpoint.timer
sudo systemctl start keyhound-checkpoint.service  # manual
```
5) Reboot verification
```bash
systemctl --no-pager --type=service | egrep 'keyhound-(solver@|dashboard|throughput)'
systemctl list-timers | grep keyhound
curl -s http://127.0.0.1:5050/api/health
```

For packaging and service details, see `docs/PACKAGING.md`.

Email alerts when a key/puzzle is found (uses Gmail SMTP account):

```bash
export SMTP_PASSWORD='<gmail_app_password_for_lightspeedup.smtp@gmail.com>'
export ALERT_EMAILS='sethpizzaboy@aol.com,sethpizzaboy@gmail.com,setsch0666@students.ecpi.edu'
# Notification system is invoked by the solver when an event is detected.
# You can test delivery:
python3 -c "from core.working_notification_system import WorkingNotificationSystem as W; W().send_email_notification('KeyHound test','This is a test')"
```

### Checkpointing (every 30–60 minutes)

Persist logs and results periodically to survive power loss:

```bash
mkdir -p checkpoints
(crontab -l 2>/dev/null; echo "*/30 * * * * cd $HOME/KeyHound && ts=\$(date +\%Y\%m\%d_\%H\%M); mkdir -p checkpoints/\$ts; cp -a run*.log results performance_metrics.db checkpoints/\$ts/ 2>/dev/null") | crontab -
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

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Users are responsible for compliance with applicable laws and regulations.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/sethpizzaboy/KeyHound/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sethpizzaboy/KeyHound/discussions)

---

**KeyHound Enhanced** - The most professional, optimally organized Bitcoin cryptography platform for the modern era.
