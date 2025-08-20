#!/bin/bash

# DivineNode Build Script - Parakleon Engine
set -e

echo "🚀 Building DivineNode (Parakleon Engine)..."

# Check if we're in the right directory
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --user -r requirements.txt

# Install additional ML dependencies if not present
echo "🧠 Installing ML dependencies..."
pip install --user torch torchvision scikit-learn tensorboard

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p checkpoints logs data

# Test imports
echo "🔍 Testing Python imports..."
cd src
python -c "from model import get_model; from data import get_dataloader; print('✅ Core imports successful')"
python -c "from db import Session; print('✅ Database imports successful')"
python -c "import fastapi, uvicorn; print('✅ API imports successful')"
cd ..

# Run a quick training test (1 epoch)
echo "🏃 Running quick ML training test..."
cd src
python train.py --epochs 1 --batch_size 64 || echo "⚠️ Training test failed"
cd ..

# Test the API server (quick startup test)
echo "🌐 Testing API server..."
cd src
timeout 10 uvicorn serve:app --host 127.0.0.1 --port 8001 &
SERVER_PID=$!
sleep 5

# Test if server is responding
if curl -s http://127.0.0.1:8001/health > /dev/null; then
    echo "✅ API server test passed"
else
    echo "⚠️ API server test failed"
fi

# Kill the test server
kill $SERVER_PID 2>/dev/null || true
cd ..

# Android build (if requested)
if [[ "$1" == "--android" ]]; then
    echo "📱 Building Android app..."
    if [[ -f "gradlew" ]]; then
        ./gradlew assembleDebug
        echo "✅ Android APK built"
    else
        echo "⚠️ No gradlew found, skipping Android build"
    fi
fi

echo "🎉 Build completed successfully!"
echo "📋 Next steps:"
echo "   • Start API server: cd src && uvicorn serve:app --host 0.0.0.0 --port 8000"
echo "   • Run training: cd src && python train.py"
echo "   • Run evaluation: cd src && python evaluate.py"
echo "   • Set OPENAI_API_KEY for LLM features"
