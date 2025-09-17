@echo off
echo *** Setting up AI Real Estate Generator with OpenRouter + DeepSeek Chat ***
echo =======================================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt

REM Setup .env file
if not exist ".env" (
    echo [*] Creating .env file from template...
    copy env_example.txt .env
    echo [!] Please edit the .env file and add your OpenRouter API key!
    echo    Get your key from: https://openrouter.ai/
) else (
    echo [OK] .env file already exists
)

REM Check if API key is set
if "%API_KEY_OPENROUTER%"=="" (
    echo [!] API_KEY_OPENROUTER environment variable not set!
    echo Please:
    echo 1. Edit the .env file with your actual API key
    echo 2. Or set it manually: set API_KEY_OPENROUTER=your-key
    echo.
    echo Get your API key from: https://openrouter.ai/
) else (
    echo [OK] API_KEY_OPENROUTER is set
)

echo.
echo [*] Setup complete! You can now:
echo 1. Run basic tests: python test_basic.py
echo 2. Test OpenRouter: python test_openrouter.py
echo 3. Test environment: python test_env.py
echo 4. FULL end-to-end test: python test_end_to_end.py
echo 5. Generate content: python main.py examples\sample_en_lisbon.json
echo 6. Save to file: python main.py examples\sample_spanish_madrid.json -o output.html
echo 7. WITH QUALITY EVALUATION: python main.py examples\sample_pt_porto.json -o output.html --evaluate
echo.
echo [*] Starting interactive session with venv activated...
echo [*] You are now inside the virtual environment (venv)
echo [*] Type 'exit' to close this session
echo.

REM Start a new command prompt with venv activated
cmd /k
