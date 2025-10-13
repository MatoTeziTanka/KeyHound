#!/usr/bin/env python3
"""
KeyHound Enhanced Setup Script

This script helps set up KeyHound Enhanced with the appropriate dependencies
based on your system and available resources.
"""

import os
import sys
import subprocess
import platform

def install_dependencies():
    """Install required dependencies."""
    print("Installing KeyHound Enhanced dependencies...")
    
    try:
        # Install core dependencies first
        core_deps = [
            "flask>=2.3.0",
            "flask-socketio>=5.3.0", 
            "werkzeug>=2.3.0",
            "psutil>=5.9.0",
            "tqdm>=4.65.0",
            "colorama>=0.4.6",
            "requests>=2.28.0",
            "cryptography>=3.4.8",
            "PyYAML>=6.0.0",
            "toml>=0.10.2"
        ]
        
        print("Installing core dependencies...")
        for dep in core_deps:
            print(f"  Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        
        print("\nCore dependencies installed successfully!")
        
        # Ask about optional dependencies
        print("\nOptional dependencies for enhanced features:")
        print("1. Machine Learning: tensorflow, scikit-learn, nltk")
        print("2. Distributed Computing: pyzmq, redis")
        print("3. GPU Acceleration: cupy, pyopencl, numba")
        
        install_optional = input("\nInstall optional dependencies? (y/n): ").lower().strip()
        
        if install_optional in ['y', 'yes']:
            optional_deps = [
                "tensorflow>=2.13.0",
                "scikit-learn>=1.3.0", 
                "nltk>=3.8.0",
                "pyzmq>=25.0.0",
                "redis>=4.5.0",
                "cupy-cuda12x>=12.0.0",  # Adjust based on CUDA version
                "pyopencl>=2023.1",
                "numba>=0.58.0"
            ]
            
            print("Installing optional dependencies...")
            for dep in optional_deps:
                try:
                    print(f"  Installing {dep}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                except subprocess.CalledProcessError:
                    print(f"  Warning: Failed to install {dep} - continuing...")
        
        print("\nSetup complete!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_config_file():
    """Create a basic configuration file."""
    config_content = """# KeyHound Enhanced Configuration
keyhound:
  version: "0.9.0"
  environment: "development"

# Web Interface Configuration
web:
  enabled: true
  host: "127.0.0.1"
  port: 5000
  auth_enabled: false
  debug: true

# Mobile App Configuration  
mobile:
  enabled: true
  app_name: "KeyHound Mobile"
  version: "1.0.0"
  pwa_enabled: true
  offline_support: true
  push_notifications: true
  theme: "dark"

# Machine Learning Configuration
ml:
  enabled: true
  models_dir: "./ml_models"

# Distributed Computing Configuration
distributed:
  enabled: false
  node_id: "keyhound_local"
  role: "worker"
  host: "127.0.0.1"
  port: 5555

# Performance Configuration
performance:
  memory_limit_mb: 2048
  max_threads: 4

# Storage Configuration
storage:
  results_dir: "./results"
  performance_db: "./performance_metrics.db"
  backup_enabled: true

# Security Configuration
security:
  encrypt_config: false
"""
    
    with open("keyhound_config.yaml", "w") as f:
        f.write(config_content)
    
    print("Configuration file created: keyhound_config.yaml")

def test_basic_functionality():
    """Test basic KeyHound functionality."""
    print("\nTesting basic functionality...")
    
    try:
        # Test basic imports
        from keyhound_enhanced import KeyHoundEnhanced
        print("✅ KeyHound Enhanced import successful")
        
        # Create instance
        keyhound = KeyHoundEnhanced(
            use_gpu=False,
            verbose=False,
            config_file="keyhound_config.yaml"
        )
        print("✅ KeyHound Enhanced initialization successful")
        
        # Test basic functionality
        test_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        if keyhound.bitcoin_crypto:
            address_info = keyhound.bitcoin_crypto.validate_address(test_address)
            print(f"✅ Bitcoin address validation: {address_info}")
        
        print("\n🎉 KeyHound Enhanced is ready to use!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("KeyHound Enhanced Setup")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        return
    
    # Create config file
    create_config_file()
    
    # Test functionality
    if test_basic_functionality():
        print("\n🚀 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python keyhound/main.py --help")
        print("2. Start web interface: python keyhound/main.py --web")
        print("3. Start mobile app: python keyhound/main.py --mobile")
        print("4. Solve a puzzle: python keyhound/main.py --puzzle 1")
    else:
        print("\n⚠️  Setup completed with warnings - check configuration")

if __name__ == "__main__":
    main()


