#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import locale
import codecs

# Force UTF-8 output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
"""
AI-Powered Real Estate Content Generator

This CLI tool generates SEO-optimized property listings in HTML format
based on structured JSON input data. Supports English and Portuguese languages.

Usage:
    python main.py <input_json_path>
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader
from llm_service import LLMService


class RealEstateContentGenerator:
    """Main class for generating real estate content."""

    def __init__(self, initialize_llm=True):
        if initialize_llm:
            self.llm_service = LLMService()
        else:
            self.llm_service = None
        self.template_env = Environment(loader=FileSystemLoader('prompts'))

    def validate_json_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the input JSON contains all required keys.

        Required keys: location, features, price, language
        Optional keys: tone
        """
        required_keys = ['location', 'features', 'price', 'language']

        for key in required_keys:
            if key not in data:
                print(f"Error: Missing required key '{key}' in input JSON", file=sys.stderr)
                return False

        # Validate language field
        if data['language'] not in ['en', 'pt', 'es']:
            print(f"Error: Language must be 'en', 'pt', or 'es', got '{data['language']}'", file=sys.stderr)
            return False

        # Validate tone field (optional)
        valid_tones = ['formal', 'friendly', 'luxury', 'investor']
        if 'tone' in data and data['tone'] not in valid_tones:
            print(f"Error: Tone must be one of {valid_tones}, got '{data['tone']}'", file=sys.stderr)
            return False

        # Set default tone if not provided
        if 'tone' not in data:
            data['tone'] = 'friendly'

        return True

    def generate_section(self, section_name: str, data: Dict[str, Any]) -> str:
        """
        Generate content for a specific section using LLM.

        Args:
            section_name: Name of the section (e.g., 'title', 'description')
            data: Input JSON data

        Returns:
            Generated content wrapped in appropriate HTML tags
        """
        try:
            # Load and render the template
            template = self.template_env.get_template(f'{section_name}.txt')
            prompt = template.render(**data)

            # Generate content using LLM (if available)
            if self.llm_service:
                content = self.llm_service.generate_content(prompt)
            else:
                # For testing: return a mock response
                content = f"[TEST MODE] Generated {section_name} content"

            # Wrap content in appropriate HTML tags
            return self.wrap_in_html_tags(section_name, content)

        except Exception as e:
            print(f"Error generating {section_name}: {e}", file=sys.stderr)
            return ""

    def wrap_in_html_tags(self, section_name: str, content: str) -> str:
        """
        Wrap generated content in the appropriate HTML tags for each section.
        """
        tag_mapping = {
            'title': f'<title>{content}</title>',
            'meta_description': f'<meta name="description" content="{content}">',
            'h1': f'<h1>{content}</h1>',
            'description': f'<section id="description">{content}</section>',
            'key_features': f'<ul id="key-features">{content}</ul>',
            'neighborhood': f'<section id="neighborhood">{content}</section>',
            'call_to_action': f'<p class="call-to-action">{content}</p>'
        }

        return tag_mapping.get(section_name, content)

    def generate_full_content(self, data: Dict[str, Any]) -> str:
        """
        Generate the complete 7-part HTML content structure.

        Sections in order:
        1. title
        2. meta_description
        3. h1
        4. description
        5. key_features
        6. neighborhood
        7. call_to_action
        """
        sections = [
            'title',
            'meta_description',
            'h1',
            'description',
            'key_features',
            'neighborhood',
            'call_to_action'
        ]

        output_parts = []
        for section in sections:
            content = self.generate_section(section, data)
            if content:
                output_parts.append(content)

        return '\n'.join(output_parts)

    def generate_complete_html(self, data: Dict[str, Any]) -> str:
        """
        Generate a complete HTML document with proper UTF-8 encoding.
        This ensures Portuguese characters display correctly in browsers.
        """
        content = self.generate_full_content(data)
        
        html_template = f"""<!DOCTYPE html>
<html lang="{data.get('language', 'en')}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {content}
</head>
<body>
    <!-- Content is in the head for SEO optimization -->
</body>
</html>"""
        return html_template


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate SEO-optimized real estate property listings from JSON data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py property_data.json
  python main.py /path/to/input.json

The JSON file must contain: location, features, price, and language fields.
Language must be 'en' for English or 'pt' for Portuguese.
        """
    )

    parser.add_argument(
        'input_json_path',
        type=str,
        help='Path to the input JSON file containing property data'
    )
    
    parser.add_argument(
        '--html',
        action='store_true',
        help='Generate complete HTML document with UTF-8 encoding (fixes Portuguese characters in browsers)'
    )

    args = parser.parse_args()

    # Check if input file exists
    input_path = Path(args.input_json_path)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print(f"Error: '{input_path}' is not a file", file=sys.stderr)
        sys.exit(1)

    try:
        # Read and parse JSON
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Initialize generator and validate input
        generator = RealEstateContentGenerator()
        if not generator.validate_json_input(data):
            sys.exit(1)

        # Generate content
        if args.html:
            output = generator.generate_complete_html(data)
        else:
            output = generator.generate_full_content(data)

        # Always print with explicit UTF-8 encoding, with a comprehensive fallback
        try:
            print(output.encode('utf-8', errors='replace').decode('utf-8'))
        except Exception as e:
            try:
                # Try printing as-is (may work in some environments)
                print(output)
            except Exception as e2:
                # As a last resort, print a safe error message
                print("[Error] Unable to print output due to encoding issues.", file=sys.stderr)
                print(f"[Debug] First error: {e}", file=sys.stderr)
                print(f"[Debug] Second error: {e2}", file=sys.stderr)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
