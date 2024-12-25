# Document-Image Matching System

## Overview
The Document-Image Matching System is an advanced application designed to analyze images, extract keywords, and fetch relevant books using cutting-edge AI capabilities. It leverages OpenAI's vision and text APIs, alongside the Open Library API, to deliver accurate and efficient results.

---

## Key Features
1. **AI-Powered Image Analysis**
   - Utilizes an OpenAI vision model to generate textual descriptions from images.
   - Summarizes descriptions into concise keywords.

2. **Open Library Integration**
   - Searches the Open Library database using extracted keywords.
   - Retrieves book details, including titles, authors, and publication years.

3. **Async Processing Pipeline**
   - Efficiently handles asynchronous operations for image analysis and book search.
   - Converts images to base64 for seamless API interaction.

4. **User-Friendly Interface**
   - Developed with Gradio for an interactive, easy-to-use platform.
   - Allows users to upload images and view results directly in the application.

---

## System Workflow
1. **Image Upload**:
   - Users upload an image through the interface.

2. **Image Processing**:
   - The system converts the image to base64 format.
   - The encoded image is analyzed by OpenAI's vision API for descriptive text.

3. **Keyword Extraction**:
   - The descriptive text is summarized into concise keywords.

4. **Book Retrieval**:
   - Extracted keywords are used to query the Open Library API.
   - Relevant book details are fetched and displayed in a tabular format.

5. **Result Presentation**:
   - Keywords and corresponding books are shown in the application for user review.

---

## Requirements
### Environment Setup
- Python 3.8+
- Required libraries:
  - `os`
  - `base64`
  - `requests`
  - `pandas`
  - `gradio`
  - `asyncio`
  - `dotenv`
  - `openai`

### Configuration
1. **API Key Setup**:
   - Create a `.env` file in the project directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_secret_api_key_here
     ```

2. **Dependencies Installation**:
   - Install required libraries using pip:
     ```bash
     pip install -r requirements.txt
     ```

---

## Usage Instructions
1. **Launching the Application**:
   - Run the script using Python:
     ```bash
     python app.py
     ```

2. **Uploading an Image**:
   - Use the Gradio interface to upload an image.

3. **Viewing Results**:
   - Keywords and relevant books are displayed after processing.

---

## License
### Commercial License
**Developed by Partha Pratim Ray**

**Copyright 2024**

This code is licensed for commercial use. Unauthorized use, duplication, or reproduction of this code in any form, including but not limited to research, educational purposes, or commercial applications, without explicit written permission from the author, is strictly prohibited and subject to legal action.

For licensing inquiries, contact:
- **Email**: parthapratimray1986@gmail.com
- **GitHub**: [ParthaPRay](http://github.com/ParthaPRay)

