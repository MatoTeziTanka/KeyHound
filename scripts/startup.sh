#!/bin/bash
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

# Install core dependencies
echo "Installing core dependencies..."
pip install flask>=2.3.0
pip install flask-socketio>=5.3.0
pip install werkzeug>=2.3.0
pip install psutil>=5.9.0
pip install tqdm>=4.65.0
pip install colorama>=0.4.6
pip install requests>=2.28.0
pip install cryptography>=3.4.8
pip install PyYAML>=6.0.0
pip install toml>=0.10.2

# Install optional dependencies (CPU-optimized versions)
echo "🔬 Installing optional dependencies..."
pip install scikit-learn>=1.3.0
pip install nltk>=3.8.0
pip install redis>=4.5.0

# Note: GPU dependencies will be skipped in standard codespace
echo "⚠️  GPU dependencies skipped (not available in standard codespace)"
echo "   For GPU access, use Google Cloud with your free credits"

# Install development tools
echo "🛠️ Installing development tools..."
pip install pytest>=7.0.0
pip install pytest-cov>=4.0.0
pip install black>=23.0.0
pip install flake8>=6.0.0
pip install mypy>=1.0.0

echo ""
echo "🧪 Running comprehensive test..."
python comprehensive_test.py

echo ""
echo "🎯 KeyHound Enhanced is ready!"
echo ""
echo "Available commands:"
echo "  python keyhound_enhanced.py --help"
echo "  python keyhound_enhanced.py --web"
echo "  python keyhound_enhanced.py --mobile"
echo "  python keyhound_enhanced.py --puzzle 1"
echo "  python keyhound_enhanced.py --show-results"
echo "  python keyhound_enhanced.py --verify-key PRIVATE_KEY"
echo ""
echo "Access URLs (after starting services):"
echo "  Web Interface: http://localhost:5000"
echo "  Mobile App:    http://localhost:5001/mobile"
echo "  PWA App:       http://localhost:5001/mobile/pwa"


