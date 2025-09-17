#!/bin/bash

echo "*** Setting up AI Real Estate Generator with OpenRouter + DeepSeek Chat ***"
echo "=========================================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
echo "[*] Installing dependencies..."
pip install -r requirements.txt

# Setup .env file
if [ ! -f ".env" ]; then
    echo "[*] Creating .env file from template..."
    cp env_example.txt .env
    echo "[!] Please edit the .env file and add your OpenRouter API key!"
    echo "   Get your key from: https://openrouter.ai/"
else
    echo "[OK] .env file already exists"
fi

# Check if API key is set
if [ -z "$API_KEY_OPENROUTER" ]; then
    echo "[!] API_KEY_OPENROUTER environment variable not set!"
    echo "Please:"
    echo "1. Edit the .env file with your actual API key"
    echo "2. Or set it manually: export API_KEY_OPENROUTER='your-key'"
    echo ""
    echo "Get your API key from: https://openrouter.ai/"
else
    echo "[OK] API_KEY_OPENROUTER is set"
fi

echo ""
echo "[*] Setup complete! You can now:"
echo "1. Run basic tests: python test_basic.py"
echo "2. Test OpenRouter: python test_openrouter.py"
echo "3. Test environment: python test_env.py"
echo "4. FULL end-to-end test: python test_end_to_end.py"
echo "5. Generate content: python main.py examples/sample_en_lisbon.json"
echo "6. Save to file: python main.py examples/sample_spanish_madrid.json -o output.html"
echo "7. WITH QUALITY EVALUATION: python main.py examples/sample_pt_porto.json -o output.html --evaluate"
echo ""
echo "[*] Starting interactive session with venv activated..."
echo "[*] You are now inside the virtual environment (venv)"
echo "[*] Type 'exit' to close this session"
echo ""

# Start a new bash session with venv activated
exec bash
