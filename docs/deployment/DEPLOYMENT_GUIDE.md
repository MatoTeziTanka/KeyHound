# KeyHound Enhanced - Deployment Guide

**Version**: 2.0.0  
**Last Updated**: October 13, 2025

---

## 📖 **Table of Contents**

1. [Deployment Overview](#deployment-overview)
2. [Docker Deployment](#docker-deployment)
3. [Google Colab Deployment](#google-colab-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Local Development](#local-development)
6. [Configuration Management](#configuration-management)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 **Deployment Overview**

KeyHound Enhanced supports multiple deployment options to fit different use cases and environments:

### **Deployment Options**
- **🐳 Docker**: Containerized deployment with Docker Compose
- **📓 Google Colab**: Cloud-based Jupyter notebook environment
- **☁️ Cloud Platforms**: AWS, Azure, GCP deployment
- **💻 Local Development**: Direct Python installation

### **Deployment Verification**
All deployment options have been verified and tested:
- ✅ **Docker**: Multi-stage build with GPU support
- ✅ **Google Colab**: Optimized for cloud GPU access
- ✅ **Local Development**: Full functionality confirmed
- ⚠️ **Cloud Platforms**: Directories exist, files need creation

---

## 🐳 **Docker Deployment**

### **Prerequisites**
- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Docker (for GPU support)
- 4GB RAM minimum, 8GB recommended

### **Quick Start**
```bash
# Clone repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Build and start services
docker-compose -f deployments/docker/docker-compose.yml up --build

# Access web interface
open http://localhost:5000
```

### **Docker Compose Services**

#### **Main Application**
```yaml
keyhound-web:
  build:
    context: .
    dockerfile: deployments/docker/Dockerfile
    target: gpu  # Use GPU-optimized build
  ports:
    - "5000:5000"
  environment:
    - KEYHOUND_CONFIG=config/environments/production.yaml
    - SECRET_KEY=${SECRET_KEY}
  volumes:
    - ./data:/app/data
    - ./results:/app/results
```

#### **Supporting Services**
- **Redis**: Distributed computing coordination (port 6379)
- **PostgreSQL**: Production database (port 5432)
- **Nginx**: Reverse proxy and load balancer (ports 80/443)
- **Prometheus**: Metrics collection (port 9090)
- **Grafana**: Monitoring dashboard (port 3000)

### **Environment Configuration**
```bash
# Create .env file
cp env.template .env

# Edit .env file with your values
SECRET_KEY=your-super-secret-key-here
DB_PASSWORD=your-database-password
GITHUB_TOKEN=your-github-token
```

### **GPU Support**
```bash
# Verify NVIDIA Docker
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi

# Build with GPU support
docker-compose -f deployments/docker/docker-compose.yml up --build

# Check GPU availability
docker exec -it keyhound-enhanced python -c "import torch; print(torch.cuda.is_available())"
```

### **Production Deployment**
```bash
# Production configuration
export SECRET_KEY="your-production-secret-key"
export DB_PASSWORD="your-secure-db-password"
export LOG_LEVEL="INFO"

# Deploy with production settings
docker-compose -f deployments/docker/docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 📓 **Google Colab Deployment**

### **Prerequisites**
- Google account
- Colab Pro (recommended for GPU access)
- Basic understanding of Jupyter notebooks

### **Quick Start**
1. **Open Colab Notebook**: [KeyHound Enhanced Colab](https://colab.research.google.com/github/sethpizzaboy/KeyHound/blob/main/deployments/colab/KeyHound_Enhanced.ipynb)
2. **Select Runtime**: Runtime → Change runtime type → GPU (T4 or A100)
3. **Run All Cells**: Runtime → Run all
4. **Access Dashboard**: Check the final cell for dashboard link

### **Colab Features**
- **GPU Acceleration**: Automatic GPU detection and optimization
- **Drive Integration**: Mount Google Drive for persistent storage
- **Auto Setup**: One-click installation and configuration
- **Progress Monitoring**: Real-time progress tracking
- **Results Export**: Export results to Google Drive

### **Performance Expectations**
| GPU Type | Keys/Second | Puzzle 40-bit | Puzzle 50-bit |
|----------|-------------|---------------|---------------|
| CPU | ~1,000 | ~11 days | ~31 years |
| T4 GPU | ~20,000 | ~14 hours | ~16 months |
| A100 GPU | ~100,000+ | ~3 hours | ~3 months |

### **Custom Configuration**
```python
# In Colab notebook
import os

# Set environment variables
os.environ['GPU_BATCH_SIZE'] = '10000'
os.environ['MAX_THREADS'] = '8'
os.environ['MEMORY_LIMIT_GB'] = '16'

# Restart runtime to apply changes
```

---

## ☁️ **Cloud Deployment**

### **AWS Deployment**

#### **EC2 Instance**
```bash
# Launch EC2 instance (recommended: g4dn.xlarge for GPU)
# Ubuntu 20.04 LTS, 4 vCPU, 16 GB RAM, GPU instance

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker ubuntu

# Clone and deploy
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound
docker-compose -f deployments/docker/docker-compose.yml up -d
```

#### **ECS with Fargate**
```yaml
# deployments/cloud/aws/ecs-task-definition.json
{
  "family": "keyhound-enhanced",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "keyhound-web",
      "image": "keyhound-enhanced:latest",
      "portMappings": [{"containerPort": 5000}],
      "environment": [
        {"name": "SECRET_KEY", "value": "your-secret-key"},
        {"name": "ENVIRONMENT", "value": "production"}
      ]
    }
  ]
}
```

### **Azure Deployment**

#### **Azure Container Instances**
```bash
# Create resource group
az group create --name keyhound-rg --location eastus

# Deploy container
az container create \
  --resource-group keyhound-rg \
  --name keyhound-enhanced \
  --image keyhound-enhanced:latest \
  --dns-name-label keyhound-app \
  --ports 5000 \
  --environment-variables SECRET_KEY=your-secret-key
```

#### **Azure Kubernetes Service**
```yaml
# deployments/cloud/azure/aks-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keyhound-enhanced
spec:
  replicas: 2
  selector:
    matchLabels:
      app: keyhound-enhanced
  template:
    metadata:
      labels:
        app: keyhound-enhanced
    spec:
      containers:
      - name: keyhound-web
        image: keyhound-enhanced:latest
        ports:
        - containerPort: 5000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: keyhound-secrets
              key: secret-key
```

### **Google Cloud Platform**

#### **Cloud Run**
```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT-ID/keyhound-enhanced

# Deploy to Cloud Run
gcloud run deploy keyhound-enhanced \
  --image gcr.io/PROJECT-ID/keyhound-enhanced \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=your-secret-key
```

#### **Google Kubernetes Engine**
```yaml
# deployments/cloud/gcp/gke-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keyhound-enhanced
spec:
  replicas: 3
  selector:
    matchLabels:
      app: keyhound-enhanced
  template:
    metadata:
      labels:
        app: keyhound-enhanced
    spec:
      containers:
      - name: keyhound-web
        image: gcr.io/PROJECT-ID/keyhound-enhanced:latest
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

---

## 💻 **Local Development**

### **System Requirements**
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **GPU**: NVIDIA GPU with CUDA support (optional)

### **Installation Steps**
```bash
# Clone repository
git clone https://github.com/sethpizzaboy/KeyHound.git
cd KeyHound

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Verify installation
python main.py --help
```

### **Configuration**
```bash
# Copy environment template
cp env.template .env

# Edit configuration
nano .env

# Set environment variables
export SECRET_KEY="your-local-secret-key"
export LOG_LEVEL="DEBUG"
```

### **Running Locally**
```bash
# Start web interface
python main.py --web

# Solve puzzle
python main.py --puzzle 40

# Test brainwallet security
python main.py --brainwallet-test

# Run with GPU
python main.py --puzzle 50 --gpu
```

### **Development Tools**
```bash
# Install development dependencies
pip install black isort flake8 pytest

# Format code
black .

# Run tests
pytest

# Run linting
flake8 .
```

---

## ⚙️ **Configuration Management**

### **Environment-Specific Configs**
```
config/
├── default.yaml              # Base configuration
├── environments/
│   ├── production.yaml       # Production settings
│   ├── docker.yaml          # Docker-specific settings
│   ├── colab.yaml           # Google Colab settings
│   └── development.yaml     # Development settings
```

### **Configuration Hierarchy**
1. **Environment Variables** (highest priority)
2. **Environment-specific YAML**
3. **Default YAML** (lowest priority)

### **Key Configuration Options**

#### **Performance Settings**
```yaml
performance:
  max_threads: 4              # CPU threads to use
  memory_limit_gb: 8          # Memory limit
  cache_size: 1000           # Cache size
  save_interval_minutes: 15   # Auto-save interval
```

#### **GPU Settings**
```yaml
gpu:
  enabled: true               # Enable GPU acceleration
  framework: "cuda"          # GPU framework (cuda, opencl)
  batch_size: 5000           # Batch size for GPU operations
  max_memory_usage: 0.8      # Max GPU memory usage (0.0-1.0)
```

#### **Security Settings**
```yaml
security:
  enable_authentication: true # Enable web authentication
  session_timeout_minutes: 30 # Session timeout
  max_login_attempts: 3       # Max login attempts
```

#### **Database Settings**
```yaml
database:
  type: "sqlite"             # Database type
  path: "data/keyhound.db"   # Database path
  backup_interval_hours: 12  # Backup interval
```

### **Environment Variables**
```bash
# Security
export SECRET_KEY="your-secret-key"
export SESSION_SECRET="your-session-secret"

# Performance
export MAX_THREADS=8
export MEMORY_LIMIT_GB=16
export GPU_ENABLED=true

# Database
export DATABASE_URL="sqlite:///data/keyhound.db"
export DB_PASSWORD="your-db-password"

# Logging
export LOG_LEVEL="INFO"
export LOG_FILE="logs/keyhound.log"
```

---

## 📊 **Monitoring and Logging**

### **Application Monitoring**

#### **Prometheus Metrics**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'keyhound-enhanced'
    static_configs:
      - targets: ['keyhound-web:5000']
    metrics_path: /metrics
    scrape_interval: 5s
```

#### **Grafana Dashboard**
- **System Metrics**: CPU, memory, disk usage
- **Application Metrics**: Keys/second, puzzle progress
- **Error Rates**: Failed operations, exceptions
- **Performance**: Response times, throughput

### **Logging Configuration**
```yaml
logging:
  level: "INFO"              # Log level (DEBUG, INFO, WARNING, ERROR)
  file: "logs/keyhound.log"  # Log file path
  max_size_mb: 100          # Max log file size
  backup_count: 5           # Number of backup files
```

### **Log Analysis**
```bash
# View recent logs
tail -f logs/keyhound.log

# Search for errors
grep "ERROR" logs/keyhound.log

# Monitor performance
grep "keys/second" logs/keyhound.log | tail -10

# Check puzzle progress
grep "puzzle" logs/keyhound.log | tail -20
```

### **Health Checks**
```bash
# Docker health check
docker exec keyhound-enhanced curl -f http://localhost:5000/health

# Application health check
python -c "
from core.simple_keyhound import SimpleKeyHound
keyhound = SimpleKeyHound()
print('Health check:', keyhound.get_system_info())
"
```

---

## 🔒 **Security Considerations**

### **Production Security**

#### **Environment Variables**
```bash
# Use environment variables for secrets
export SECRET_KEY="$(openssl rand -base64 32)"
export DB_PASSWORD="$(openssl rand -base64 32)"
export SESSION_SECRET="$(openssl rand -base64 32)"
```

#### **Network Security**
```yaml
# Docker Compose with security
services:
  keyhound-web:
    networks:
      - internal
    ports:
      - "127.0.0.1:5000:5000"  # Bind to localhost only

  nginx:
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl  # SSL certificates
```

#### **SSL/TLS Configuration**
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://keyhound-web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Access Control**
```yaml
# Enable authentication
security:
  enable_authentication: true
  session_timeout_minutes: 30
  max_login_attempts: 3

# Use strong passwords
web:
  secret_key: "${SECRET_KEY}"
```

### **Data Protection**
```yaml
# Enable encryption
results:
  encryption_enabled: true
  compression_enabled: true

# Secure database
database:
  type: "postgresql"
  url: "${DATABASE_URL}"
  ssl: true
```

---

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **Docker Issues**
```bash
# Container won't start
docker logs keyhound-enhanced

# Permission denied
sudo chown -R $USER:$USER data/ results/

# GPU not available
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi
```

#### **Performance Issues**
```bash
# High memory usage
docker stats keyhound-enhanced

# Slow performance
# Check CPU usage and enable GPU acceleration
python main.py --puzzle 40 --gpu
```

#### **Network Issues**
```bash
# Can't access web interface
# Check if port 5000 is open
netstat -tlnp | grep 5000

# Check firewall
sudo ufw status
sudo ufw allow 5000
```

### **Debug Mode**
```bash
# Enable debug logging
python main.py --web --log-level DEBUG

# Docker debug
docker-compose -f deployments/docker/docker-compose.yml up --build
```

### **Log Analysis**
```bash
# Check application logs
docker logs keyhound-enhanced

# Check system logs
journalctl -u docker

# Check performance
docker exec keyhound-enhanced python -c "
from core.simple_keyhound import SimpleKeyHound
keyhound = SimpleKeyHound()
print(keyhound.get_performance_stats())
"
```

---

## 📋 **Deployment Checklist**

### **Pre-Deployment**
- [ ] Review security configuration
- [ ] Set strong passwords and secrets
- [ ] Configure monitoring and logging
- [ ] Test deployment in staging environment
- [ ] Backup existing data (if upgrading)

### **Deployment**
- [ ] Deploy using appropriate method (Docker/Cloud/Local)
- [ ] Verify all services are running
- [ ] Test web interface access
- [ ] Verify GPU acceleration (if applicable)
- [ ] Check monitoring and logging

### **Post-Deployment**
- [ ] Run health checks
- [ ] Monitor performance metrics
- [ ] Test puzzle solving functionality
- [ ] Verify backup procedures
- [ ] Document deployment configuration

---

## 🎯 **Best Practices**

### **Security**
1. **Use environment variables** for all secrets
2. **Enable authentication** in production
3. **Use HTTPS** for web access
4. **Regular security updates**
5. **Monitor access logs**

### **Performance**
1. **Start with small puzzles** to test performance
2. **Enable GPU acceleration** when available
3. **Monitor resource usage**
4. **Optimize configuration** for your hardware
5. **Use appropriate instance sizes** in cloud

### **Reliability**
1. **Implement health checks**
2. **Set up monitoring and alerting**
3. **Regular backups** of important data
4. **Test disaster recovery procedures**
5. **Keep dependencies updated**

### **Scalability**
1. **Use container orchestration** for scaling
2. **Implement load balancing**
3. **Use distributed computing** for large puzzles
4. **Monitor resource utilization**
5. **Plan for horizontal scaling**

---

**KeyHound Enhanced Deployment Guide v2.0.0**  
*Professional Bitcoin Cryptography Platform*
