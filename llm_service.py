"""
LLM Service Module for Real Estate Content Generation

This module handles all communication with OpenRouter API using DeepSeek Chat
for generating property listing content.
"""

import sys
import os
import io
from typing import Optional

# Force UTF-8 output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, io.UnsupportedOperation, RuntimeError) as e:
        # Silently handle cases where stream reconfiguration fails
        # - AttributeError: if reconfigure exists but is not callable
        # - UnsupportedOperation: if the stream doesn't support reconfiguration
        # - RuntimeError: if the stream is already closed or in an invalid state
        pass

try:
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError as e:
    missing_package = str(e).split("'")[1] if "'" in str(e) else "openai or python-dotenv"
    print(f"Error: {missing_package} package not installed. Run: pip install openai python-dotenv", file=sys.stderr)
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()


class LLMService:
    """Service class for interacting with OpenRouter API using DeepSeek Chat."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM service with OpenRouter API key.

        Args:
            api_key: OpenRouter API key. If None, will look for API_KEY_OPENROUTER environment variable.
        """
        self.api_key = api_key or os.getenv('API_KEY_OPENROUTER')

        if not self.api_key:
            print("Error: API_KEY_OPENROUTER environment variable not set", file=sys.stderr)
            print("Please set your API key: export API_KEY_OPENROUTER='your-api-key-here'", file=sys.stderr)
            sys.exit(1)

        # Initialize OpenAI client pointing to OpenRouter
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

        # Configure generation parameters for consistent, high-quality output
        self.generation_config = {
            "model": "deepseek/deepseek-chat",
            "temperature": 0.7,  # Balanced creativity and consistency
            "max_tokens": 2048,  # Sufficient for property descriptions
            "top_p": 0.8,
        }

    def generate_content(self, prompt: str) -> str:
        """
        Generate content using OpenRouter API with DeepSeek Chat.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Generated text content

        Raises:
            Exception: If API call fails
        """
        try:
            # Create the messages for chat completion
            messages = [
                {"role": "user", "content": prompt}
            ]

            # Make the API call
            completion = self.client.chat.completions.create(
                model=self.generation_config["model"],
                messages=messages,
                temperature=self.generation_config["temperature"],
                max_tokens=self.generation_config["max_tokens"],
                top_p=self.generation_config["top_p"],
            )

            # Extract the text content
            if completion.choices and len(completion.choices) > 0:
                content = completion.choices[0].message.content
                if content:
                    # Normalize problematic Unicode characters to ASCII equivalents
                    normalized_content = self._normalize_text(content.strip())
                    return normalized_content
                else:
                    raise Exception("Empty response from API")
            else:
                raise Exception("No choices returned from API")

        except Exception as e:
            error_msg = f"API call failed: {str(e)}"
            print(f"Error: {error_msg}", file=sys.stderr)
            raise Exception(error_msg)

    def test_connection(self) -> bool:
        """
        Test the API connection with a simple prompt.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            test_prompt = "Respond with 'OK' if you can understand this message."
            response = self.generate_content(test_prompt)
            return 'OK' in response.upper()
        except Exception:
            return False

    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Selectively normalize problematic Unicode characters while preserving Portuguese authenticity.

        Converts typographic characters (smart quotes, em dashes) that cause terminal issues
        but preserves Portuguese accented characters (á, ã, é, ó, ç) for authenticity.

        Args:
            text: Input text that may contain smart quotes and accented characters

        Returns:
            Text with typographic issues fixed but Portuguese characters preserved
        """
        # Dictionary of problematic Unicode characters and their ASCII replacements
        # SELECTIVE NORMALIZATION: Only convert problematic typographic characters
        # but preserve essential Portuguese accented characters for authenticity
        replacements = {
            # Smart quotes (problematic in terminals)
            '\u2018': "'",  # Left single quotation mark
            '\u2019': "'",  # Right single quotation mark
            '\u201c': '"',  # Left double quotation mark
            '\u201d': '"',  # Right double quotation mark

            # Dashes (problematic in terminals)
            '\u2013': '-',  # En dash
            '\u2014': '-',  # Em dash

            # Other typographic characters that cause terminal issues
            '\u2026': '...',  # Horizontal ellipsis
            '\u00a0': ' ',  # Non-breaking space

            # NOTE: Portuguese accented characters (ã, é, ó, ç, etc.) are preserved
            # to maintain authenticity of Portuguese content like "São Jorge" and "Apolónia"
            # If you see garbled characters in terminal, use: python main.py --html > output.html
            '\u20ac': 'EUR',  # Euro sign (€) - converted for wider compatibility
        }

        # Apply replacements
        normalized = text
        for unicode_char, ascii_replacement in replacements.items():
            normalized = normalized.replace(unicode_char, ascii_replacement)

        return normalized
