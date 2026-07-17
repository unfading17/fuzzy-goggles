#!/usr/bin/env python3
"""
Install dependencies for PermitAI
"""

import subprocess
import sys

def install_dependencies():
    """Install all required dependencies."""
    print("Installing PermitAI dependencies...")
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)
