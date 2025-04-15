# prompt: I need a python script that will take a YouTube URL, transcribe the URL and then submit the transcription to Google Gemini for summarization. From a pull down, the user should be able to request 1). A shor tsummary, 2). Bullet points, 3). a detailed summary, 4). Key take aways, or 5). Lecture notes. Then they can click a 'submit' button and the app will transcribe the video and submit the transcript to Google Gemini with the prompt according to what they selected

from flask import Flask, render_template_string, request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as palm

# Replace with your actual API key
palm.configure(api_key="YOUR_PALM_API_KEY")

!pip install flask youtube-transcript-api google-generativeai

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Summarizer</title>
</head>
<body>
    <h1>YouTube Summarizer</h1>
    <form method="POST">
        <label for="youtube_url">YouTube URL:</label>
        <input type="text" name="youtube_url" id="youtube_url" required><br><br>

        <label for="summary_type">Summary Type:</label>
        <select name="summary_type" id="summary_type">
            <option value="short">Short Summary</option>
            <option value="bullets">Bullet Points</option>
            <option value="detailed">Detailed Summary</option>
            <option value="key_takeaways">Key Takeaways</option>
            <option value="lecture_notes">Lecture Notes</option>
        </select><br><br>

        <input type="submit" value="Submit">
    </form>
    {% if summary %}
        <h2>Summary:</h2>
        <pre>{{ summary }}</pre>
    {% endif %}
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    error = None
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        summary_type = request.form.get("summary_type")

        try:
            video_id = youtube_url.split("v=")[-1]
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([entry['text'] for entry in transcript_list])

            # Construct the prompt based on the selected summary type.
            prompts = {
                "short": "Provide a short summary of the following text: ",
                "bullets": "Summarize the following text as bullet points: ",
                "detailed": "Provide a detailed summary of the following text: ",
                "key_takeaways": "What are the key takeaways from the following text? ",
                "lecture_notes": "Create lecture notes from the following text: "
            }
            prompt = prompts.get(summary_type, "Summarize the following text: ") + transcript

            completion = palm.generate_text(
                model="models/text-bison-001",
                prompt=prompt,
                temperature=0.2,  # Adjust temperature for creativity
                max_output_tokens=500  # Adjust max tokens as needed
            )
            summary = completion.result

        except Exception as e:
            error = f"An error occurred: {e}"

    return render_template_string(HTML_TEMPLATE, summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True)
