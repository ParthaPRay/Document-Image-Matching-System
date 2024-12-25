########
# Document-Image Matching System Implementation
#######
# Developed by:
# Partha Pratim Ray
# http://github.com/ParthaPRay
# Commercial Licencse [Do NOT use the code without written permission for any type of work such as research or duplication or anything similar]
# Contact parthapratimray1986@gmail.com
# 2024

##########

# Version 1

#######################################################
 
### Used opanAI and open library APIs

# Create a .env file in same directory of this code and save youw own openai API key
"""
OPENAI_API_KEY=your_secret_api_key_here
"""

import os
import base64
import requests
import pandas as pd
import gradio as gr
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI  # Updated library

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Create a global AsyncOpenAI client
client = AsyncOpenAI(api_key=api_key)

####### For low res mode, openai expects a 512px x 512px image. 
####### For high res mode, the short side of the image should be less than 768px and the long side should be less than 2,000px.

############################
# 1) Async Vision + Summaries
############################
async def analyze_image_and_extract_keywords(image_base64: str) -> str:
    """
    1) Sends base64-encoded image to an OpenAI vision model to get a textual description.
    2) Summarizes that textual description into 1 keyword.
    Returns a string of those keywords.
    """

    # STEP A: Send image to an OpenAI vision-capable model for description
    try:
        vision_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Describe the main objects, concepts, or actions in this image."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=150,
            temperature=0.7,
        )

        description_text = vision_response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error analyzing image: {e}"

    # STEP B: Summarize that textual description into 1 keyword
    try:
        summarization_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant who extracts concise keywords.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Original description:\n\n{description_text}\n\n"
                        "Extract the top 1 keyword or named entity from this text."
                    ),
                },
            ],
            max_tokens=50,
            temperature=0.0,
        )
        summary_keywords = summarization_response.choices[0].message.content.strip()

    except Exception as e:
        summary_keywords = f"Error extracting keywords: {e}"

    return summary_keywords

############################
# 2) Open Library Fetch
############################
def fetch_books(query, limit=5):
    """
    Fetches books from the Open Library Search API using a general ('q') query.
    Returns a DataFrame with relevant book details.
    """
    base_url = "https://openlibrary.org/search.json"
    params = {"q": query, "limit": limit}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        books = []
        for doc in data.get("docs", []):
            book = {
                "Title": doc.get("title", "N/A"),
                "Author": ", ".join(doc.get("author_name", ["Unknown"])),
                "First Publish Year": doc.get("first_publish_year", "N/A"),
                "Edition Count": doc.get("edition_count", "N/A"),
                "Open Library ID": doc.get("key", "N/A"),
            }
            books.append(book)

        return pd.DataFrame(books)
    except requests.RequestException as e:
        return pd.DataFrame([{"Error": f"Error fetching data: {e}"}])

############################
# 3) Async Pipeline
############################
async def async_process_image(image):
    """
    Async pipeline that:
      1) Converts the uploaded image to base64
      2) Sends it to the OpenAI Vision + Summaries to get keywords
      3) Uses those keywords to query Open Library
      4) Returns (text_summary, dataframe)
    """
    if image is None:
        return "No image provided", None

    # Convert image to base64
    with open(image, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    # 1) Analyze + Summarize
    keywords = await analyze_image_and_extract_keywords(base64_image)

    # 2) Query books
    books_df = fetch_books(keywords, limit=5)
    if books_df.empty:
        return f"**Extracted Keywords**: {keywords}\n\nNo books found.", None

    # 3) Format results
    books_str = books_df.to_string(index=False)
    output_text = (
        f"**Extracted Keywords**: {keywords}\n\n"
        f"**Top Books**:\n{books_str}"
    )

    return output_text, books_df

def process_image(image):
    """
    This is the synchronous function Gradio calls. 
    Under the hood, it runs the async pipeline via asyncio.run().
    """
    return asyncio.run(async_process_image(image))

############################
# 4) Gradio Interface
############################
with gr.Blocks() as demo:
    gr.Markdown("""
    ## Document-Image Matching System Implementation
    
    **Image → Keywords → Books (Async OpenAI Vision + Text API and Open Library API)**
    
    **Developed by Partha Pratim Ray**
    
    **Contact: parthapratimray1986@gmail.com, Copyright 2024**

    **Commercial License**
    
    This application uses an AI-powered pipeline to analyze images, extract keywords, and fetch relevant books. Interested persons/entities must take permission before using any part of this code into reserach, study, learning or commerical purposes. Use of this code without written permission is legally punishable.
    """)
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath", label="Upload an image")
            submit_button = gr.Button("Analyze & Find Books")
        with gr.Column():
            output_text = gr.Markdown()
            output_table = gr.Dataframe()

    # Connect the button click to the synchronous wrapper function
    submit_button.click(
        fn=process_image,
        inputs=[image_input],
        outputs=[output_text, output_table],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")

