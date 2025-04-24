# README for Py_youtube_summary

## Overview
`Py_youtube_summary` is a Flask-based web application that summarizes content from YouTube video transcripts, websites, PDF files, or raw text input. It leverages the Google Gemini API for generating summaries in various formats (e.g., summary, bullet points, detailed, or key takeaways). The app provides a simple interface for users to input a URL, upload a PDF, or paste text and receive a summarized output.

## Features
- **YouTube Transcript Summarization**: Extracts and summarizes transcripts from YouTube videos using the `youtube_transcript_api`.
- **Website Content Summarization**: Scrapes text from websites using `BeautifulSoup` and generates summaries.
- **PDF Text Extraction**: Extracts text from uploaded PDF files using `pypdf` for summarization.
- **Text Input Summarization**: Summarizes user-provided text directly.
- **Multiple Summary Modes**: Supports different summary formats:
  - Summary
  - Bullet Points
  - Detailed
  - Key Takeaways
- **Real-Time Streaming**: Uses Server-Sent Events (SSE) to stream summary results to the client.
- **Static File Serving**: Serves HTML, CSS, and JavaScript files from the `src` directory.

## Prerequisites
- Python 3.8+
- A Google Gemini API key (set in a `.env` file)
- Required Python packages (listed in `requirements.txt`)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ailyb/Py_youtube_summary.git
   cd Py_youtube_summary
   
   
## Set Up a Virtual Environment (optional but recommended):
bash
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
## Install Dependencies:
bash
```
pip install -r requirements.txt
```
## Set Up Environment Variables:
Create a .env file in the project root.

Add your Google Gemini API key:
plaintext
```
API_KEY=your_gemini_api_key_here
```
Run the Application:
bash
```
python app.py
```
The app will run on http://localhost:5000.

## Usage
Access the Web Interface:
Open http://localhost:5000 in a browser.

The interface (src/index.html) allows you to:
Enter a YouTube URL, website URL, or paste text.

Upload a PDF file.

Select a summary mode (Summary, Bullet Points, Detailed, Key Takeaways).

Submit a Request:
Provide a YouTube URL, website URL, PDF file, or text input.

Choose a summary mode and submit.

The summary will stream in real-time via Server-Sent Events.

API Endpoint:
The app exposes a /process endpoint (POST) for programmatic access.

Example request:
bash
```
curl -X POST http://localhost:5000/process \
-F "url=https://www.youtube.com/watch?v=video_id" \
-F "mode=Summary"
```
Response: Streamed summary text in SSE format.

Project Structure
plaintext
```
Py_youtube_summary/
├── src/                    # Static files (HTML, CSS, JS)
│   └── index.html          # Main web interface
├── .env                    # Environment variables (not tracked)
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
└── README.md               # This file
```
## Dependencies
flask: Web framework for the application.

youtube_transcript_api: Fetches YouTube video transcripts.

google-generativeai: Interacts with the Google Gemini API for summarization.

pypdf: Extracts text from PDF files.

requests: Fetches website content.

beautifulsoup4: Parses HTML for website text extraction.

python-dotenv: Loads environment variables from .env.

## Install dependencies:
bash

pip install flask youtube_transcript_api google-generativeai pypdf requests beautifulsoup4 python-dotenv

## Environment Variables
API_KEY: Your Google Gemini API key (required).

## Notes
Ensure the YouTube video has transcripts enabled for summarization.

Website summarization may vary based on the site's structure and accessibility.

PDF files must be text-based (not scanned images) for text extraction to work.

The Gemini API may have usage limits or costs depending on your plan.

## Limitations
No error handling for large PDFs or very long texts (may hit API limits).

YouTube transcript extraction fails if transcripts are disabled or unavailable.

Website scraping may not work for dynamic or JavaScript-heavy sites.

Requires a valid Gemini API key for operation.

## Contributing
Contributions are welcome! To contribute:
Fork the repository.

Create a feature branch (git checkout -b feature-name).

Commit changes (git commit -m "Add feature").

Push to the branch (git push origin feature-name).

Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact


