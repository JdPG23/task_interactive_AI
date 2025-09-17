#!/usr/bin/env python3
"""
Test script for OpenRouter + DeepSeek V3 integration
"""

import os
import sys
from llm_service import LLMService

# Add current directory to path
sys.path.insert(0, '.')


def test_openrouter_connection():
    """Test OpenRouter API connection with DeepSeek Chat."""
    print("🧪 Testing OpenRouter + DeepSeek Chat connection...")

    # Check if API key is set
    api_key = os.getenv('API_KEY_OPENROUTER')
    if not api_key:
        print("❌ API_KEY_OPENROUTER environment variable not found")
        print("Please set it with: export API_KEY_OPENROUTER='your-key'")
        return False

    print(f"✅ API key found (length: {len(api_key)})")

    try:
        # Initialize service
        service = LLMService()
        print("✅ LLM Service initialized successfully")

        # Test simple prompt
        test_prompt = "Hello! Can you respond with just 'OpenRouter connection successful'?"
        print(f"📤 Sending test prompt: {test_prompt}")

        response = service.generate_content(test_prompt)
        print(f"📥 Response: {response}")

        # Check if response contains expected text
        if "successful" in response.lower():
            print("✅ Connection test PASSED")
            return True
        else:
            print("⚠️  Unexpected response, but connection seems to work")
            return True

    except Exception as e:
        print(f"❌ Connection test FAILED: {e}")
        return False


def test_real_estate_prompt():
    """Test with a real estate related prompt."""
    print("\n🧪 Testing real estate content generation...")

    try:
        service = LLMService()

        # Real estate prompt similar to what the system uses
        prompt = """
        Generate a concise SEO-optimized title for a real estate listing.
        Property details:
        - Type: 3-bedroom apartment
        - Location: Lisbon, Portugal
        - Price: €450,000

        Generate only the title, no additional explanations.
        """

        print("📤 Sending real estate prompt...")
        response = service.generate_content(prompt)
        print(f"📥 Generated title: {response}")

        print("✅ Real estate content generation test PASSED")
        return True

    except Exception as e:
        print(f"❌ Real estate test FAILED: {e}")
        return False

def main():
    """Run OpenRouter tests."""
    print("🚀 Testing OpenRouter + DeepSeek Chat Integration")
    print("=" * 50)

    success1 = test_openrouter_connection()
    success2 = test_real_estate_prompt() if success1 else False

    if success1 and success2:
        print("\n🎉 All tests PASSED! OpenRouter + DeepSeek Chat is working correctly.")
        print("\nYou can now run the main program:")
        print("python main.py examples/sample_en_lisbon.json")
        return True
    else:
        print("\n❌ Some tests FAILED. Check your API key and internet connection.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
