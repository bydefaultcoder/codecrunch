"""
Minimal installation script - installs only essential packages.
This gets the core system working without optional features.
"""

import subprocess
import sys

def install_package(package, description=""):
    """Install a package."""
    try:
        if description:
            print(f"📦 {description}...")
        else:
            print(f"📦 Installing {package}...")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"   ✅ Installed")
            return True
        else:
            print(f"   ⚠️  Warning: {result.stderr[:100]}")
            # Still return True if it's just a warning
            return "error" not in result.stderr.lower()[:200]
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout - package took too long")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return False

def main():
    """Install minimal essential packages."""
    print("=" * 60)
    print("🔬 AI Research Lab Simulator - Minimal Installation")
    print("=" * 60)
    print("\nInstalling only essential packages...\n")
    
    # Essential packages in order of importance
    packages = [
        ("PyYAML", "YAML parser (for config)"),
        ("pydantic-settings", "Settings management"),
        ("langchain-core==0.3.79", "LangChain core"),
        ("langchain-text-splitters==0.3.11", "Text splitting utilities"),
        ("langchain-anthropic/claude-3-haiku==0.2.0", "anthropic/claude-3-haiku/Claude support"),
        ("requests", "HTTP requests"),
        ("tenacity>=8.1.0,!=8.4.0", "Retry logic"),
    ]
    
    installed = 0
    failed = 0
    
    for package, desc in packages:
        if install_package(package, desc):
            installed += 1
        else:
            failed += 1
        print()  # Blank line
    
    print("=" * 60)
    print(f"✅ Installed: {installed}/{len(packages)}")
    if failed > 0:
        print(f"⚠️  Failed: {failed}/{len(packages)}")
    print("=" * 60)
    
    if installed >= len(packages) - 1:  # Allow 1 failure
        print("\n🎉 Minimal installation complete!")
        print("\nNext steps:")
        print("1. Test configuration: python test_api_keys.py")
        print("2. Run CLI: python -m src.main 'Your Research Topic'")
        print("\nNote: UI (streamlit) and vector store (chromadb) are optional")
    else:
        print("\n⚠️  Some packages failed. Check errors above.")
        print("You may need to install missing dependencies manually.")

if __name__ == "__main__":
    main()

