#main.py
import os
import re
from io import BytesIO
import pypdf
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from google.generativeai import GenerativeModel, configure
from bs4 import BeautifulSoup
import time
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)

configure(api_key=os.environ['api_key'])
model = GenerativeModel("gemini-pro")


@app.route("/", methods=['GET', 'POST'])
def index():
    return send_file('src/index.html')


def extract_youtube_transcript(url):
    try:
        video_id = re.findall(r"youtube\.com/.*?v=([a-zA-Z0-9_-]+)", url)[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text
    except Exception:
        return "Error: YouTube transcript not found."


def extract_website_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception:
        return "Error: Website not reachable."


def extract_pdf_text(file):
    try:
        pdf_reader = pypdf.PdfReader(BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages :
           text += page.extract_text()
        return text
    except Exception:
        return "Error: Could not process the PDF."


def generate_gemini_response(text, mode):
    if mode == "Summary":
        prompt = f"Summarize the following text:\n\n{text}"
    elif mode == "Bullet Points":
        prompt = f"Provide a bullet point summary of the following text:\n\n{text}"
    elif mode == "Detailed":
        prompt = f"Provide a detailed summary of the following text:\n\n{text}"
    elif mode == "Key Takeaways":
        prompt = f"List the key takeaways from the following text:\n\n{text}"
    else:
        return "Error: Invalid mode."
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
             yield "data: "+ str(chunk.text) + "\n\n"


    except Exception as e:
        return f"Error: An error occurred with Gemini: {e}"


@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('url')
    file = request.files.get('file')
    mode = request.form.get('mode')

    if url:
        if "youtube.com" in url:
            text = extract_youtube_transcript(url)
        else:
            text = extract_website_text(url)
    elif file:
        text = extract_pdf_text(file)
    else:
        return jsonify({"error": "No URL or file provided."})

    if text.startswith("Error"):
         return jsonify({"result": text})


    def generate():
      yield from generate_gemini_response(text, mode)
    return app.response_class(generate(), mimetype='text/event-stream')




@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files from the src directory."""
    file_path = os.path.join('src', filename)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404


def main():
    app.run(port=5000)

if __name__ == "__main__":
    main()
