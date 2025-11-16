#!/bin/bash

# PersonaGenerator Installation Script

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 PersonaGenerator - Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python 3: $(python3 --version)"

# Check Chrome
if ! command -v google-chrome &> /dev/null && ! [ -d "/Applications/Google Chrome.app" ]; then
    echo "⚠️  Google Chrome not found. Please install Chrome browser."
    echo "   Download from: https://www.google.com/chrome/"
fi

# Check ChromeDriver
if ! command -v chromedriver &> /dev/null; then
    echo "⚠️  ChromeDriver not found."
    echo "   Installing with Homebrew..."
    if command -v brew &> /dev/null; then
        brew install chromedriver
    else
        echo "❌ Homebrew not found. Install chromedriver manually:"
        echo "   https://chromedriver.chromium.org/"
        exit 1
    fi
fi
echo "✅ ChromeDriver: $(chromedriver --version | head -1)"

# Check UnifiedLLMClient
UNIFIED_CLIENT_PATH="$HOME/Development/Scripts/UnifiedLLMClient"
if [ ! -d "$UNIFIED_CLIENT_PATH" ]; then
    echo "❌ UnifiedLLMClient not found at: $UNIFIED_CLIENT_PATH"
    echo "   Please ensure UnifiedLLMClient is installed"
    exit 1
fi
echo "✅ UnifiedLLMClient found"

echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "📁 Creating directories..."
mkdir -p output

echo ""
echo "🔧 Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file (add your API keys)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Making scripts executable..."
chmod +x persona_generator.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Installation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next steps:"
echo "1. Edit sample_urls.txt with LinkedIn profile URLs"
echo "2. (Optional) Add API keys to .env for premium AI models"
echo "3. Run: python3 persona_generator.py --urls sample_urls.txt"
echo ""
echo "💡 For free usage, Qwen model requires no API key!"
echo ""
