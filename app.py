import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""As a LinkedIn post caption generator, your role is to streamline the process of crafting engaging
     captions for LinkedIn posts. You'll be provided with transcript text from videos, and your task is to distill
     the essence of the entire video into a concise and compelling LinkedIn post caption. Your caption should be structured
     in  paragraph form, ensuring clarity 
     and brevity while conveying the key insights from the video. 
     Your goal is to create professional and informative captions within a 250-word limit. 
     Your input will help LinkedIn users quickly grasp the main points of the video and encourage them to engage with the content. 
     Please provide a LinkedIn caption for the given transcript text
     that effectively summarizes the video's content and captivates the audience. """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("LinkedIn post caption generator")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Caption For linkedln"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)



