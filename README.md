# AI-Powered Real Estate Content Generator

A sophisticated CLI tool that generates SEO-optimized, multilingual property listings using DeepSeek Chat via OpenRouter API. This tool creates compelling, accurate, and benefit-oriented content for real estate marketing.

## 🚀 Features

- **SEO-First Content Generation**: Every piece of content is optimized for search engines
- **Multilingual Support**: Generates content in English (`en`), Portuguese (`pt`), and Spanish (`es`)
- **Benefit-Oriented Language**: Focuses on lifestyle benefits rather than just features
- **Robust Data Handling**: Gracefully handles missing optional data points
- **Structured Output**: Produces 7-part HTML content structure
- **CLI Interface**: Simple command-line usage with JSON input

## 📋 Requirements

- Python 3.8+
- OpenRouter API Key (DeepSeek V3 access)
- Internet connection for API calls

## 🛠️ Installation

1. **Clone or download the project files**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenRouter API Key**
   ```bash
   # Option 1: Environment variable
   export API_KEY_OPENROUTER="your-openrouter-api-key-here"

   # Option 2: .env file (recommended)
   cp env_example.txt .env
   # Then edit .env and replace with your actual API key
   ```

   The system will automatically load the API key from the `.env` file if it exists.

## 📖 Usage

### Basic Usage

**Generate content to console:**
```bash
python main.py examples/sample_en_lisbon.json
```

**Save output to HTML file (recommended):**
```bash
python main.py examples/sample_en_lisbon.json -o output.html
```

**Alternative save method:**
```bash
python main.py examples/sample_en_lisbon.json > output.html
```

**Generate complete HTML document:**
```bash
python main.py examples/sample_en_lisbon.json --html -o complete_page.html
```

**Generate with quality evaluation (recommended for important content):**
```bash
python main.py examples/sample_en_lisbon.json -o output.html --evaluate
```

The tool generates HTML-tagged content that you can save directly to an HTML file for immediate use in web pages or content management systems.

### Command Line Options

- `-o, --output FILE` - Save output directly to file with UTF-8 encoding (recommended for special characters)
- `--html` - Generate complete HTML document with proper structure
- `--safe-output` - Use ASCII-safe output mode for terminals with encoding issues
- `--evaluate` - **⚠️ RECOMMENDED**: Evaluate content quality after generation (shows quality score and detailed analysis)

### Testing the System

The system includes comprehensive tests at different levels:

#### **1. Basic Tests (No API Required)**
```bash
python test_basic.py
```
Tests core functionality without API calls (JSON validation, templates, HTML wrapping).

#### **2. Environment Tests**
```bash
python test_env.py
```
Verifies that the `.env` file is properly configured with your API key.

#### **3. API Connection Tests**
```bash
python test_openrouter.py
```
Tests the connection with OpenRouter and DeepSeek Chat model.

#### **4. End-to-End Tests (Full Pipeline)**
```bash
python test_end_to_end.py
```
**RECOMMENDED**: Runs the complete system with real API calls, testing:
- Environment configuration
- API connectivity
- JSON processing
- All 7 content sections generation
- HTML output formatting
- System integration

#### **Quick Setup & Test**
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat

# Then run end-to-end test
python test_end_to_end.py
```

```bash
# Example: Save generated content to HTML file
python main.py examples/sample_en_lisbon.json -o property_listing.html

