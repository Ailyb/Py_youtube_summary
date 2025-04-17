#testing functionality

from flask import Flask, render_template_string, request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as palm
from google.generativeai import GenerativeModel, configure
summary_type = "short"  # Default summary type
model = GenerativeModel("gemini-pro")
# Replace with your actual API key
palm.configure(api_key="AIzaSyDsf2OnWSe4u6loFguOgXlLcsqSfZ9yWz8")
youtube_url ="https://www.youtube.com/watch?v=O-Vu-DMIU40"
video_id = youtube_url.split("v=")[-1]
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
transcript = " ".join([entry['text'] for entry in transcript_list])


prompts = {     "short": "Provide a short summary of the following text: ",
                "bullets": "Summarize the following text as bullet points: ",
                "detailed": "Provide a detailed summary of the following text: ",
                "key_takeaways": "What are the key takeaways from the following text? ",
                "lecture_notes": "Create lecture notes from the following text: "
            }
prompt = prompts.get(summary_type, "Summarize the following text: ") + transcript
response = model.generate_content(prompt)
print(response.text)
