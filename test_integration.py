#!/usr/bin/env python3
"""
Integration test for DivineNode (Parakleon Engine)
Tests the complete ML pipeline and API functionality.
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path

def run_command(cmd, cwd=None, timeout=60):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, timeout=timeout, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def test_ml_pipeline():
    """Test the ML training and evaluation pipeline"""
    print("🧠 Testing ML Pipeline...")
    
    # Test training (1 epoch)
    print("  - Testing training...")
    success, stdout, stderr = run_command("python train.py --epochs 1 --batch_size 32", 
                                         cwd="src", timeout=120)
    if not success:
        print(f"  ❌ Training failed: {stderr}")
        return False
    print("  ✅ Training successful")
    
    # Test evaluation
    print("  - Testing evaluation...")
    success, stdout, stderr = run_command("python evaluate.py --checkpoint_path ../checkpoints/best.pth", 
                                         cwd="src", timeout=60)
    if not success:
        print(f"  ❌ Evaluation failed: {stderr}")
        return False
    print("  ✅ Evaluation successful")
    
    return True

def test_api_endpoints():
    """Test all API endpoints"""
    print("🌐 Testing API endpoints...")
    
    # Start server in background
    server_process = subprocess.Popen(["python", "-m", "uvicorn", "serve:app", "--host", "127.0.0.1", "--port", "8002"],
                                     cwd="src", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    time.sleep(5)
    
    base_url = "http://127.0.0.1:8002"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code != 200:
            print(f"  ❌ Health endpoint failed: {response.status_code}")
            return False
        health_data = response.json()
        if not health_data.get("ml_model_loaded"):
            print("  ❌ ML model not loaded")
            return False
        print("  ✅ Health endpoint working")
        
        # Test generate endpoint
        response = requests.post(f"{base_url}/generate", 
                               json={"prompt": "Hello"}, timeout=10)
        if response.status_code != 200:
            print(f"  ❌ Generate endpoint failed: {response.status_code}")
            return False
        print("  ✅ Generate endpoint working")
        
        # Test prediction endpoint with dummy image
        from PIL import Image
        import io
        import numpy as np
        
        # Create test image
        img = Image.fromarray(np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('test.png', img_bytes, 'image/png')}
        response = requests.post(f"{base_url}/predict", files=files, timeout=10)
        if response.status_code != 200:
            print(f"  ❌ Predict endpoint failed: {response.status_code}")
            return False
        prediction_data = response.json()
        if "prediction" not in prediction_data:
            print("  ❌ Prediction response missing prediction field")
            return False
        print("  ✅ Predict endpoint working")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API test failed: {e}")
        return False
    finally:
        # Kill server
        server_process.terminate()
        server_process.wait()

def test_build_script():
    """Test the build script"""
    print("🔨 Testing build script...")
    
    success, stdout, stderr = run_command("./scripts/build.sh", timeout=180)
    if not success:
        print(f"  ❌ Build script failed: {stderr}")
        return False
    print("  ✅ Build script successful")
    return True

def main():
    """Run all integration tests"""
    print("🚀 DivineNode Integration Test Suite")
    print("=" * 50)
    
    # Change to project root
    os.chdir(Path(__file__).parent)
    
    tests = [
        ("Build Script", test_build_script),
        ("ML Pipeline", test_ml_pipeline),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {name}")
        except Exception as e:
            print(f"❌ FAIL {name}: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("📋 Test Summary")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n🎯 {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DivineNode is ready for production.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()