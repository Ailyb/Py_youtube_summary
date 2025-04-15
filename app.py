# prompt: A basic flask web application. The front end is a simple text input box that takes a URL -the text input box would be labeled "YouTube URL". Once entered In the text input box for the YouTube URL section--we will use python packages to extract the transcript of the YouTube URL video.

!pip install flask youtube-transcript-api

from flask import Flask, render_template_string, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Transcript Extractor</title>
</head>
<body>
    <h1>YouTube Transcript Extractor</h1>
    <form method="POST">
        <label for="youtube_url">YouTube URL:</label>
        <input type="text" name="youtube_url" id="youtube_url" required><br><br>
        <input type="submit" value="Get Transcript">
    </form>
    {% if transcript %}
        <h2>Transcript:</h2>
        <pre>{{ transcript }}</pre>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = None
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        try:
            video_id = youtube_url.split("v=")[-1]
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = "\n".join([entry['text'] for entry in transcript_list])
        except Exception as e:
            transcript = f"Error: {e}"  # Handle potential errors
    return render_template_string(HTML_TEMPLATE, transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True)
