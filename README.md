# Dictionary API

A lightweight Flask-based API that provides word definitions by querying the Wiktionary REST API. This service fetches, parses, and returns clean word definitions with parts of speech and examples.

## Features

- **Word Definition Lookup**: Get definitions for any word in multiple languages
- **Clean Data**: Automatically removes HTML tags and formatting from Wiktionary responses
- **Multiple Languages**: Support for different language codes (defaults to English)
- **Structured Response**: Returns organized data with parts of speech, definitions, and examples
- **Async Support**: Built with async/await for better performance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Maxime-Hrt/Wiktionary-API.git
cd dict
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the Flask development server:
```bash
python main.py
```

The server will start on `http://localhost:5000` with auto-reload enabled.

### API Endpoints

#### GET `/<word>`

Look up definitions for a specific word.

**Parameters:**
- `word` (path parameter): The word to look up
- `locale` (query parameter, optional): Language code (defaults to 'en')

**Example Requests:**

```bash
# Look up "hello" in English
curl -X GET "http://127.0.0.1:5000/hello"

# Look up "bonjour" in French
curl -X GET "http://127.0.0.1:5000/bonjour?locale=fr"

# Look up "tahu" in Malay
curl -X GET "http://127.0.0.1:5000/tahu?locale=ms"
```

**Response Format:**

Successful response (200):
```json
{
  "definitions": [
    {
      "partOfSpeech": "noun",
      "definition": "A greeting or an expression of goodwill.",
      "examples": ["Hello, how are you today?", "She gave me a warm hello."]
    },
    {
      "partOfSpeech": "verb",
      "definition": "To greet with 'hello'.",
      "examples": ["I helloed my neighbor as I walked by."]
    }
  ]
}
```

Error response (404/500):
```json
{
  "error": "No definition found"
}
```

## API Details

### Supported Language Codes

The API supports all language codes available in Wiktionary. Common examples:
- `en` - English
- `fr` - French
- `es` - Spanish
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `zh` - Chinese

### Data Processing

The API automatically:
- Removes HTML tags from Wiktionary responses
- Replaces HTML entities (e.g., `&nbsp;` → space)
- Structures the data into a consistent format
- Filters out empty or invalid definitions

## Dependencies

- **Flask**: Web framework with async support
- **httpx**: Async HTTP client for API requests
- **re**: Python regex module for HTML tag removal

### Key Functions

- `clean_definition_string()`: Removes HTML tags and entities from text
- `fetch_and_parse_definition()`: Async function that fetches and parses Wiktionary data
- `get_definition()`: Flask route handler for word lookups

## Error Handling

The API handles various error scenarios:
- **404**: Word not found in Wiktionary
- **500**: Network errors, API failures, or parsing issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT

## Acknowledgments

- Powered by the [Wiktionary API](https://en.wiktionary.org/api/rest_v1/)
- Built with Flask and httpx
