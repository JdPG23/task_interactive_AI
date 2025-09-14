"""
LLM Service Module for Real Estate Content Generation

This module handles all communication with OpenRouter API using DeepSeek Chat
for generating property listing content.
"""

import sys
import os
import locale
from typing import Optional

# Force UTF-8 output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
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
                    return content.strip()
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
