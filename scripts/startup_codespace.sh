#!/bin/bash

# KeyHound Enhanced - Codespace Startup Script
# This version is designed to work in GitHub Codespaces

echo "🚀 KeyHound Enhanced - Codespace Startup"
echo "========================================"

# Check if we're in a codespace
if [ -n "$CODESPACE_NAME" ]; then
    echo "✅ Running in GitHub Codespace: $CODESPACE_NAME"
else
    echo "⚠️  Not in a GitHub Codespace environment"
fi

# Check Python version
echo ""
echo "🐍 Python environment:"
python3 --version

# Install basic dependencies
echo ""
echo "📦 Installing basic dependencies..."
pip install --user requests colorama cryptography

# Test the codespace version
echo ""
echo "🧪 Testing KeyHound Enhanced (Codespace Version)..."
python3 keyhound_codespace.py --list-puzzles

echo ""
echo "🎯 KeyHound Enhanced is ready!"
echo ""
echo "Available commands:"
echo "  python3 keyhound_codespace.py --help"
echo "  python3 keyhound_codespace.py --list-puzzles"
echo "  python3 keyhound_codespace.py --puzzle 1"
echo "  python3 keyhound_codespace.py --brainwallet-test 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"
echo "  python3 keyhound_codespace.py --benchmark 30"
echo "  python3 keyhound_codespace.py --show-results"
echo ""
echo "🚀 Try running: python3 keyhound_codespace.py"


