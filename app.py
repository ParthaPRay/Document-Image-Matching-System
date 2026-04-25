# ============================================================
# Document-Image Matching System for Open Library using GPT 5.4
# Developed By Partha Pratim Ray
# Contact: parthapratimray1986@gmail.com; ppray@cus.ac.in
# ============================================================

# ============================================================
# Reuired to Install
# pip install openai gradio pandas requests python-dotenv -q
# ============================================================

# ============================================================
# REQUIRED IMPORTS
# ============================================================
import base64
import time
import os
import requests
import pandas as pd
import gradio as gr

from datetime import datetime
from urllib.parse import quote_plus
from openai import OpenAI
from google.colab import userdata


# ============================================================
# API KEY
# ============================================================

api_key = userdata.get("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("Please add OPENAI_API_KEY in Colab Secrets.")

client = OpenAI(api_key=api_key)


# ============================================================
# MODEL SELECTION
# ============================================================

VISION_MODEL = "gpt-5.4-mini"
SUMMARY_MODEL = "gpt-5.4-nano"


# ============================================================
# CSV FILE PATH
# ============================================================

CSV_FILE_PATH = "image_open_library_results.csv"


# ============================================================
# STEP 1: IDENTIFY MAIN ENTITY FROM IMAGE
# ============================================================

def analyze_image(image_base64: str):
    start_time = time.perf_counter()

    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an image-to-library-search assistant. "
                        "Your job is not to describe the whole image generally. "
                        "Your job is to identify the single most important searchable entity "
                        "that should be used for book retrieval."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Look at this image and identify the single main searchable entity. "
                                "The entity may be a famous person, author, book title, monument, place, "
                                "historical event, object, artwork, animal, plant, scientific concept, "
                                "religious figure, cultural theme, or academic subject.\n\n"
                                "Rules:\n"
                                "1. If a famous person is recognizable or likely, return that person's name.\n"
                                "2. If text/title is visible, prefer the title or named subject.\n"
                                "3. Avoid generic visual phrases such as 'elderly man', 'portrait', "
                                "'black-and-white photo', 'traditional dress', or 'seated person'.\n"
                                "4. Do not invent unreadable text.\n"
                                "5. Give the likely main entity and one short reason.\n\n"
                                "Output format (STRICTLY follow exactly with each item on a new separate line):\n"
                                "Main Entity: <entity>\n"
                                "Confidence: <High/Medium/Low>\n"
                                "Reason: <one short sentence>\n\n"
                                "Do NOT write everything in one line.\n"
                                "Do NOT combine fields.\n"
                                "Each field must be on its own separate line."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
            max_completion_tokens=180,
            temperature=0.1,
        )

        elapsed_time = time.perf_counter() - start_time

        result = response.choices[0].message.content.strip()

        result = result.replace(" Confidence:", "\nConfidence:")
        result = result.replace(" Reason:", "\nReason:")

        return result, elapsed_time

    except Exception as e:
        elapsed_time = time.perf_counter() - start_time
        return f"ERROR_IMAGE_ANALYSIS: {e}", elapsed_time


# ============================================================
# STEP 2: EXTRACT CLEAN OPEN LIBRARY QUERY
# ============================================================

def extract_search_keyword(image_analysis: str):
    start_time = time.perf_counter()

    if image_analysis.startswith("ERROR_IMAGE_ANALYSIS"):
        elapsed_time = time.perf_counter() - start_time
        return image_analysis, elapsed_time

    try:
        response = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create Open Library search queries. "
                        "Return exactly one clean query. "
                        "Return only the main entity, not a description. "
                        "If a famous person is mentioned, return only the full name of the person. "
                        "Remove generic words such as portrait, photograph, image, picture, elderly man, "
                        "black-and-white, seated, traditional dress, robe, cap, object, or photo. "
                        "No explanation. No quotation marks."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Image analysis:\n{image_analysis}\n\n"
                        "Extract the single best Open Library search query."
                    ),
                },
            ],
            max_completion_tokens=25,
            temperature=0,
        )

        keyword = response.choices[0].message.content.strip()
        keyword = keyword.replace('"', "").replace("'", "").strip()

        elapsed_time = time.perf_counter() - start_time
        return keyword, elapsed_time

    except Exception as e:
        elapsed_time = time.perf_counter() - start_time
        return f"ERROR_KEYWORD_EXTRACTION: {e}", elapsed_time


