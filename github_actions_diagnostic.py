#!/usr/bin/env python3
"""
GitHub Actions Diagnostic Script for AI/ML Projects
This script helps identify common issues in AI/ML GitHub Actions workflows
"""

import sys
import subprocess
import os
import platform
import psutil

def run_command(cmd):
    """Run a command and return its output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def check_system_info():
    """Check system information"""
    print("=== SYSTEM INFORMATION ===")
    print(f"Platform: {platform.platform()}")
    print(f"Python version: {sys.version}")
    print(f"Architecture: {platform.architecture()}")

    # Memory info
    if hasattr(psutil, 'virtual_memory'):
        memory = psutil.virtual_memory()
        print(f"Total memory: {memory.total / (1024**3):.2f} GB")
        print(f"Available memory: {memory.available / (1024**3):.2f} GB")
        print(f"Memory usage: {memory.percent}%")

    # Disk info
    if hasattr(psutil, 'disk_usage'):
        disk = psutil.disk_usage('/')
        print(f"Total disk space: {disk.total / (1024**3):.2f} GB")
        print(f"Free disk space: {disk.free / (1024**3):.2f} GB")
        print(f"Disk usage: {((disk.total - disk.free) / disk.total) * 100:.2f}%")

    print()

def check_python_packages():
    """Check Python package installations"""
    print("=== PYTHON PACKAGES ===")

    # Check pip version
    code, stdout, stderr = run_command("pip --version")
    if code == 0:
        print(f"Pip version: {stdout}")
    else:
        print(f"Pip check failed: {stderr}")

    # Common AI/ML packages to check
    packages_to_check = [
        'torch', 'tensorflow', 'transformers', 'numpy', 'pandas', 
        'scikit-learn', 'matplotlib', 'seaborn', 'jupyter', 
        'openai', 'huggingface-hub'
    ]

    print("\nInstalled AI/ML packages:")
    for package in packages_to_check:
        try:
            __import__(package)
            module = sys.modules[package]
            version = getattr(module, '__version__', 'unknown')
            print(f"âœ“ {package}: {version}")
        except ImportError:
            print(f"âœ— {package}: Not installed")

    print()

def check_environment_variables():
    """Check important environment variables"""
    print("=== ENVIRONMENT VARIABLES ===")

    important_vars = [
        'GITHUB_WORKSPACE', 'GITHUB_REPOSITORY', 'GITHUB_REF', 
        'GITHUB_SHA', 'GITHUB_TOKEN', 'RUNNER_OS', 'RUNNER_ARCH',
        'OPENAI_API_KEY', 'HUGGINGFACE_TOKEN', 'CUDA_VISIBLE_DEVICES',
        'PATH', 'PYTHONPATH'
    ]

    for var in important_vars:
        value = os.environ.get(var, 'Not set')
        if 'TOKEN' in var or 'KEY' in var:
            # Hide sensitive information
            if value != 'Not set':
                value = f"Set (length: {len(value)})"
        print(f"{var}: {value}")

    print()

def check_cuda_gpu():
    """Check CUDA and GPU availability"""
    print("=== CUDA/GPU CHECK ===")

    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("No CUDA GPUs available")
    except ImportError:
        print("PyTorch not installed - cannot check CUDA")

    # Check nvidia-smi
    code, stdout, stderr = run_command("nvidia-smi")
    if code == 0:
        print("nvidia-smi output:")
        print(stdout[:500] + "..." if len(stdout) > 500 else stdout)
    else:
        print("nvidia-smi not available or failed")

    print()

def check_git_info():
    """Check Git repository information"""
    print("=== GIT REPOSITORY INFO ===")

    commands = [
        ("Git version", "git --version"),
        ("Current branch", "git branch --show-current"),
        ("Latest commit", "git log -1 --oneline"),
        ("Repository status", "git status --porcelain"),
        ("Remote URL", "git remote get-url origin")
    ]

    for desc, cmd in commands:
        code, stdout, stderr = run_command(cmd)
        if code == 0:
            print(f"{desc}: {stdout}")
        else:
            print(f"{desc}: Failed - {stderr}")

    print()

def check_network_connectivity():
    """Check network connectivity to important services"""
    print("=== NETWORK CONNECTIVITY ===")

    urls_to_test = [
        "https://pypi.org",
        "https://github.com",
        "https://api.openai.com",
        "https://huggingface.co"
    ]

    for url in urls_to_test:
        code, stdout, stderr = run_command(f"curl -Is {url} | head -1")
        if code == 0:
            print(f"âœ“ {url}: {stdout}")
        else:
            print(f"âœ— {url}: Connection failed")

    print()

def main():
    """Main diagnostic function"""
    print("GitHub Actions Diagnostic Script for AI/ML Projects")
    print("=" * 50)
    print()

    try:
        check_system_info()
        check_python_packages()
        check_environment_variables()
        check_cuda_gpu()
        check_git_info()
        check_network_connectivity()

        print("=== DIAGNOSTIC COMPLETE ===")
        print("If you're still experiencing issues, please share this output")
        print("along with your workflow file and error messages.")

    except Exception as e:
        print(f"Diagnostic script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
