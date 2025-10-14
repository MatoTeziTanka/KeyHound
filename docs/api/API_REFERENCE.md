# KeyHound Enhanced - Complete API Reference

## 📋 Table of Contents

- [🔑 Core APIs](#-core-apis)
- [⚡ Performance APIs](#-performance-apis)
- [🧠 Advanced APIs](#-advanced-apis)
- [🌐 Web APIs](#-web-apis)
- [📊 Monitoring APIs](#-monitoring-apis)
- [🔧 Configuration APIs](#-configuration-apis)
- [📝 Usage Examples](#-usage-examples)

---

## 🔑 Core APIs

### KeyHoundEnhanced

The main class that orchestrates all KeyHound functionality.

```python
from core.keyhound_enhanced import KeyHoundEnhanced

# Initialize with basic settings
keyhound = KeyHoundEnhanced(
    use_gpu=False,           # Enable GPU acceleration
    use_distributed=False,   # Enable distributed computing
    config_file=None,        # Path to config file
    verbose=True            # Enable verbose logging
)
```

**Key Methods:**

```python
# Puzzle solving
keyhound.solve_puzzle(bits=40, target_address=None, start_key=None)

# Brainwallet testing
keyhound.test_brainwallet_security(
    patterns=None,           # Custom patterns
    max_attempts=1000000,    # Maximum attempts
    timeout=3600            # Timeout in seconds
)

# Enable advanced features
keyhound.enable_gpu_acceleration(framework='cuda')
keyhound.enable_distributed_computing(nodes=4)
```

**Available Features Check:**
```python
# Check what features are available
features = keyhound._available_features
print(f"GPU Available: {features['gpu']}")
print(f"Web Available: {features['web']}")
print(f"ML Available: {features['ml']}")
print(f"Distributed Available: {features['distributed']}")
```

---

### BitcoinCryptography

Core Bitcoin cryptography operations.

```python
from core.bitcoin_cryptography import BitcoinCryptography

crypto = BitcoinCryptography()
```

**Key Methods:**

```python
# Key generation and validation
private_key = crypto.generate_private_key()
public_key = crypto.private_key_to_public_key(private_key)
address = crypto.public_key_to_address(public_key)

# Validation
is_valid = crypto.is_valid_private_key(private_key)
is_valid = crypto.is_valid_address(address)

# Address formats
legacy_address = crypto.generate_address(private_key, format='legacy')
p2sh_address = crypto.generate_address(private_key, format='p2sh')
bech32_address = crypto.generate_address(private_key, format='bech32')

# Message signing and verification
signature = crypto.sign_message(private_key, message)
is_valid = crypto.verify_message(address, message, signature)
```

**Address Generation Options:**
```python
# Different address formats
formats = ['legacy', 'p2sh', 'bech32']

# For each format
for fmt in formats:
    address = crypto.generate_address(private_key, format=fmt)
    print(f"{fmt}: {address}")
```

---

### BrainwalletPatternLibrary

Advanced brainwallet pattern recognition and testing.

```python
from core.brainwallet_patterns import BrainwalletPatternLibrary

pattern_lib = BrainwalletPatternLibrary()
```

**Key Methods:**

```python
# Pattern matching
patterns = pattern_lib.find_patterns(text="password123")
matches = pattern_lib.match_patterns(text="MySecretKey")

# Pattern generation
custom_patterns = pattern_lib.generate_patterns(
    base_text="hello",
    variations=['uppercase', 'numbers', 'symbols']
)

# Security testing
security_score = pattern_lib.assess_security(text="MyPassword123!")
weaknesses = pattern_lib.find_weaknesses(text="password")
```

**Pattern Categories:**
```python
# Available pattern categories
categories = pattern_lib.get_categories()
# Returns: ['common', 'dictionary', 'patterns', 'personal']

# Get patterns by category
common_patterns = pattern_lib.get_patterns_by_category('common')
```

---

## ⚡ Performance APIs

### GPUAccelerationManager

GPU acceleration for high-performance computing.

```python
from gpu.gpu_acceleration import GPUAccelerationManager, GPUConfig

# Check GPU availability first
if GPU_AVAILABLE:
    gpu_config = GPUConfig(
        framework='cuda',        # 'cuda', 'opencl', 'numba'
        device_id=0,            # GPU device ID
        memory_limit=8192,      # Memory limit in MB
        verbose=True
    )
    
    gpu_manager = GPUAccelerationManager(gpu_config)
    
    if gpu_manager.is_gpu_available():
        print(f"GPU: {gpu_manager.get_device_info()}")
        
        # Parallel key generation
        keys = gpu_manager.generate_keys_parallel(count=10000)
        
        # Parallel address generation
        addresses = gpu_manager.generate_addresses_parallel(keys)
        
        # Performance metrics
        metrics = gpu_manager.get_performance_metrics()
        print(f"Keys/sec: {metrics['keys_per_second']}")
```

**GPU Frameworks Supported:**
- **CUDA**: NVIDIA GPUs with CUDA support
- **OpenCL**: Cross-platform GPU computing
- **Numba**: JIT compilation for GPU

---

### MemoryOptimizer

Intelligent memory management for large-scale operations.

```python
from core.memory_optimization import MemoryOptimizer, get_memory_optimizer

optimizer = get_memory_optimizer()

# Memory monitoring
stats = optimizer.get_memory_stats()
print(f"Memory Usage: {stats['percent']}%")
print(f"Available: {stats['available']} MB")

# Memory optimization
optimizer.optimize_memory()
optimizer.clear_cache()

# Batch processing
batch_processor = optimizer.create_batch_processor(
    batch_size=10000,
    max_memory_mb=2048
)

# Process large datasets
for batch in batch_processor.process_large_dataset(data):
    process_batch(batch)
```

**Memory Optimization Features:**
```python
# Streaming key processor for large ranges
stream_processor = optimizer.create_streaming_processor(
    start_key=0,
    end_key=2**40,
    batch_size=1000000
)

for batch in stream_processor:
    # Process each batch
    results = process_key_batch(batch)
    yield results
```

---

## 🧠 Advanced APIs

### MachineLearningManager

AI-powered pattern recognition and optimization.

```python
from ml.machine_learning import MachineLearningManager, create_ml_manager

if ML_AVAILABLE:
    ml_manager = create_ml_manager()
    
    # Pattern recognition
    patterns = ml_manager.recognize_patterns(data)
    
    # Performance optimization
    optimized_params = ml_manager.optimize_parameters(
        current_params,
        performance_data
    )
    
    # Predictive analysis
    predictions = ml_manager.predict_performance(
        puzzle_bits=50,
        hardware_specs=system_info
    )
```

**ML Models Available:**
```python
# Available model types
models = ml_manager.get_available_models()
# Returns: ['pattern_recognition', 'performance_optimization', 'predictive_analysis']

# Load specific model
model = ml_manager.load_model('pattern_recognition')
```

---

### DistributedComputingManager

Multi-node distributed computing coordination.

```python
from distributed.distributed_computing import DistributedComputingManager, create_distributed_manager

if DISTRIBUTED_AVAILABLE:
    distributed_manager = create_distributed_manager(
        node_role='coordinator',    # 'coordinator', 'worker'
        network_config={
            'host': 'localhost',
            'port': 8080,
            'protocol': 'tcp'
        }
    )
    
    # Coordinate distributed puzzle solving
    if distributed_manager.is_coordinator():
        # Distribute work to workers
        work_units = distributed_manager.distribute_work(
            puzzle_bits=50,
            total_range=2**50,
            worker_count=4
        )
        
        # Collect results
        results = distributed_manager.collect_results()
        
    else:
        # Worker node - process assigned work
        work_unit = distributed_manager.get_work_unit()
        results = process_work_unit(work_unit)
        distributed_manager.submit_results(results)
```

**Network Configuration:**
```python
# Network setup
network_config = NetworkConfig(
    protocol='tcp',          # 'tcp', 'udp', 'websocket'
    compression=True,        # Enable compression
    encryption=True,         # Enable encryption
    heartbeat_interval=30    # Heartbeat in seconds
)
```

---

## 🌐 Web APIs

### KeyHoundWebInterface

Web-based dashboard and API server.

```python
from web.web_interface import KeyHoundWebInterface, create_web_interface

if WEB_AVAILABLE:
    web_interface = create_web_interface(
        host='localhost',
        port=5000,
        debug=False
    )
    
    # Start web server
    web_interface.start()
    
    # API endpoints available:
    # GET  /api/status          - System status
    # GET  /api/puzzles         - Available puzzles
    # POST /api/solve           - Start puzzle solving
    # GET  /api/results         - Get results
    # GET  /api/performance     - Performance metrics
```

**Web API Endpoints:**

```python
# RESTful API endpoints
endpoints = {
    'GET /api/status': 'System status and health',
    'GET /api/puzzles': 'List available Bitcoin puzzles',
    'POST /api/solve': 'Start puzzle solving',
    'GET /api/results': 'Get solving results',
    'GET /api/performance': 'Performance metrics',
    'GET /api/config': 'Configuration settings',
    'POST /api/config': 'Update configuration',
    'GET /api/logs': 'System logs',
    'GET /ws/status': 'WebSocket for real-time updates'
}

# Example API usage
import requests

# Check system status
response = requests.get('http://localhost:5000/api/status')
status = response.json()

# Start puzzle solving
solve_request = {
    'puzzle_bits': 40,
    'use_gpu': True,
    'timeout': 3600
}
response = requests.post('http://localhost:5000/api/solve', json=solve_request)
```

---

### KeyHoundMobileApp

Progressive Web App for mobile devices.

```python
from web.mobile_app import KeyHoundMobileApp, create_mobile_app

if WEB_AVAILABLE:
    mobile_app = create_mobile_app(
        enable_pwa=True,         # Enable Progressive Web App
        enable_notifications=True, # Enable push notifications
        offline_mode=True        # Enable offline functionality
    )
    
    # Mobile-specific features
    mobile_app.enable_touch_gestures()
    mobile_app.enable_offline_caching()
    mobile_app.register_service_worker()
```

---

## 📊 Monitoring APIs

### PerformanceMonitor

Real-time performance monitoring and alerting.

```python
from core.performance_monitoring import PerformanceMonitor, get_performance_monitor

monitor = get_performance_monitor()

# Start monitoring
monitor.start_monitoring()

# Custom metrics
monitor.start_timer('puzzle_solve')
# ... do work ...
monitor.stop_timer('puzzle_solve')

# Performance metrics
metrics = monitor.get_metrics()
print(f"CPU Usage: {metrics['cpu_percent']}%")
print(f"Memory Usage: {metrics['memory_percent']}%")
print(f"Keys/sec: {metrics['keys_per_second']}")

# Set alerts
monitor.set_alert_threshold('cpu_percent', 90, 'critical')
monitor.set_alert_threshold('memory_percent', 85, 'warning')

# Get alerts
alerts = monitor.get_active_alerts()
```

**Available Metrics:**
```python
# System metrics
system_metrics = monitor.get_system_metrics()
# Returns: cpu_percent, memory_percent, disk_usage, network_io

# Application metrics
app_metrics = monitor.get_application_metrics()
# Returns: keys_per_second, puzzles_solved, errors_count, uptime

# Custom metrics
monitor.record_metric('custom_metric', value=123.45)
```

---

### ResultPersistenceManager

Persistent storage and backup of results.

```python
from core.result_persistence import ResultPersistenceManager, get_result_persistence_manager

persistence_manager = get_result_persistence_manager()

# Store results
result = {
    'private_key': 'abc123...',
    'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
    'puzzle_bits': 40,
    'timestamp': '2025-01-01T00:00:00Z',
    'metadata': {'solver': 'gpu', 'time_taken': 3600}
}

persistence_manager.store_result(result)

# Retrieve results
results = persistence_manager.get_results(
    puzzle_bits=40,
    date_range=('2025-01-01', '2025-01-31'),
    limit=100
)

# Backup and restore
backup_file = persistence_manager.create_backup()
persistence_manager.restore_from_backup(backup_file)
```

**Storage Backends:**
```python
# File system storage (default)
file_storage = persistence_manager.get_storage_backend('file_system')

# Database storage (if configured)
db_storage = persistence_manager.get_storage_backend('database')

# Cloud storage (if configured)
cloud_storage = persistence_manager.get_storage_backend('cloud')
```

---

## 🔧 Configuration APIs

### ConfigurationManager

Centralized configuration management.

```python
from core.configuration_manager import ConfigurationManager, get_config_manager

config_manager = get_config_manager()

# Get configuration
config = config_manager.get_config()
print(f"Puzzle solving config: {config['puzzle_solving']}")

# Update configuration
config_manager.update_config({
    'puzzle_solving': {
        'max_bits': 66,
        'batch_size': 10000
    }
})

# Validate configuration
is_valid = config_manager.validate_config(config)

# Get default configuration
default_config = config_manager.get_default_config()
```

**Configuration Schema:**
```python
# Configuration structure
config_schema = {
    'puzzle_solving': {
        'max_bits': 66,           # Maximum puzzle bits
        'batch_size': 10000,      # Batch size for processing
        'timeout': 3600,          # Timeout in seconds
        'enable_progress': True   # Enable progress reporting
    },
    'performance': {
        'enable_gpu': False,      # Enable GPU acceleration
        'enable_distributed': False, # Enable distributed computing
        'log_level': 'INFO',      # Logging level
        'memory_limit': 4096      # Memory limit in MB
    },
    'storage': {
        'backend': 'file_system', # Storage backend
        'path': './data',         # Storage path
        'backup_enabled': True    # Enable backups
    }
}
```

---

## 📝 Usage Examples

### Basic Puzzle Solving

```python
from core.keyhound_enhanced import KeyHoundEnhanced

# Initialize KeyHound
keyhound = KeyHoundEnhanced(use_gpu=True, verbose=True)

# Solve a 40-bit puzzle
try:
    result = keyhound.solve_puzzle(bits=40, timeout=3600)
    if result:
        print(f"Found key: {result['private_key']}")
        print(f"Address: {result['address']}")
    else:
        print("Puzzle not solved within timeout")
except Exception as e:
    print(f"Error: {e}")
```

### Advanced Brainwallet Testing

```python
# Test brainwallet security
patterns = [
    "password123",
    "MySecretKey",
    "BitcoinWallet"
]

for pattern in patterns:
    print(f"Testing pattern: {pattern}")
    security_score = keyhound.pattern_library.assess_security(pattern)
    print(f"Security score: {security_score}/100")
    
    if security_score < 50:
        print("WARNING: Weak pattern detected!")
```

### GPU-Accelerated Solving

```python
# Enable GPU acceleration
if keyhound._available_features['gpu']:
    keyhound.enable_gpu_acceleration(framework='cuda')
    
    # Solve with GPU
    result = keyhound.solve_puzzle(
        bits=50,
        use_gpu=True,
        batch_size=100000
    )
    
    # Get GPU performance metrics
    if keyhound.gpu_manager:
        metrics = keyhound.gpu_manager.get_performance_metrics()
        print(f"GPU Performance: {metrics['keys_per_second']} keys/sec")
```

### Web Interface Setup

```python
# Start web interface
if keyhound._available_features['web']:
    web_interface = keyhound.create_web_interface(
        host='0.0.0.0',
        port=5000,
        enable_api=True,
        enable_websocket=True
    )
    
    # Start server
    web_interface.start()
    print("Web interface available at: http://localhost:5000")
```

### Distributed Computing

```python
# Set up distributed computing
if keyhound._available_features['distributed']:
    keyhound.enable_distributed_computing(
        node_role='coordinator',
        worker_nodes=['node1', 'node2', 'node3'],
        network_config={
            'host': 'localhost',
            'port': 8080
        }
    )
    
    # Solve puzzle using distributed computing
    result = keyhound.solve_puzzle(
        bits=60,
        use_distributed=True,
        worker_count=4
    )
```

---

## 🚀 Performance Optimization

### Best Practices

1. **GPU Acceleration**: Use GPU for puzzles > 45 bits
2. **Batch Processing**: Use appropriate batch sizes (10K-100K)
3. **Memory Management**: Monitor memory usage for large puzzles
4. **Distributed Computing**: Use for puzzles > 55 bits
5. **Configuration**: Optimize based on hardware specs

### Performance Tuning

```python
# Optimize for your hardware
config = {
    'puzzle_solving': {
        'batch_size': 50000,  # Adjust based on GPU memory
        'max_bits': 66       # Set based on hardware capability
    },
    'performance': {
        'enable_gpu': True,   # Enable if GPU available
        'memory_limit': 8192  # Set based on available RAM
    }
}

keyhound.config_manager.update_config(config)
```

---

## 🔒 Security Considerations

1. **Private Keys**: Never log or expose private keys
2. **Network Security**: Use encryption for distributed computing
3. **Access Control**: Implement authentication for web interface
4. **Data Backup**: Regular backups of important results
5. **Audit Logging**: Monitor all operations for security

---

This comprehensive API reference covers all available functionality in KeyHound Enhanced. Each API is designed to be modular and can be used independently or in combination for maximum flexibility and performance.
