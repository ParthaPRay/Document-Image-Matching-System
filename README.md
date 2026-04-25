````markdown
# 📚 Document–Image Matching System for Open Library using GPT 5.4

AI-powered **Image → Main Entity Identification → Open Library Book Retrieval** using OpenAI Vision Models and the Open Library API.

Developed by **Partha Pratim Ray**  
📧 parthapratimray1986@gmail.com  
📧 ppray@cus.ac.in

---

## 🚀 Project Overview

This project is an intelligent multimodal retrieval system that accepts an uploaded image and automatically identifies the **single most important searchable entity** from that image (such as a famous person, book title, monument, historical event, scientific concept, cultural object, or academic subject).

The system then converts that entity into a clean bibliographic search query and retrieves the most relevant books from the **Open Library API**, presenting results in a structured tabular format along with detailed API timing analysis.

Additionally, all results are automatically saved into a local `.csv` file for future research analysis, benchmarking, and documentation.

This system is especially useful for:

- Academic demonstrations
- Research prototypes
- Digital library systems
- Educational retrieval systems
- Multimodal search experiments
- AI-assisted bibliographic discovery

Source code reference: :contentReference[oaicite:0]{index=0}

---

# 🔍 Core Workflow

```text
Image Upload
   ↓
Image Encoding (Base64)
   ↓
AI Vision Analysis (GPT-5.4-mini)
   ↓
Main Entity Detection
   ↓
Textual Description Generation
   ↓
Keyword Extraction (GPT-5.4-nano)
   ↓
Bibliographic Query Generation
   ↓
Open Library Search API
   ↓
Book Retrieval
   ↓
Result Display + CSV Logging
````

---

# 🧠 Model Strategy

| Task           | Model/API Used   |
| -------------- | ---------------- |
| Image Analysis | GPT-5.4-mini     |
| Query Cleaning | GPT-5.4-nano     |
| Book Retrieval | Open Library API |
| User Interface | Gradio           |
| Result Storage | CSV + Pandas     |

---

# ✨ Key Features

## 1. Intelligent Image Understanding

Instead of generating generic image descriptions, the system identifies:

* Famous personalities
* Authors
* Historical figures
* Religious figures
* Monuments
* Artworks
* Scientific concepts
* Cultural themes
* Academic subjects
* Book titles
* Recognizable named entities

This significantly improves search quality.

---

## 2. Strict Entity-Based Retrieval

The system avoids vague descriptions such as:

❌ elderly man
❌ black-and-white photo
❌ traditional dress
❌ seated person

and prioritizes:

✅ C. V. Raman
✅ Buddha
✅ White Tiger
✅ Bharatanatyam
✅ Taj Mahal

This improves Open Library matching accuracy.

---

## 3. Structured Open Library Search

Retrieved metadata includes:

* Title
* Author
* First Publish Year
* Edition Count
* Languages
* ISBN
* Open Library Work ID

---

## 4. Automatic CSV Logging

Every processed image is permanently saved in:

```text
image_open_library_results.csv
```

This supports:

* research reproducibility
* performance benchmarking
* large-scale experiments
* longitudinal evaluation

---

## 5. API Performance Benchmarking

The system records:

* Image Encoding Time
* Vision API Time
* Keyword API Time
* Open Library API Time
* Internal Processing Delay
* Total End-to-End Processing Time

This enables system-level performance analysis.

---

# 📦 Required Installation

Install dependencies using:

```bash
pip install openai gradio pandas requests python-dotenv -q
```

---

# 🔐 OpenAI API Setup (Google Colab)

This project is designed for **Google Colab**.

Store your API key securely using:

```python
from google.colab import userdata
```

Add your OpenAI key inside:

```text
Colab Secrets → OPENAI_API_KEY
```

The system automatically loads:

```python
api_key = userdata.get("OPENAI_API_KEY")
```

---

# ▶️ How to Run

## Step 1

Open the notebook in **Google Colab**

---

## Step 2

Install required packages

```bash
pip install openai gradio pandas requests python-dotenv -q
```

---

## Step 3

Add your OpenAI API Key to Colab Secrets

```text
OPENAI_API_KEY
```

---

## Step 4

Run all cells

---

## Step 5

Upload an image and click:

```text
🚀 Analyze Image and Find Books
```

---

## Step 6

View:

* AI Analysis Result
* Open Library Results
* Timing Summary
* Saved CSV File

---

# 📊 Example Output

## Image Analysis

```text
Main Entity: C. V. Raman
Confidence: High
Reason: The portrait closely matches the well-known Indian physicist C. V. Raman in formal attire and turban.
```

---

## Final Open Library Search Query

```text
C. V. Raman
```

---

## Open Library Results

| Title                   | Author  | Year |
| ----------------------- | ------- | ---- |
| The Life of C. V. Raman | Various | 1985 |

---

## Timing Summary

```text
Vision API Time: 1.53 seconds
Keyword API Time: 0.76 seconds
Open Library API Time: 0.41 seconds
Total Processing Time: 2.71 seconds
```

---

# 🎯 Research Significance

This work demonstrates a practical bridge between:

## Computer Vision

and

## Bibliographic Information Retrieval

using lightweight LLM-based semantic reasoning.

It is especially valuable for:

* Digital Humanities
* Smart Libraries
* Educational AI Systems
* Visual Knowledge Retrieval
* AI-powered Cataloguing
* Library Science Automation

---

# 🖥️ Interface Design

The system uses a professionally designed **Gradio Interface** with:

* sober academic color scheme
* structured workflow display
* wide result tables
* clean result visualization
* CSV download support
* professional research presentation aesthetics

Suitable for:

* conferences
* thesis demonstrations
* congress presentations
* research exhibitions

---

# 🔬 Future Improvements

Possible future extensions include:

* multi-book relevance ranking
* PDF retrieval integration
* Google Books API support
* CrossRef API support
* Semantic Scholar integration
* OCR for scanned documents
* multilingual search support
* domain-specific academic retrieval
* local vector database integration
* RAG-based scholarly retrieval

---

# 👨‍💻 Author

## Dr. Partha Pratim Ray

Assistant Professor (Stage II)
Department of Computer Applications
School of Physical Sciences
Sikkim University

Research Areas:

* Internet of AI Things (IoAT)
* Edge Computing
* Large Language Models
* Multimodal Retrieval Systems
* Generative AI
* Pervasive Biomedical Informatics

Recognitions:

* Stanford Top 2% Scientist
* Fellow of IETE
* Senior Member of INAE

---

# 📜 License

This project is developed for:

## Academic Research and Educational Demonstration

Feel free to use, extend, and cite for non-commercial academic purposes.

---

# ⭐ If You Like This Project

Please consider:

* starring the repository
* citing the work
* sharing with researchers
* extending the system for your domain

---

# धन्यवाद

Building intelligent bridges between images and knowledge.

```
```
