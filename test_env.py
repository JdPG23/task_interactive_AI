#!/usr/bin/env python3
"""
Test script to verify .env file loading
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except ImportError:
    print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

def test_env_loading():
    """Test if environment variables are loaded from .env file."""
    print("🔍 Testing .env file loading...")

    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Create it with: cp env_example.txt .env")
        print("Then edit it with your OpenRouter API key")
        return False

    # Check API key
    api_key = os.getenv('API_KEY_OPENROUTER')
    if not api_key:
        print("❌ API_KEY_OPENROUTER not found in .env file")
        print("Please add your OpenRouter API key to the .env file")
        return False

    if api_key == 'tu-api-key-de-openrouter-aqui':
        print("❌ API_KEY_OPENROUTER still has placeholder value")
        print("Please replace with your actual OpenRouter API key")
        return False

    print(f"✅ API_KEY_OPENROUTER loaded successfully (length: {len(api_key)})")
    return True

def main():
    """Run environment tests."""
    print("🚀 Testing Environment Configuration")
    print("=" * 40)

    if test_env_loading():
        print("\n🎉 Environment configuration is correct!")
        print("You can now run:")
        print("  python test_openrouter.py")
        print("  python main.py examples/sample_en_lisbon.json")
        return True
    else:
        print("\n❌ Environment configuration needs fixing.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
