#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io

# Basic UTF-8 configuration for console output
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, io.UnsupportedOperation, RuntimeError) as e:
        # Silently handle cases where stream reconfiguration fails
        # - AttributeError: if reconfigure exists but is not callable
        # - UnsupportedOperation: if the stream doesn't support reconfiguration
        # - RuntimeError: if the stream is already closed or in an invalid state
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


def make_ascii_safe(text: str) -> str:
    """Convert accented characters to ASCII-safe alternatives for terminals with encoding issues."""
    replacements = {
        # Portuguese & Spanish characters
        'ã': 'a~', 'á': 'a', 'ç': 'c', 'é': 'e', 'ê': 'e', 'í': 'i', 
        'ó': 'o', 'ô': 'o', 'õ': 'o~', 'ú': 'u', 'ñ': 'n~',
        # Uppercase
        'Ã': 'A~', 'Á': 'A', 'Ç': 'C', 'É': 'E', 'Ê': 'E', 'Í': 'I',
        'Ó': 'O', 'Ô': 'O', 'Õ': 'O~', 'Ú': 'U', 'Ñ': 'N~',
        # Symbols
        '²': '2', '³': '3', '€': 'EUR',
    }
    
    result = text
    for accented, ascii_alt in replacements.items():
        result = result.replace(accented, ascii_alt)
    return result


class RealEstateContentGenerator:
    """Main class for generating real estate content."""

    def __init__(self, initialize_llm=True):
        if initialize_llm:
            self.llm_service = LLMService()
        else:
            self.llm_service = None
        self.template_env = Environment(loader=FileSystemLoader('prompts'))

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

    @staticmethod
    def wrap_in_html_tags(section_name: str, content: str) -> str:
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

    @staticmethod
    def validate_json_input(data: Dict[str, Any]) -> bool:
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
    
    parser.add_argument(
        '--safe-output',
        action='store_true',
        help='Use ASCII-safe output mode for terminals with encoding issues (converts accented characters to '
             'alternatives)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Save output directly to file with UTF-8 encoding (avoids PowerShell redirection encoding issues)'
    )
    
    parser.add_argument(
        '--evaluate',
        action='store_true',
        help='Evaluate content quality after generation (shows quality score and detailed analysis)'
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
        
        # Evaluate content quality if requested
        if args.evaluate:
            try:
                from content_evaluator import ContentEvaluator
                evaluator = ContentEvaluator()
                
                print("\n" + "="*50, file=sys.stderr)
                print("📊 CONTENT QUALITY EVALUATION", file=sys.stderr)
                print("="*50, file=sys.stderr)
                
                # Generate evaluation report
                report = evaluator.generate_report(output, data['language'])
                score = report['overall_score']
                
                # Display results
                print(f"📈 Overall Quality Score: {score}/100", file=sys.stderr)
                
                if score >= 80:
                    print("🏆 EXCELLENT - Content exceeds expectations!", file=sys.stderr)
                elif score >= 60:
                    print("✅ GOOD - Content meets quality standards", file=sys.stderr)
                elif score >= 40:
                    print("⚠️  FAIR - Content needs some improvement", file=sys.stderr)
                else:
                    print("❌ POOR - Content requires significant improvement", file=sys.stderr)
                
                # Show detailed breakdown
                print("\n📋 Detailed Analysis:", file=sys.stderr)
                
                # Readability metrics
                if 'readability' in report:
                    readability = report['readability']
                    print(f"  📖 Readability:", file=sys.stderr)
                    print(f"    • Flesch Score: {readability.get('flesch_score', 0):.1f}/100", file=sys.stderr)
                    print(f"    • Avg Words/Sentence: {readability.get('avg_words_per_sentence', 0):.1f}",
                          file=sys.stderr)
                    print(f"    • Total Words: {readability.get('total_words', 0)}", file=sys.stderr)
                
                # SEO evaluation
                if 'seo' in report:
                    seo = report['seo']
                    seo_score = seo.get('seo_score', 0)
                    print(f"  🎯 SEO Score: {seo_score}/100", file=sys.stderr)
                    keyword_count = seo.get('keyword_count', 0)
                    if keyword_count > 0:
                        print(f"    • Keywords found: {keyword_count} keywords", file=sys.stderr)
                        print(f"    • Keyword density: {seo.get('keyword_density', 0)}%", file=sys.stderr)
                
                # Character limits
                if 'character_limits' in report:
                    limits = report['character_limits']
                    compliant_count = sum(1 for section in limits.values() if section.get('compliant', False))
                    total_count = len(limits)
                    print(f"  📏 Character Limits: {compliant_count}/{total_count} sections compliant", file=sys.stderr)
                    
                    # Show non-compliant sections
                    for section, data in limits.items():
                        if not data.get('compliant', True):
                            print(f"    ❌ {section}: {data.get('status', 'Check failed')}", file=sys.stderr)
                
                # Structure compliance
                if 'structure_compliance' in report:
                    structure = report['structure_compliance']
                    sections_found = sum(1 for found in structure.values() if found)
                    print(f"  🏗️  Structure: {sections_found}/7 sections found", file=sys.stderr)
                    
                    # Show which sections are missing
                    missing_sections = [section for section, found in structure.items() if not found]
                    if missing_sections:
                        print(f"    ❌ Missing: {', '.join(missing_sections)}", file=sys.stderr)
                
                print("\n💡 Tips for improvement:", file=sys.stderr)
                print("  • Use --html option for complete document structure", file=sys.stderr)
                print("  • Ensure all 7 required sections are present", file=sys.stderr)
                print("  • Check character limits for title (<60) and meta description (<155)", file=sys.stderr)
                
                print("="*50, file=sys.stderr)
                
            except (ImportError, NameError):
                print("⚠️  Content evaluator not available. Install required dependencies.", file=sys.stderr)
            except Exception as e:
                print(f"⚠️  Evaluation failed: {e}", file=sys.stderr)

        # Handle output destination
        if args.output:
            # Save directly to file with UTF-8 encoding (recommended method)
            try:
                output_content = make_ascii_safe(output) if args.safe_output else output
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                print(f"Output saved successfully to: {args.output}")
            except Exception as e:
                print(f"Error saving to file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Output to console (may have encoding issues on some Windows systems)
            try:
                if args.safe_output:
                    # Use ASCII-safe output
                    safe_output = make_ascii_safe(output)
                    print(safe_output)
                else:
                    # Try direct print
                    print(output)
            except UnicodeEncodeError:
                # Fallback to safe mode if encoding fails
                print("Note: Using ASCII-safe output due to terminal encoding limitations", file=sys.stderr)
                safe_output = make_ascii_safe(output)
                print(safe_output)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
