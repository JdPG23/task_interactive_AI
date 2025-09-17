#!/usr/bin/env python3
"""
Basic test script for the Real Estate Content Generator

This script tests the basic functionality without requiring API access.
"""

import json
import sys
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, '.')

from main import RealEstateContentGenerator


def test_json_validation():
    """Test JSON validation functionality."""
    print("[TEST] Testing JSON validation...")

    generator = RealEstateContentGenerator(initialize_llm=False)

    # Test valid JSON
    valid_data = {
        "location": {"neighborhood": "Test", "city": "Test", "country": "Test"},
        "features": {"bedrooms": 2, "area": 100},
        "price": 300000,
        "language": "en"
    }

    assert generator.validate_json_input(valid_data), "Valid JSON should pass validation"
    print("[PASS] Valid JSON validation passed")

    # Test missing required key
    invalid_data = {
        "features": {"bedrooms": 2, "area": 100},
        "price": 300000,
        "language": "en"
    }

    assert not generator.validate_json_input(invalid_data), "Invalid JSON should fail validation"
    print("[PASS] Invalid JSON validation correctly failed")

    # Test invalid language
    invalid_lang_data = {
        "location": {"neighborhood": "Test", "city": "Test", "country": "Test"},
        "features": {"bedrooms": 2, "area": 100},
        "price": 300000,
        "language": "fr"  # French is not supported (only en, pt, es are valid)
    }

    assert not generator.validate_json_input(invalid_lang_data), "Invalid language should fail validation"
    print("[PASS] Invalid language validation correctly failed")


def test_template_loading():
    """Test that templates can be loaded and rendered."""
    print("\n[TEST] Testing template loading...")

    generator = RealEstateContentGenerator(initialize_llm=False)

    # Test data
    test_data = {
        "location": {"neighborhood": "Test", "city": "Test", "country": "Test"},
        "features": {"bedrooms": 2, "area": 100, "balcony": True},
        "price": 300000,
        "language": "en"
    }

    # Test that we can load and render templates (without API call)
    try:
        template = generator.template_env.get_template('title.txt')
        prompt = template.render(**test_data)
        assert len(prompt) > 0, "Template should render to non-empty content"
        assert "2-Bedroom Apartment" in prompt, "Template should contain bedroom count"
        print("[PASS] Template loading and rendering works")
    except Exception as e:
        print(f"[FAIL] Template test failed: {e}")
        return False

    return True


def test_html_wrapping():
    """Test HTML tag wrapping functionality."""
    print("\n[TEST] Testing HTML tag wrapping...")

    generator = RealEstateContentGenerator(initialize_llm=False)

    # Test different sections
    test_content = "Test content"

    title_html = generator.wrap_in_html_tags('title', test_content)
    assert title_html == f'<title>{test_content}</title>', "Title should be wrapped correctly"

    meta_html = generator.wrap_in_html_tags('meta_description', test_content)
    assert meta_html == f'<meta name="description" content="{test_content}">', "Meta should be wrapped correctly"

    desc_html = generator.wrap_in_html_tags('description', test_content)
    assert desc_html == f'<section id="description">{test_content}</section>', "Description should be wrapped correctly"

    print("[PASS] HTML tag wrapping works correctly")


def test_sample_files():
    """Test that sample JSON files are valid."""
    print("\n[TEST] Testing sample JSON files...")

    sample_files = [
        'examples/sample_en_lisbon.json',
        'examples/sample_pt_porto.json',
        'examples/sample_minimal.json'
    ]

    generator = RealEstateContentGenerator(initialize_llm=False)

    for file_path in sample_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if generator.validate_json_input(data):
                    print(f"[PASS] {file_path} is valid")
                else:
                    print(f"[FAIL] {file_path} failed validation")
                    return False
            except Exception as e:
                print(f"[FAIL] Error reading {file_path}: {e}")
                return False
        else:
            print(f"[FAIL] {file_path} does not exist")
            return False

    return True


def main():
    """Run all basic tests."""
    print("Running Real Estate Content Generator Basic Tests")
    print("=" * 50)

    try:
        test_json_validation()
        if not test_template_loading():
            return False
        test_html_wrapping()
        if not test_sample_files():
            return False

        print("\n[SUCCESS] All basic tests passed! The system is ready for API testing.")

        return True

    except Exception as e:
        print(f"\n[ERROR] Test suite failed: {e}")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
