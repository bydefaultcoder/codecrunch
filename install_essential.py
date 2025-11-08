"""
Quick installation script for essential packages only.
Run this to install the minimum required packages.
"""

import subprocess
import sys

def install_package(package):
    """Install a package and return success status."""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        print(f"✅ {package} installed")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    """Install essential packages."""
    print("🔧 Installing essential packages for AI Research Lab Simulator\n")
    
    essential_packages = [
        "PyYAML",
        "pydantic-settings",
        "langchain-core==0.3.79",
        "langchain-text-splitters==0.3.11",
        "langchain-anthropic/claude-3-haiku==0.2.0",
        "requests",
        "SQLAlchemy",
        "aiohttp",
        "tenacity",
        "dataclasses-json",
    ]
    
    success_count = 0
    for package in essential_packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n✅ Installed {success_count}/{len(essential_packages)} packages")
    
    if success_count == len(essential_packages):
        print("\n🎉 All essential packages installed!")
        print("You can now test with: python test_api_keys.py")
    else:
        print("\n⚠️  Some packages failed to install. Check errors above.")

if __name__ == "__main__":
    main()

