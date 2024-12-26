# Cover Letter Generator

A web application that generates personalized cover letters based on job descriptions and company information. Built with Flask and OpenAI's GPT models.

## Features

- Generate tailored cover letters using AI
- Auto-fetch job descriptions from LinkedIn and other job boards
- Customize company name and additional context
- Copy generated letters to clipboard with one click
- Responsive web interface

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd cover-letter-writer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create your prompt template:
   - Copy `example-prompt.txt` to `prompt.txt`
   - Customize `prompt.txt` with your information
   - Note: `prompt.txt` is gitignored to protect your personal information

4. Create your configuration file:
   - Copy `example-config.json` to `config.json`
   - Add your OpenAI API key to `config.json`
   - Note: `config.json` is gitignored to protect your API key

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5001`

## Usage

1. Enter the company name
2. For job descriptions, either:
   - Paste a job posting URL and click "Fetch Description"
   - Manually paste the job description
3. Add any additional context relevant to the application
4. Click "Generate Cover Letter"
5. Copy the generated letter using the "Copy to Clipboard" button

## Requirements

- Python 3.7+
- Flask
- OpenAI API key
- Internet connection for job description fetching

## Configuration

The application can be configured through `config.json`:

- `API_KEY`: Your OpenAI API key
- `MODEL`: The OpenAI model to use (defaults to gpt-3.5-turbo)
- `HTML_PARSER_MODEL`: Model for parsing job descriptions (optional)

## Development

The project structure:
```
.
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   └── index.html      # Main page template
├── requirements.txt    # Python dependencies
├── config.json         # Configuration file (gitignored)
├── example-config.json # Example configuration file
├── prompt.txt          # Your customized prompt template (gitignored)
└── example-prompt.txt  # Example prompt template
```

## License

[MIT License](LICENSE)
