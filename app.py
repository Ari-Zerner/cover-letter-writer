from flask import Flask, render_template, request, jsonify
import json
import openai
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

app = Flask(__name__)

# Load API key from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
    openai.api_key = config.get('API_KEY')

# Load the prompt template
with open('prompt.txt', 'r') as f:
    PROMPT_TEMPLATE = f.read()

def extract_fields_from_prompt(prompt):
    """Extract fields from the prompt, distinguishing between short and long fields."""
    # Extract double-bracketed fields first (for longer text)
    long_fields = re.findall(r'\[\[([^\]]+)\]\]', prompt)
    
    # Replace double-bracketed fields with placeholders to avoid interference
    temp_prompt = prompt
    for field in long_fields:
        temp_prompt = temp_prompt.replace(f'[[{field}]]', '')
    
    # Extract single-bracketed fields (for short text)
    short_fields = re.findall(r'\[([^\]]+)\]', temp_prompt)
    
    return {
        'short_fields': short_fields,
        'long_fields': long_fields
    }

# Extract fields when app starts
PROMPT_FIELDS = extract_fields_from_prompt(PROMPT_TEMPLATE)

@app.route('/')
def index():
    return render_template('index.html', fields=PROMPT_FIELDS)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data for each field
        field_values = {}
        
        # Get values for both short and long fields
        for field in PROMPT_FIELDS['short_fields']:
            value = request.form.get(field.lower().replace(' ', '_'), '').strip()
            field_values[field] = value if value else "(no information provided)"
        for field in PROMPT_FIELDS['long_fields']:
            value = request.form.get(field.lower().replace(' ', '_'), '').strip()
            field_values[field] = value if value else "(no information provided)"
        
        # Fill in the prompt template
        filled_prompt = PROMPT_TEMPLATE
        for field, value in field_values.items():
            # Try replacing both single and double bracketed versions
            filled_prompt = filled_prompt.replace(f'[{field}]', value)
            filled_prompt = filled_prompt.replace(f'[[{field}]]', value)

        # Call OpenAI API
        response = openai.chat.completions.create(
            model=config.get('MODEL', 'gpt-3.5-turbo'),  # Fallback to gpt-3.5-turbo if MODEL not specified
            messages=[
                {"role": "user", "content": filled_prompt}
            ]
        )

        cover_letter = response.choices[0].message.content

        return jsonify({'success': True, 'cover_letter': cover_letter})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/fetch-job-description', methods=['POST'])
def fetch_job_description():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'})

        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the job description
        description = ""
        
        # LinkedIn
        if 'linkedin.com' in url:
            description_div = soup.find('div', {'class': 'description__text'})
            if description_div:
                description = description_div.get_text(separator='\n', strip=True)
        
        # Generic fallback - look for common job description containers
        if not description:
            for selector in [
                'job-description',
                'jobDescription',
                'job_description',
                'job__description',
                'description',
                'posting-requirements'
            ]:
                element = soup.find(id=selector) or soup.find(class_=selector)
                if element:
                    description = element.get_text(separator='\n', strip=True)
                    break

        if not description:
            return jsonify({
                'success': False, 
                'error': 'Could not find job description. Please copy and paste manually.'
            })

        return jsonify({'success': True, 'description': description})

        if not description:
            return jsonify({
                'success': False, 
                'error': 'Could not find job description. Please copy and paste manually.'
            })

        return jsonify({
            'success': True, 
            'description': description,
            'company_name': company_name if company_name else ""
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
