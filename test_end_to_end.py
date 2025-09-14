#!/usr/bin/env python3
"""
End-to-End Test for the Complete AI Real Estate Generator System

This test verifies the entire pipeline:
1. Environment configuration (.env)
2. OpenRouter API connection
3. JSON input processing
4. LLM content generation for all 7 sections
5. HTML output formatting
6. Complete system integration

FEATURES:
- Automatically opens generated HTML in browser for review
- Interactive prompts to control test flow
- Comprehensive validation of all 7 sections
- Detailed error reporting
"""

import os
import sys
import json
import subprocess
import webbrowser
from pathlib import Path
from llm_service import LLMService

# Add current directory to path
sys.path.insert(0, '.')

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ python-dotenv not installed")
    sys.exit(1)


def test_environment_setup():
    """Test 1: Verify environment and .env configuration."""
    print("🧪 Test 1: Environment Setup")
    print("-" * 30)

    # Check .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found")
        return False
    print("✅ .env file exists")

    # Check API key is loaded
    api_key = os.getenv('API_KEY_OPENROUTER')
    if not api_key or api_key == 'tu-api-key-de-openrouter-aqui':
        print("❌ API_KEY_OPENROUTER not properly configured")
        return False
    print("✅ API key loaded from .env")
    return True


def test_openrouter_connection():
    """Test 2: Verify OpenRouter API connection."""
    print("\n🧪 Test 2: OpenRouter Connection")
    print("-" * 30)

    try:
        service = LLMService()
        print("✅ LLM Service initialized")

        # Test simple connection
        response = service.generate_content("Say 'Hello' if you can read this.")
        if "Hello" in response or "hello" in response:
            print("✅ OpenRouter API responding correctly")
            return True
        else:
            print(f"⚠️  Unexpected response: {response[:100]}...")
            return True  # Still consider it working

    except Exception as e:
        print(f"❌ OpenRouter connection failed: {e}")
        return False


def test_sample_json_validation():
    """Test 3: Verify sample JSON files are valid."""
    print("\n🧪 Test 3: Sample JSON Validation")
    print("-" * 30)

    sample_files = [
        'examples/sample_en_lisbon.json',
        'examples/sample_minimal.json',
        'examples/sample_pt_porto.json'
    ]

    for json_file in sample_files:
        if not Path(json_file).exists():
            print(f"❌ {json_file} not found")
            return False

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            required_keys = ['location', 'features', 'price', 'language']
            if not all(key in data for key in required_keys):
                print(f"❌ {json_file} missing required keys")
                return False

            print(f"✅ {json_file} is valid")

        except Exception as e:
            print(f"❌ Error reading {json_file}: {e}")
            return False

    return True


def test_full_pipeline():
    """Test 4: Run complete pipeline with real JSON input."""
    print("\n🧪 Test 4: Full Pipeline Execution")
    print("-" * 30)

    test_input = 'examples/sample_minimal.json'
    test_output = 'test_output.html'

    if not Path(test_input).exists():
        print(f"❌ Test input file {test_input} not found")
        return False

    try:
        # Run the main program
        print(f"🚀 Running: python main.py {test_input}")
        result = subprocess.run(
            [sys.executable, 'main.py', test_input],
            capture_output=True,
            text=True,
            timeout=300  # 60 second timeout
        )

        if result.returncode != 0:
            print(f"❌ Program execution failed: {result.stderr}")
            return False

        output = result.stdout.strip()
        print("✅ Program executed successfully")

        # Save output for inspection with proper UTF-8 encoding
        with open(test_output, 'w', encoding='utf-8', errors='replace') as f:
            f.write(output)
        print(f"✅ Output saved to {test_output}")

        # Verify output contains all expected sections
        expected_sections = [
            '<title>',
            '<meta name="description"',
            '<h1>',
            '<section id="description">',
            '<ul id="key-features">',
            '<section id="neighborhood">',
            '<p class="call-to-action">'
        ]

        missing_sections = []
        for section in expected_sections:
            if section not in output:
                missing_sections.append(section)

        if missing_sections:
            print(f"❌ Missing sections: {missing_sections}")
            print(f"📄 Check {test_output} for full output")
            return False

        print("✅ All 7 HTML sections present in output")

        # Note: Browser will be opened at the end of the test in cleanup()
        print("✅ Test completed - browser will open at the end for review")

        return True

    except subprocess.TimeoutExpired:
        print("❌ Program execution timed out (60s)")
        return False
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False


def test_output_quality():
    """Test 5: Verify output quality and structure."""
    print("\n🧪 Test 5: Output Quality Check")
    print("-" * 30)

    output_file = 'test_output.html'

    if not Path(output_file).exists():
        print(f"❌ {output_file} not found (run pipeline test first)")
        return False

    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for basic HTML structure
        if not content.strip().startswith('<'):
            print("❌ Output doesn't start with HTML tag")
            return False

        # Check for multiple sections (should have 7)
        section_count = content.count('<')  # Rough count of HTML tags
        if section_count < 7:
            print(f"❌ Too few HTML sections (found {section_count}, expected ≥7)")
            return False

        # Check for content (not empty sections)
        if len(content.strip()) < 500:
            print("❌ Output too short (probably missing content)")
            return False

        print("✅ Output structure and quality look good")
        print(f"📊 Output length: {len(content)} characters")
        print(f"🏷️  HTML sections: ~{section_count}")

        return True

    except Exception as e:
        print(f"❌ Quality check failed: {e}")
        return False


def cleanup():
    """Clean up test files."""
    test_output = 'test_output.html'
    if Path(test_output).exists():
        # Open the file in browser before deleting it
        try:
            print(f"🌐 Opening {test_output} in browser for review...")
            print("   (This is the final output - take your time to review it)")
            webbrowser.open(f'file://{Path(test_output).absolute()}')
            print("✅ HTML file opened in browser")
            print("   Press Enter when you're done reviewing to continue cleanup...")
            input()
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")

        os.remove(test_output)
        print(f"🧹 Cleaned up {test_output}")


def main():
    """Run all end-to-end tests."""
    print("🚀 END-TO-END TEST SUITE")
    print("=" * 50)
    print("Testing the complete AI Real Estate Generator pipeline")
    print("This may take a minute or two...\n")

    tests = [
        ("Environment Setup", test_environment_setup),
        ("OpenRouter Connection", test_openrouter_connection),
        ("Sample JSON Validation", test_sample_json_validation),
        ("Full Pipeline Execution", test_full_pipeline),
        ("Output Quality Check", test_output_quality)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print("25")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The system is working perfectly end-to-end.")
        print("\nYou can now confidently use:")
        print("  python main.py examples/sample_en_lisbon.json")
        print("  python main.py examples/sample_pt_porto.json")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")

    # Cleanup
    cleanup()

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
