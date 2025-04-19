#testing functionality
import os
from flask import Flask, render_template_string, request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as palm
from google.generativeai import GenerativeModel, configure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

summary_type = "short"  # Default summary type
model = GenerativeModel("gemini-2.0-flash-001")
# Replace with your actual API key
palm.configure(api_key=os.getenv('API_KEY'))
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


#%%
# from google import genai
# client = genai.Client(api_key=os.getenv('API_KEY'))
# for m in client.models.list():
#     model_info = client.models.get(model=m.name)
#     print(model_info)
# import os
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()
# print(os.getenv('api_key'))