# ============================================================
# STEP 3: OPEN LIBRARY SEARCH
# ============================================================

def fetch_books(query, limit=5):           ######## Change limit=10, or any other number as number of books you wish
    start_time = time.perf_counter()

    if query.startswith("ERROR"):
        elapsed_time = time.perf_counter() - start_time
        return pd.DataFrame([{"Error": query}]), elapsed_time

    url = "https://openlibrary.org/search.json"

    params = {
        "q": query,
        "limit": limit,
        "fields": "title,author_name,first_publish_year,edition_count,key,isbn,language"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        docs = data.get("docs", [])
        elapsed_time = time.perf_counter() - start_time

        if not docs:
            return pd.DataFrame([{"Message": "No books found for this search query."}]), elapsed_time

        books = []

        for doc in docs:
            isbn_list = doc.get("isbn", [])
            lang_list = doc.get("language", [])

            books.append({
                "Title": doc.get("title", "N/A"),
                "Author": ", ".join(doc.get("author_name", ["Unknown"])),
                "First Publish Year": doc.get("first_publish_year", "N/A"),
                "Edition Count": doc.get("edition_count", "N/A"),
                "Languages": ", ".join(lang_list[:5]) if isinstance(lang_list, list) else "N/A",
                "First ISBN": "'" + str(isbn_list[0]) if isinstance(isbn_list, list) and len(isbn_list) > 0 else "N/A",
                "Open Library Work ID": doc.get("key", "N/A"),
            })

        return pd.DataFrame(books), elapsed_time

    except Exception as e:
        elapsed_time = time.perf_counter() - start_time
        return pd.DataFrame([{"Error": f"Open Library API error: {e}"}]), elapsed_time


# ============================================================
# STEP 4: SAVE RESULTS TO CSV
# ============================================================

def extract_main_entity_confidence_reason(image_analysis):
    main_entity = ""
    confidence = ""
    reason = ""

    try:
        lines = image_analysis.split("\n")

        for line in lines:
            line = line.strip()

            if line.startswith("Main Entity:"):
                main_entity = line.replace("Main Entity:", "").strip()

            elif line.startswith("Confidence:"):
                confidence = line.replace("Confidence:", "").strip()

            elif line.startswith("Reason:"):
                reason = line.replace("Reason:", "").strip()

    except:
        pass

    return main_entity, confidence, reason
    
    
    
    
    
    
    
    
    
    
    
def save_results_to_csv(
    image_path,
    image_analysis,
    search_query,
    search_url,
    books_df,
    image_encoding_time,
    vision_api_time,
    keyword_api_time,
    open_library_api_time,
    other_processing_delay,
    total_processing_time
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    main_entity, confidence, reason = extract_main_entity_confidence_reason(image_analysis)

    rows = []

    for _, row in books_df.iterrows():
        rows.append({
            "Timestamp": timestamp,
            "Uploaded Image Path": image_path,
            "Vision Model Used": VISION_MODEL,
            "Keyword Model Used": SUMMARY_MODEL,
            "Image Analysis": image_analysis,
            "Main Entity": main_entity,
            "Confidence": confidence,
            "Reason": reason,
            "Final Open Library Search Query": search_query,
            "Open Library Search URL": search_url,

            "Title": row.get("Title", "N/A"),
            "Author": row.get("Author", "N/A"),
            "First Publish Year": row.get("First Publish Year", "N/A"),
            "Edition Count": row.get("Edition Count", "N/A"),
            "Languages": row.get("Languages", "N/A"),
            "First ISBN": row.get("First ISBN", "N/A"),
            "Open Library Work ID": row.get("Open Library Work ID", "N/A"),
            "Message": row.get("Message", ""),
            "Error": row.get("Error", ""),

            "Image Encoding Time (seconds)": round(image_encoding_time, 4),
            "Vision API Time (seconds)": round(vision_api_time, 4),
            "Keyword API Time (seconds)": round(keyword_api_time, 4),
            "Open Library API Time (seconds)": round(open_library_api_time, 4),
            "Other Processing / Network Delay (seconds)": round(other_processing_delay, 4),
            "Total Processing Time (seconds)": round(total_processing_time, 4)
        })

    csv_df = pd.DataFrame(rows)

    if os.path.exists(CSV_FILE_PATH):
        csv_df.to_csv(CSV_FILE_PATH, mode="a", index=False, header=False, encoding="utf-8-sig")
    else:
        csv_df.to_csv(CSV_FILE_PATH, mode="w", index=False, header=True, encoding="utf-8-sig")

    return CSV_FILE_PATH

# ============================================================
# STEP 5: MAIN PIPELINE
# ============================================================

def process_image(image):
    total_start_time = time.perf_counter()

    if image is None:
        return "Please upload an image.", None, None, None

    image_encoding_start = time.perf_counter()

    with open(image, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    image_encoding_time = time.perf_counter() - image_encoding_start

    image_analysis, vision_api_time = analyze_image(image_base64)
    search_query, keyword_api_time = extract_search_keyword(image_analysis)
    books_df, open_library_api_time = fetch_books(search_query, limit=5)       ######## Change limit=10, or any other number as number of books you wish

    total_processing_time = time.perf_counter() - total_start_time

    other_processing_delay = total_processing_time - (
        image_encoding_time +
        vision_api_time +
        keyword_api_time +
        open_library_api_time
    )

    encoded_query = quote_plus(search_query)
    search_url = f"https://openlibrary.org/search.json?q={encoded_query}"

    timing_df = pd.DataFrame([
        {
            "Processing Stage": "Image Encoding",
            "Model/API Used": "Local base64 encoding",
            "Time Taken (seconds)": round(image_encoding_time, 4)
        },
        {
            "Processing Stage": "Image Analysis API Call",
            "Model/API Used": VISION_MODEL,
            "Time Taken (seconds)": round(vision_api_time, 4)
        },
        {
            "Processing Stage": "Keyword Extraction API Call",
            "Model/API Used": SUMMARY_MODEL,
            "Time Taken (seconds)": round(keyword_api_time, 4)
        },
        {
            "Processing Stage": "Open Library API Call",
            "Model/API Used": "Open Library Search API",
            "Time Taken (seconds)": round(open_library_api_time, 4)
        },
        {
            "Processing Stage": "Other Processing / Network Delay",
            "Model/API Used": "Internal pipeline overhead",
            "Time Taken (seconds)": round(other_processing_delay, 4)
        },
        {
            "Processing Stage": "Total Processing Time",
            "Model/API Used": "Complete end-to-end pipeline",
            "Time Taken (seconds)": round(total_processing_time, 4)
        }
    ])

    csv_file = save_results_to_csv(
        image_path=image,
        image_analysis=image_analysis,
        search_query=search_query,
        search_url=search_url,
        books_df=books_df,
        image_encoding_time=image_encoding_time,
        vision_api_time=vision_api_time,
        keyword_api_time=keyword_api_time,
        open_library_api_time=open_library_api_time,
        other_processing_delay=other_processing_delay,
        total_processing_time=total_processing_time
    )

    output_text = f"""
## Result

**Vision Model Used:** `{VISION_MODEL}`  
**Keyword Model Used:** `{SUMMARY_MODEL}`  

### Image Analysis

{image_analysis.replace(chr(10), "  \n")}

### Final Open Library Search Query
`{search_query}`

### Open Library Search URL
`{search_url}`

### Processing Time Summary

**Vision API Time:** `{round(vision_api_time, 4)} seconds`  
**Keyword API Time:** `{round(keyword_api_time, 4)} seconds`  
**Open Library API Time:** `{round(open_library_api_time, 4)} seconds`  
**Total Processing Time:** `{round(total_processing_time, 4)} seconds`

### CSV Saving Status

Results have been saved successfully in local CSV file:

`{CSV_FILE_PATH}`
"""

    return output_text, books_df, timing_df, csv_file


# ============================================================
# STEP 6: ATTRACTIVE GRADIO INTERFACE (SOBER COLOR SCHEME)
# ============================================================

custom_css = """
body {
    background: linear-gradient(135deg, #f8fafc 0%, #f5f5f4 45%, #fafaf9 100%);
}

.gradio-container {
    max-width: 1500px !important;
    margin: auto !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

#main-header {
    text-align: center;
    padding: 30px 22px;
    border-radius: 22px;
    background: linear-gradient(135deg, #dbeafe, #e0e7ff, #f5f3ff);
    color: #1e293b;
    margin-bottom: 22px;
    box-shadow: 0 10px 24px rgba(148, 163, 184, 0.18);
    border: 1px solid #cbd5e1;
}

#main-header h1 {
    font-size: 34px;
    margin-bottom: 8px;
    font-weight: 700;
    color: #0f172a;
}

#main-header p {
    font-size: 16px;
    opacity: 0.95;
    color: #334155;
}

.info-card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    border: 1px solid #d6d3d1;
    margin-bottom: 18px;
}

#upload-card, #result-card {
    background: white;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    border: 1px solid #d6d3d1;
}

#analyze-btn {
    background: linear-gradient(135deg, #374151, #111827) !important;
    color: white !important;
    border-radius: 14px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 12px !important;
    border: none !important;
}

#analyze-btn:hover {
    box-shadow: 0 8px 18px rgba(17, 24, 39, 0.18);
}

#footer-note {
    text-align: center;
    color: #57534e;
    font-size: 13px;
    margin-top: 18px;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    gr.HTML(
        """
        <div id="main-header">
            <h1>📚 Document–Image Matching System for Open Library using GPT5.4</h1>
            <p>AI-powered Image → Main Entity Identification → Open Library Book Retrieval</p>
        </div>
        """
    )

    gr.Markdown(
        """
        <div class="info-card">

        ### 🔍 System Workflow

        **Image Upload** → **Main Entity Detection** → **Clean Search Query** → **Open Library Results**

        **Model Strategy:**  
        - 🖼️ Image/entity identification: `gpt-5.4-mini`  
        - 🧠 Query cleaning: `gpt-5.4-nano`  
        - 📖 Retrieval source: Open Library API  

        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=1, elem_id="upload-card"):
            gr.Markdown("## 🖼️ Upload Image")

            image_input = gr.Image(
                type="filepath",
                label="Upload an image of a person, book cover, monument, object, or document",
                height=500
            )

            submit_button = gr.Button(
                "🚀 Analyze Image and Find Books",
                elem_id="analyze-btn"
            )

        with gr.Column(scale=5, elem_id="result-card"):
            gr.Markdown("## 📌 AI Analysis Result")

            output_text = gr.Markdown()

            gr.Markdown("## 📚 Open Library Results")

            output_table = gr.Dataframe(
                label="Matched Books",
                wrap=True,
                interactive=False
            )

            gr.Markdown("## ⏱️ API and Processing Time Analysis")

            timing_table = gr.Dataframe(
                label="Timing Summary",
                wrap=True,
                interactive=False
            )

            gr.Markdown("## 💾 Saved CSV File")

            csv_output = gr.File(
                label="Download / View Saved CSV File"
            )

    gr.HTML(
        """
        <div id="footer-note">
            Developed by Partha Pratim Ray (parthapratimray1986@gmail.com) for research demonstration | Image-to-Library Retrieval using OpenAI Vision Models and Open Library API
        </div>
        """
    )

    submit_button.click(
        fn=process_image,
        inputs=image_input,
        outputs=[output_text, output_table, timing_table, csv_output],
    )

demo.launch(share=True, debug=False)
