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
Copyright (c) 2024 Partha Pratim Ray

Permission is hereby granted, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal or academic purposes only, subject to the following conditions:

1. **Commercial Use**:
   This Software is licensed for commercial use only under explicit written permission and a fee agreed upon with the author, Partha Pratim Ray. Unauthorized commercial use, including but not limited to distribution, sublicensing, or monetization of this Software or any derivative works, is strictly prohibited and subject to legal action.

2. **Restrictions**:
   - The Software shall not be used for any unlawful or unethical purpose.
   - Duplication, replication, or redistribution of the Software, in whole or in part, is prohibited without prior written consent.
   - Modification or removal of any copyright notices is prohibited.

3. **Attribution**:
   - All usage, publications, or projects utilizing this Software must give appropriate credit to the author, Partha Pratim Ray.
   - Include the following attribution statement in any derivative works or research:
     > "This software was developed by Partha Pratim Ray and is used under a commercial license."

4. **Warranty Disclaimer**:
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For licensing inquiries, fees, or permissions, contact:
- Email: parthapratimray1986@gmail.com
- GitHub: [ParthaPRay](http://github.com/ParthaPRay)


