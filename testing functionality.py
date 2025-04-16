#testing functionality

from flask import Flask, render_template_string, request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as palm

# Replace with your actual API key
palm.configure(api_key="YOUR_PALM_API_KEY")
youtube_url =""
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

completion = palm.generate_text(                        
        model="models/text-bison-001",
        prompt=prompt,
        temperature=0.2,  # Adjust temperature for creativity
        max_output_tokens=500  # Adjust max tokens as needed
        )
summary = completion.result
print(summary)