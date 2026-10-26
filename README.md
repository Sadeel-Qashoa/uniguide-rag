# UniGuide AI — PTUK Edition

An AI-powered academic assistant that uses **Retrieval-Augmented Generation (RAG)** to answer questions about Palestine Technical University–Kadoorie (PTUK).

## Features

- Answers questions about academic calendars and registration procedures.
- Retrieves relevant information from university documents.
- Generates answers using an LLM through OpenRouter.
- Displays the source documents used to answer questions.
- Returns "I don't know" when no sufficiently relevant information is retrieved.
- Provides a simple web interface using Gradio.

## Technologies

- Python
- ChromaDB
- OpenRouter API
- Gradio
- Python dotenv

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Sadeel-Qashoa/uniguide-rag.git
cd uniguide-rag
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate it on Windows (Git Bash)**

```bash
source .venv/Scripts/activate
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**5. Configure the API key**

Create a `.env` file in the project directory:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

## Run the Application

```bash
python app.py
```

Open the local Gradio URL displayed in the terminal.

## Example Questions

- When does the first semester add and drop period end?
- When does late course withdrawal begin in the first semester of 2026/2027?
- Can I change my registered courses in September 2026?

## Project Structure

```text
uniguide-rag/
├── documents/
│   ├── academic_calendar.txt
│   └── registration.txt
├── rag.py
├── app.py
├── test.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations

- Answers depend on the documents currently included in the project.
- Academic information may become outdated.
- Ambiguous questions may require clarification.
- The application is a prototype and is not an official PTUK service.

## Project Purpose

Built as a practical RAG learning project in preparation for the IEEE BU National RAG Hackathon 2026.