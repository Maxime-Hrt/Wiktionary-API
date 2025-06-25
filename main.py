from flask import Flask, request
from typing import List, Dict, Tuple, Optional, Union, Any
import httpx
import re

app = Flask(__name__)

endpoint = "https://en.wiktionary.org/api/rest_v1/page/definition"

# Python regex pattern to match HTML tags
filter_regex = r"<\s*/?[a-z]+(?:\s+[a-z]+=\"[^<>\"]+\")*\s*/?>"

def clean_definition_string(definition_string: str) -> str:
    """Remove HTML tags from definition string and replace &nbsp; with space.
    
    Args:
        definition_string: Raw definition string that may contain HTML tags
        
    Returns:
        Cleaned definition string with HTML tags removed
    """
    return re.sub(filter_regex, '', definition_string).replace('&nbsp;', ' ')

# Example response structure for documentation
example_response = [
    {
        "partOfSpeech": "noun",
        "definitions": ["definition 1", "definition 2"],
        "examples": ["example 1", "example 2"],
    }
]

async def fetch_and_parse_definition(word: str, locale: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Fetch and parse word definitions from Wiktionary API.
    
    Args:
        word: The word to look up
        locale: Language code for the definition (e.g. 'en' for English)
        
    Returns:
        A tuple containing:
            - List of parsed definitions if successful, None if failed
            - Error message if failed, None if successful
            
    Each definition in the returned list contains:
        - partOfSpeech: The grammatical category (noun, verb, etc.)
        - definition: The actual meaning
        - examples: List of example usages
    """
    url = f"{endpoint}/{word}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            key = locale if locale in data else list(data.keys())[0]
            
            if not data[key]:
                return None, "No definition found"
                
            output = []
            for definitions in data[key]:
                part_of_speech = definitions.get('partOfSpeech')
                if definitions.get('definitions'):
                    for definition in definitions['definitions']:
                        examples = []
                        if definition.get('examples'):
                            for example in definition['examples']:
                                examples.append(clean_definition_string(example))
                        output.append({
                            "partOfSpeech": part_of_speech,
                            "definition": clean_definition_string(definition.get('definition')),
                            "examples": examples
                        })
            return output, None
        except Exception as e:
            return None, str(e)

@app.route('/<word>', methods=['GET'])
async def get_definition(word: str) -> Tuple[Dict[str, Any], int]:
    """Flask route handler for word definition lookups.
    
    Args:
        word: The word to look up definitions for
        
    Returns:
        Tuple containing:
            - Dictionary with either definitions or error message
            - HTTP status code
            
    Query Parameters:
        locale: Language code for the definition (defaults to 'en')
    """
    locale = request.args.get('locale', 'en')
    definitions, error = await fetch_and_parse_definition(word, locale)
    
    if error:
        status_code = 404 if error == "No definition found" else 500
        return {"error": error}, status_code
        
    return {"definitions": definitions}, 200


if __name__ == '__main__':
    app.run(use_reloader=True)