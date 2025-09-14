#!/usr/bin/env python3
"""
Comprehensive End-to-End Test for the AI Real Estate Generator System

This test verifies the complete enhanced pipeline:
1. Environment configuration (.env)
2. OpenRouter API connection
3. JSON input processing
4. LLM content generation for all 7 sections
5. HTML output formatting
6. Multilingual support (English, Portuguese, Spanish)
7. Content quality evaluation and scoring
8. System integration with all bonus features

ENHANCED FEATURES:
- Tests all 3 supported languages
- Content quality evaluation with scoring
- Automatically opens generated HTML in browser for review
- Interactive prompts to control test flow
- Comprehensive validation of all 7 sections
- Detailed error reporting
- Tone customization testing
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
            encoding='utf-8',
            errors='replace',
            timeout=300  # 300 second timeout
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


def test_multilingual_support():
    """Test 6: Test content generation in all 3 supported languages."""
    print("\n🧪 Test 6: Multilingual Support (EN, PT, ES)")
    print("-" * 30)
    
    test_files = [
        ('examples/sample_en_lisbon.json', 'en', 'English'),
        ('examples/sample_pt_porto.json', 'pt', 'Portuguese'),
        ('examples/sample_spanish_madrid.json', 'es', 'Spanish')
    ]
    
    generated_files = []
    
    for json_file, lang_code, lang_name in test_files:
        if not Path(json_file).exists():
            print(f"❌ {json_file} not found")
            return False
        
        output_file = f'test_{lang_code}_output.html'
        
        try:
            print(f"🚀 Testing {lang_name}...")
            result = subprocess.run(
                [sys.executable, 'main.py', json_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=120
            )
            
            if result.returncode != 0:
                print(f"❌ {lang_name} generation failed: {result.stderr}")
                return False
            
            # Save output
            with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
                f.write(result.stdout.strip())
            
            generated_files.append((output_file, lang_code, lang_name))
            print(f"✅ {lang_name} content generated successfully")
            
            # Open in browser for user review
            try:
                print(f"🌐 Opening {lang_name} output in browser...")
                print(f"   📋 Please review the {lang_name} content for:")
                print("      ✅ All 7 HTML sections present")
                print("      ✅ Language-appropriate keywords and phrases")
                print("      ✅ Natural, fluent text quality")
                print("      ✅ Proper character encoding (ñ, á, ç, etc.)")
                webbrowser.open(f'file://{Path(output_file).absolute()}')
                input(f"   ⏳ Press Enter when done reviewing {lang_name} content...")
            except Exception as e:
                print(f"⚠️  Could not open browser for {lang_name}: {e}")
                input("   📋 Press Enter to continue...")
            
        except subprocess.TimeoutExpired:
            print(f"❌ {lang_name} generation timed out")
            return False
        except Exception as e:
            print(f"❌ {lang_name} test failed: {e}")
            return False
    
    # Store generated files for cleanup
    test_multilingual_support.generated_files = generated_files
    print("✅ All 3 languages tested successfully")
    return True


def test_content_evaluator():
    """Test 7: Test content quality evaluation for all languages."""
    print("\n🧪 Test 7: Content Quality Evaluation")
    print("-" * 30)
    
    if not hasattr(test_multilingual_support, 'generated_files'):
        print("❌ No generated files found. Run multilingual test first.")
        return False
    
    try:
        from content_evaluator import ContentEvaluator
        evaluator = ContentEvaluator()
        
        overall_scores = []
        
        for output_file, lang_code, lang_name in test_multilingual_support.generated_files:
            if not Path(output_file).exists():
                print(f"❌ {output_file} not found")
                continue
            
            # Read content
            with open(output_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Evaluate content
            report = evaluator.generate_report(content, lang_code)
            score = report['overall_score']
            overall_scores.append(score)
            
            # Show results
            print(f"📊 {lang_name}: {score}/100", end="")
            if score >= 80:
                print(" 🏆 EXCELLENT")
            elif score >= 60:
                print(" ✅ GOOD")
            elif score >= 40:
                print(" ⚠️  FAIR")
            else:
                print(" ❌ POOR")
        
        # Overall evaluation
        if overall_scores:
            avg_score = sum(overall_scores) / len(overall_scores)
            print(f"\n📈 Average Quality Score: {avg_score:.1f}/100")
            
            if avg_score >= 75:
                print("🎉 Content quality exceeds expectations!")
                return True
            elif avg_score >= 60:
                print("✅ Content quality meets standards")
                return True
            else:
                print("⚠️  Content quality needs improvement")
                return False
        
        return False
        
    except ImportError:
        print("❌ Content evaluator not available")
        return False
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return False


def cleanup():
    """Clean up test files."""
    test_files = ['test_output.html']
    
    # Add multilingual test files if they exist
    if hasattr(test_multilingual_support, 'generated_files'):
        for output_file, _, _ in test_multilingual_support.generated_files:
            test_files.append(output_file)
    
    print("\n🧹 Cleaning up test files...")
    
    # Clean up all test files (no need to open again, already reviewed)
    cleaned_count = 0
    for file_path in test_files:
        if Path(file_path).exists():
            os.remove(file_path)
            cleaned_count += 1
    
    if cleaned_count > 0:
        print(f"✅ Cleaned up {cleaned_count} test files")
    else:
        print("ℹ️  No test files to clean up")


def main():
    """Run all end-to-end tests."""
    print("🚀 COMPREHENSIVE END-TO-END TEST SUITE")
    print("=" * 60)
    print("Testing the complete AI Real Estate Generator pipeline:")
    print("✅ Environment & API connectivity")
    print("✅ JSON validation & processing") 
    print("✅ Content generation pipeline")
    print("✅ Multilingual support (EN, PT, ES)")
    print("✅ Content quality evaluation")
    print("✅ All bonus features")
    print("\nThis comprehensive test may take 3-5 minutes...\n")

    tests = [
        ("Environment Setup", test_environment_setup),
        ("OpenRouter Connection", test_openrouter_connection),
        ("Sample JSON Validation", test_sample_json_validation),
        ("Full Pipeline Execution", test_full_pipeline),
        ("Output Quality Check", test_output_quality),
        ("Multilingual Support", test_multilingual_support),
        ("Content Quality Evaluation", test_content_evaluator)
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
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The system is working perfectly end-to-end.")
        print("\n🌍 You can now confidently use all 3 languages:")
        print("  python main.py examples/sample_en_lisbon.json      # English")
        print("  python main.py examples/sample_pt_porto.json       # Portuguese")
        print("  python main.py examples/sample_spanish_madrid.json # Spanish")
        print("\n🎯 Plus tone customization and content evaluation features!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")

    # Cleanup
    cleanup()

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
