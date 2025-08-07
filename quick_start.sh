#!/bin/bash

# T4P Competition Law Toolkit - Quick Start Script

echo "🚀 T4P Competition Law Toolkit - Quick Start"
echo "=============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Test the application
echo "🧪 Testing application..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup complete! Starting the application..."
    echo "📱 The application will open in your browser at http://localhost:8501"
    echo "🛑 Press Ctrl+C to stop the application"
    echo ""
    
    # Start the application
    streamlit run app.py --server.headless true --server.port 8501
else
    echo "❌ Setup failed. Please check the errors above."
    exit 1
fi