# Example: Generate with quality evaluation  
python main.py examples/sample_pt_porto.json -o output_pt.html --evaluate
```

### Input JSON Format

The input JSON file must contain the following required fields:

```json
{
  "location": {
    "neighborhood": "Chiado",
    "city": "Lisbon",
    "region": "Lisbon",
    "country": "Portugal"
  },
  "features": {
    "bedrooms": 3,
    "bathrooms": 2,
    "area": 120,
    "balcony": true,
    "elevator": true,
    "parking": false
  },
  "price": 450000,
  "language": "en"
}
```

#### Required Fields

- **`location`** (object): Property location information
  - `neighborhood` (string): Neighborhood name
  - `city` (string): City name
  - `country` (string): Country name
  - `region` (string, optional): Region/state name

- **`features`** (object): Property characteristics
  - `bedrooms` (integer): Number of bedrooms
  - `bathrooms` (integer, optional): Number of bathrooms
  - `area` (integer): Total area in square meters
  - `balcony` (boolean, optional): Whether property has a balcony
  - `elevator` (boolean, optional): Whether building has an elevator
  - `parking` (boolean, optional): Whether parking is included
  - `year_built` (integer, optional): Year the property was built
  - `furnished` (boolean, optional): Whether property is furnished
  - `garden` (boolean, optional): Whether property has a garden

- **`price`** (integer): Property price in euros

- **`language`** (string): Output language - must be `"en"`, `"pt"`, or `"es"`

## 📄 Output Structure

The tool generates 7 HTML sections in the following order:

1. **`<title>`** - SEO-optimized page title (max 60 characters)
2. **`<meta name="description">`** - Compelling meta description (max 155 characters)
3. **`<h1>`** - Main page headline highlighting key selling points
4. **`<section id="description">`** - Rich property description (500-700 characters)
5. **`<ul id="key-features">`** - Bulleted list of 3-5 key features
6. **`<section id="neighborhood">`** - Neighborhood description and lifestyle benefits
7. **`<p class="call-to-action">`** - Call-to-action encouraging next steps

## 🌍 Language Support

### English (`"en"`)
- Uses English terminology
- Follows English grammar and conventions
- Includes SEO keywords like "apartment for sale in [location]"

### Portuguese (`"pt"`)
- Uses Portuguese conventions (Portugal variant)
- Implements "T3" notation for bedroom count
- Includes localized SEO keywords like "apartamento à venda em [localização]"
- Proper handling of Portuguese characters (ã, ç, ê, ô, etc.)

### Spanish (`"es"`)
- Uses Spanish terminology and grammar
- Follows Spanish real estate conventions
- Includes localized SEO keywords like "apartamento en venta en [ubicación]"
- Proper handling of Spanish characters (ñ, á, é, í, ó, ú, etc.)

## 📝 Examples

### Example Input (English)

```json
{
  "location": {
    "neighborhood": "Alfama",
    "city": "Lisbon",
    "country": "Portugal"
  },
  "features": {
    "bedrooms": 2,
    "bathrooms": 1,
    "area": 85,
    "balcony": true,
    "elevator": false
  },
  "price": 320000,
  "language": "en"
}
```

### Example Input (Portuguese)

```json
{
  "location": {
    "neighborhood": "Campo de Ourique",
    "city": "Lisboa",
    "country": "Portugal"
  },
  "features": {
    "bedrooms": 3,
    "bathrooms": 2,
    "area": 140,
    "balcony": true,
    "elevator": true,
    "parking": true,
    "year_built": 2018
  },
  "price": 580000,
  "language": "pt"
}
```

### Example Input (Spanish)

```json
{
  "location": {
    "neighborhood": "Malasaña",
    "city": "Madrid",
    "country": "España"
  },
  "features": {
    "bedrooms": 2,
    "bathrooms": 2,
    "area": 90,
    "balcony": true,
    "elevator": true,
    "parking": false,
    "year_built": 2019,
    "furnished": true
  },
  "price": 420000,
  "language": "es"
}
```

## 🔧 Technical Details

### Architecture

- **CLI Tool**: Built with Python's `argparse` for command-line interface
- **LLM Integration**: Uses DeepSeek Chat model via OpenRouter API
- **Template Engine**: Jinja2 for dynamic prompt generation
- **Error Handling**: Comprehensive error handling for API failures and invalid input

### Content Generation Rules

The tool follows strict content generation principles:

- **Accuracy**: Content reflects only the data provided in input JSON
- **SEO Optimization**: Natural integration of relevant keywords
- **Benefit-Focused**: Emphasizes lifestyle benefits over mere features
- **Multilingual**: Proper localization for Portuguese and Spanish content
- **Character Limits**: Strict adherence to HTML tag character limits
- **Quality Assurance**: Use `--evaluate` flag for quality scoring and improvement suggestions

> **💡 Production Tip**: Always use `--evaluate` for important content to ensure quality standards are met before publishing.

### Dependencies

- `openai >= 1.0.0` - OpenRouter API client (compatible with OpenAI library)
- `jinja2 >= 3.0.0` - Template engine for dynamic prompts
- `python-dotenv >= 1.0.0` - Environment variable loader from .env files

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: API_KEY_OPENROUTER environment variable not set
   ```
   Solution:
   - Create a `.env` file: `cp env_example.txt .env`
   - Edit `.env` and add your OpenRouter API key
   - Or set environment variable: `export API_KEY_OPENROUTER="your-key"`

2. **Missing Required Fields**
   ```
   Error: Missing required key 'location' in input JSON
   ```
   Solution: Ensure all required fields are present in your JSON file

3. **Invalid Language Code**
   ```
   Error: Language must be 'en', 'pt', or 'es', got 'fr'
   ```
   Solution: Use only `"en"`, `"pt"`, or `"es"` for the language field

4. **Import Error**
   ```
   Error: openai package not installed
   ```
   Solution: Run `pip install -r requirements.txt`

5. **Character Encoding Issues (Windows)**
   ```
   Garbled characters: apartamento en Malaša±a
   ```
   Solution: Use the `-o` option to save directly to file:
   ```bash
   python main.py examples/sample_spanish_madrid.json -o output.html
   ```

### API Rate Limits

The tool uses DeepSeek Chat via OpenRouter API which has rate limits. If you encounter rate limit errors, wait a few minutes before retrying.

## 🤝 Contributing

This tool is designed to be robust and follows real estate content marketing best practices. For improvements or bug reports, please ensure changes align with the core principles:

- SEO-first content generation
- Multilingual accuracy
- Benefit-oriented language
- Data-driven content creation

## 📄 License

This project is provided as-is for educational and commercial use in real estate content generation.

## 🔗 Links

- [OpenRouter API](https://openrouter.ai/) - For API key setup
- [DeepSeek Chat Documentation](https://api-docs.deepseek.com/) - Model reference
- [Real Estate SEO Best Practices](https://developers.google.com/search/docs/appearance/structured-data/real-estate-listing) - Google guidelines
