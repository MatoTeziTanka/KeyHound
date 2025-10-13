#!/usr/bin/env python3
"""
GitHub Codespace Setup Helper for KeyHound Enhanced
This script helps prepare the repository for GitHub Codespaces testing
"""

import os
import sys
import json
from pathlib import Path

def create_codespace_config():
    """Create GitHub Codespace configuration."""
    print("🚀 Setting up GitHub Codespace configuration...")
    
    # Ensure .devcontainer directory exists
    devcontainer_dir = Path(".devcontainer")
    devcontainer_dir.mkdir(exist_ok=True)
    
    # Create devcontainer.json if it doesn't exist
    devcontainer_json = devcontainer_dir / "devcontainer.json"
    if not devcontainer_json.exists():
        print("❌ devcontainer.json not found. Please ensure it was created.")
        return False
    
    # Create postCreateCommand.sh if it doesn't exist
    post_create_script = devcontainer_dir / "postCreateCommand.sh"
    if not post_create_script.exists():
        print("❌ postCreateCommand.sh not found. Please ensure it was created.")
        return False
    
    print("✅ Codespace configuration files found")
    return True

def create_test_scripts():
    """Create test scripts for codespace environment."""
    print("🧪 Creating test scripts...")
    
    # Create a simple test runner
    test_runner = """#!/usr/bin/env python3
import subprocess
import sys
import time

def run_codespace_test():
    print("🚀 Starting KeyHound Enhanced Codespace Test...")
    print("=" * 60)
    
    # Test 1: Check Python environment
    print("🐍 Testing Python environment...")
    print(f"Python version: {sys.version}")
    
    # Test 2: Check if we can import key modules
    print("\\n📦 Testing imports...")
    try:
        import flask
        print("✅ Flask available")
    except ImportError:
        print("❌ Flask missing - installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True)
    
    try:
        import numpy
        print("✅ NumPy available")
    except ImportError:
        print("❌ NumPy missing - installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "numpy"], check=True)
    
    # Test 3: Run comprehensive test if available
    print("\\n🧪 Running comprehensive test...")
    try:
        result = subprocess.run([sys.executable, "comprehensive_test.py"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Comprehensive test completed successfully")
            print(result.stdout[-500:])  # Show last 500 chars
        else:
            print("❌ Comprehensive test failed")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out after 5 minutes")
    except FileNotFoundError:
        print("⚠️  Comprehensive test script not found")
    
    print("\\n🎉 Codespace test completed!")
    print("\\nNext steps:")
    print("1. Start web interface: python keyhound/main.py --web")
    print("2. Start mobile app: python keyhound/main.py --mobile")
    print("3. Solve a puzzle: python keyhound/main.py --puzzle 1")

if __name__ == "__main__":
    run_codespace_test()
"""
    
    with open("codespace_test.py", "w") as f:
        f.write(test_runner)
    
    print("✅ Created codespace_test.py")
    
    # Create a startup script
    startup_script = """#!/bin/bash
echo "🚀 KeyHound Enhanced - Codespace Startup"
echo "========================================"

# Check if we're in a codespace
if [ -n "$CODESPACES" ]; then
    echo "✅ Running in GitHub Codespace"
    echo "Codespace name: $CODESPACE_NAME"
else
    echo "⚠️  Not running in codespace - local environment"
fi

echo ""
echo "🐍 Python environment:"
python --version
echo ""

echo "📦 Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🧪 Running quick test..."
python codespace_test.py

echo ""
echo "🎯 KeyHound Enhanced is ready!"
echo ""
echo "Available commands:"
echo "  python keyhound/main.py --help"
echo "  python keyhound/main.py --web"
echo "  python keyhound/main.py --mobile"
echo "  python keyhound/main.py --puzzle 1"
echo ""
echo "Access URLs (after starting services):"
echo "  Web Interface: http://localhost:5000"
echo "  Mobile App:    http://localhost:5001/mobile"
"""
    
    with open("startup.sh", "w") as f:
        f.write(startup_script)
    
    # Make executable
    os.chmod("startup.sh", 0o755)
    os.chmod("codespace_test.py", 0o755)
    
    print("✅ Created startup.sh")
    return True

def create_codespace_readme():
    """Create a codespace-specific README."""
    print("📖 Creating codespace README...")
    
    readme_content = """# 🚀 KeyHound Enhanced - GitHub Codespace

## Quick Start

This repository is configured for GitHub Codespaces testing.

### 🎯 Immediate Steps:

1. **Start the environment:**
   ```bash
   ./startup.sh
   ```

2. **Run quick test:**
   ```bash
   python codespace_test.py
   ```

3. **Start KeyHound Enhanced:**
   ```bash
   # Web interface
   python keyhound/main.py --web
   
   # Mobile app
   python keyhound/main.py --mobile
   
   # Solve a puzzle
   python keyhound/main.py --puzzle 1
   ```

### 📊 Access Points

- **Web Interface**: http://localhost:5000
- **Mobile App**: http://localhost:5001/mobile
- **PWA App**: http://localhost:5001/mobile/pwa

### 🧪 Testing

Run comprehensive tests:
```bash
python comprehensive_test.py
```

### 🔧 Configuration

The codespace is pre-configured with:
- Python 3.11
- All required dependencies
- Optimized settings for cloud environment
- Port forwarding for web services

### 🎉 Ready to Test!

Your KeyHound Enhanced environment is ready for comprehensive testing!
"""
    
    with open("CODESPACE_README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created CODESPACE_README.md")
    return True

def main():
    """Main setup function."""
    print("🚀 KeyHound Enhanced - GitHub Codespace Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("keyhound/main.py").exists():
        print("❌ Please run this script from the KeyHound directory")
        return False
    
    # Create configurations
    success = True
    success &= create_codespace_config()
    success &= create_test_scripts()
    success &= create_codespace_readme()
    
    if success:
        print("\n🎉 GitHub Codespace setup complete!")
        print("\nNext steps:")
        print("1. Commit and push changes to GitHub")
        print("2. Go to your repository on GitHub")
        print("3. Click 'Code' → 'Codespaces' → 'Create codespace'")
        print("4. Wait for the environment to build")
        print("5. Run: ./startup.sh")
        print("\n🚀 Ready for free testing in the cloud!")
    else:
        print("\n❌ Setup encountered issues. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()


