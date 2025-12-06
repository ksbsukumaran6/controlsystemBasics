"""
Control Systems Learning Environment Setup
==========================================

This script helps set up the Python environment for learning control systems.
Run this after installing Python to install all necessary packages.

Usage: python setup_environment.py
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    print("Control Systems Learning Environment Setup")
    print("=" * 50)
    
    # Check if Python is available
    print(f"Python version: {sys.version}")
    
    # Essential packages for control systems
    packages = [
        "numpy",           # Numerical computing
        "scipy",           # Scientific computing (includes signal processing)
        "matplotlib",      # Plotting and visualization
        "control",         # Python Control Systems Library
        "sympy",           # Symbolic mathematics
        "jupyter",         # Jupyter notebooks
        "pandas",          # Data manipulation
        "seaborn",         # Statistical plotting
        "ipympl",          # Interactive matplotlib in Jupyter
    ]
    
    print("\nInstalling packages...")
    print("-" * 30)
    
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    if failed_packages:
        print(f"⚠️  Some packages failed to install: {', '.join(failed_packages)}")
        print("You may need to install them manually later.")
    else:
        print("🎉 All packages installed successfully!")
    
    print("\nNext steps:")
    print("1. Create a virtual environment (recommended)")
    print("2. Start learning with Jupyter notebooks")
    print("3. Begin with basic control theory concepts")

if __name__ == "__main__":
    main()