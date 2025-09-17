#!/usr/bin/env python3
"""
Content Quality and Readability Evaluator for Real Estate Listings

This module provides tools to evaluate the quality, readability, and compliance
of generated real estate content with guidelines.
"""

import re
import sys
from typing import Dict
import argparse


class ContentEvaluator:
    """Evaluates content quality and compliance with guidelines."""

    def __init__(self):
        # SEO keyword patterns for different languages
        self.seo_patterns = {
            'en': [
                r'apartment for sale',
                r'property (for sale )?in \w+',
                r'\d+\-bedroom',
                r'real estate',
            ],
            'pt': [
                r'apartamento à venda',
                r'T\d+',
                r'imóvel em \w+',
                r'propriedade',
            ],
            'es': [
                r'apartamento en venta',
                r'propiedad en \w+',
                r'apartamento de \d+ dormitorios?',
                r'inmueble',
                r'piso en venta',
            ]
        }

        # Character limits for each section
        self.limits = {
            'title': 70,
            'meta_description': 155,
            'description': (500, 700)  # range
        }

    def evaluate_readability(self, text: str) -> Dict[str, float]:
        """
        Calculate readability metrics using simplified algorithms.
        
        Returns:
            Dictionary with readability scores
        """
        # Clean text
        clean_text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        sentences = re.split(r'[.!?]+', clean_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = re.findall(r'\b\w+\b', clean_text.lower())
        syllables = sum(self._count_syllables(word) for word in words)
        
        if not sentences or not words:
            return {'flesch_score': 0, 'avg_words_per_sentence': 0, 'avg_syllables_per_word': 0}
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        # Simplified Flesch Reading Ease Score
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
        
        return {
            'flesch_score': round(flesch_score, 1),
            'avg_words_per_sentence': round(avg_sentence_length, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'total_words': len(words),
            'total_sentences': len(sentences)
        }

    def evaluate_seo_keywords(self, content: str, language: str) -> Dict[str, any]:
        """Evaluate SEO keyword presence and density."""
        patterns = self.seo_patterns.get(language, [])
        found_keywords = []
        
        for pattern in patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                found_keywords.extend(matches)
        
        words = re.findall(r'\b\w+\b', content.lower())
        keyword_density = len(found_keywords) / len(words) * 100 if words else 0
        
        return {
            'found_keywords': found_keywords,
            'keyword_count': len(found_keywords),
            'keyword_density': round(keyword_density, 2),
            'seo_score': min(100, len(found_keywords) * 20)  # Up to 100 points
        }

    def evaluate_character_limits(self, sections: Dict[str, str]) -> Dict[str, Dict]:
        """Check if content respects character limits."""
        results = {}
        
        for section, content in sections.items():
            clean_content = re.sub(r'<[^>]+>', '', content).strip()
            char_count = len(clean_content)
            
            if section in self.limits:
                limit = self.limits[section]
                if isinstance(limit, tuple):  # Range
                    min_limit, max_limit = limit
                    compliant = min_limit <= char_count <= max_limit
                    status = f"{char_count} chars (target: {min_limit}-{max_limit})"
                else:  # Maximum
                    compliant = char_count <= limit
                    status = f"{char_count}/{limit} chars"
                
                results[section] = {
                    'char_count': char_count,
                    'compliant': compliant,
                    'status': status
                }
        
        return results

    def generate_report(self, content: str, language: str = 'en') -> Dict:
        """Generate a comprehensive evaluation report."""
        # Parse sections from content
        sections = self._parse_sections(content)
        
        # Run all evaluations
        readability = self.evaluate_readability(content)
        seo = self.evaluate_seo_keywords(content, language)
        limits = self.evaluate_character_limits(sections)
        structure = self.evaluate_structure_compliance(content)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(readability, seo, limits, structure)
        
        return {
            'overall_score': overall_score,
            'readability': readability,
            'seo': seo,
            'character_limits': limits,
            'structure_compliance': structure,
            'sections_found': len(sections)
        }

    @staticmethod
    def evaluate_structure_compliance(content: str) -> Dict[str, bool]:
        """Check if all required HTML sections are present."""
        required_sections = [
            r'<title>.*?</title>',
            r'<meta name="description".*?>',
            r'<h1>.*?</h1>',
            r'<section id="description">.*?</section>',
            r'<ul id="key-features">.*?</ul>',
            r'<section id="neighborhood">.*?</section>',
            r'<p class="call-to-action">.*?</p>'
        ]

        results = {}
        for i, pattern in enumerate(required_sections, 1):
            section_name = pattern.split('"')[1] if '"' in pattern else f"section_{i}"
            results[section_name] = bool(re.search(pattern, content, re.DOTALL))

        return results

    @staticmethod
    def _parse_sections(content: str) -> Dict[str, str]:
        """Parse HTML sections from content."""
        sections = {}
        
        # Title
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            sections['title'] = title_match.group(1)
        
        # Meta description
        meta_match = re.search(r'<meta name="description" content="(.*?)">', content)
        if meta_match:
            sections['meta_description'] = meta_match.group(1)
        
        # Description section
        desc_match = re.search(r'<section id="description">(.*?)</section>', content, re.DOTALL)
        if desc_match:
            sections['description'] = desc_match.group(1)
        
        return sections

    @staticmethod
    def _calculate_overall_score(readability, seo, limits, structure) -> int:
        """Calculate overall quality score (0-100)."""
        score = 0
        
        # Readability (30 points max)
        flesch = readability.get('flesch_score', 0)
        if flesch >= 60:  # Good readability
            score += 30
        elif flesch >= 30:  # Fair readability
            score += 20
        else:  # Poor readability
            score += 10
        
        # SEO (25 points max)
        score += min(25, seo.get('seo_score', 0) // 4)
        
        # Character limits compliance (25 points max)
        compliant_sections = sum(1 for section in limits.values() if section['compliant'])
        total_sections = len(limits)
        if total_sections > 0:
            score += (compliant_sections / total_sections) * 25
        
        # Structure compliance (20 points max)
        compliant_structure = sum(1 for compliant in structure.values() if compliant)
        total_structure = len(structure)
        if total_structure > 0:
            score += (compliant_structure / total_structure) * 20
        
        return min(100, int(score))

    @staticmethod
    def _count_syllables(word: str) -> int:
        """Count syllables in a word using a simple heuristic."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel

        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1

        return max(1, syllable_count)


def main():
    """CLI interface for content evaluation."""
    parser = argparse.ArgumentParser(
        description='Evaluate real estate content quality and compliance'
    )
    parser.add_argument('content_file', help='Path to HTML content file')
    parser.add_argument('--language', choices=['en', 'pt', 'es'], default='en',
                       help='Content language for SEO evaluation')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed breakdown')
    
    args = parser.parse_args()
    
    # Read content
    try:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.content_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Evaluate content
    evaluator = ContentEvaluator()
    report = evaluator.generate_report(content, args.language)
    
    # Display results
    print("🎯 CONTENT QUALITY EVALUATION REPORT")
    print("=" * 50)
    print(f"📊 Overall Score: {report['overall_score']}/100")
    
    if report['overall_score'] >= 80:
        print("🏆 EXCELLENT - Content meets high quality standards")
    elif report['overall_score'] >= 60:
        print("✅ GOOD - Content meets basic quality standards")
    elif report['overall_score'] >= 40:
        print("⚠️  FAIR - Content needs some improvements")
    else:
        print("❌ POOR - Content needs significant improvements")
    
    if args.verbose:
        print(f"\n📖 Readability Metrics:")
        print(f"  Flesch Score: {report['readability']['flesch_score']}/100")
        print(f"  Avg Words/Sentence: {report['readability']['avg_words_per_sentence']}")
        print(f"  Total Words: {report['readability']['total_words']}")
        
        print(f"\n🔍 SEO Analysis:")
        print(f"  Keywords Found: {report['seo']['keyword_count']}")
        print(f"  Keyword Density: {report['seo']['keyword_density']}%")
        print(f"  SEO Score: {report['seo']['seo_score']}/100")
        
        print(f"\n📏 Character Limits:")
        for section, data in report['character_limits'].items():
            status = "✅" if data['compliant'] else "❌"
            print(f"  {section}: {status} {data['status']}")
        
        print(f"\n🏗️  Structure Compliance:")
        for section, compliant in report['structure_compliance'].items():
            status = "✅" if compliant else "❌"
            print(f"  {section}: {status}")


if __name__ == '__main__':
    main()
