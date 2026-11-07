# UniGuide AI — PTUK Edition 🎓

An AI-powered academic assistant for **Palestine Technical University – Kadoorie (PTUK)**, Tulkarm Main Campus, built using **Retrieval-Augmented Generation (RAG)**.

UniGuide AI helps students find academic information through a conversational interface, using a curated collection of university-related documents.

> **Disclaimer:** UniGuide AI is an independent educational prototype and is not an official PTUK service. Information should be verified through official university channels when important decisions are involved.

## Features

- **Academic Question Answering:** Answers questions about calendars, registration, regulations, tuition, scholarships, practical training, and student services.
- **Semantic Search:** Uses ChromaDB to retrieve relevant document chunks.
- **Document-Specific Chunking:** Splits different types of university documents using tailored chunking strategies.
- **Keyword Reranking:** Improves retrieval relevance using keyword and phrase matching.
- **Query Expansion:** Adds related search expressions to improve information retrieval.
- **Conversation Context:** Rewrites follow-up questions using recent chat history before retrieving documents.
- **Grounded Answers:** Instructs the language model to use only retrieved context and acknowledge missing information.
- **Source Display:** Shows readable titles for retrieved documents.
- **Interactive Chat Interface:** Uses Gradio for a conversational user experience.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Application development |
| ChromaDB | Vector storage and semantic retrieval |
| OpenRouter API | Access to a language model |
| Gradio | Web-based chatbot interface |
| python-dotenv | Environment variable management |
| Git & GitHub | Version control and project hosting |

## System Architecture

```text
University Documents
        |
        v
Document-Specific Chunking
        |
        v
ChromaDB Vector Collection
        |
        |
Student Question + Chat History
        |
        v
Question Rewriting (LLM)
        |
        v
Semantic Retrieval
        |
        v
Query Expansion + Reranking
        |
        v
Relevant Document Chunks
        |
        v
Prompt Construction
        |
        v
OpenRouter LLM
        |
        v
Answer + Retrieved Source Titles
        |
        v
Gradio Chat Interface
```

*The diagram summarizes the processing stages. Query expansion is applied during the retrieval process.*

## Knowledge Base

The current knowledge base contains **10 text documents**, organized into **247 chunks**.

| Document | Content |
|---|---|
| `academic_calendar.txt` | Academic dates and examinations |
| `academic_regulations.txt` | Academic regulations and GPA |
| `academic_staff.txt` | Academic staff information |
| `announcements.txt` | University announcements |
| `majors_and_tuition.txt` | Academic programs and tuition |
| `practical_training.txt` | Practical training requirements |
| `registration.txt` | Registration and withdrawal procedures |
| `scholarships_and_loans.txt` | Scholarships and tuition exemptions |
| `student_services.txt` | Student support services |
| `university_contacts.txt` | University contact information |

The knowledge base includes information with different verification levels. Some information is student-provided and has not been independently verified.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sadeel-Qashoa/uniguide-rag.git
cd uniguide-rag
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows (Git Bash):

```bash
source .venv/Scripts/activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the API key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do not commit actual API keys to GitHub.

## Run the Application

```bash
python app.py
```

Open the local URL displayed in the terminal.

The application loads its document collection and prepares the ChromaDB index during startup.

## Example Questions

- When is the first semester add/drop period for 2026/2027?
- How do I calculate my cumulative GPA?
- What is the sibling tuition discount percentage?
- How many practical training hours are required for Computer Systems Engineering?
- When is the deadline for first semester late course withdrawal?

### Conversation Example

**Student:** When is the first semester add/drop period for 2026/2027?

**UniGuide:** September 13–17, 2026.

**Student:** And what about summer?

**UniGuide:** The summer semester add/drop period is June 21–23, 2027.

This example demonstrates context-aware follow-up question rewriting.

## Evaluation

Initial tests were conducted on a small, curated evaluation set.

### Retrieval Evaluation

| Metric | Result |
|---|---|
| Hit Rate@1 | 80% (8/10) |
| Hit Rate@3 | 100% (10/10) |
| Hit Rate@5 | 100% (10/10) |

These results describe retrieval performance on ten test questions only and should not be interpreted as overall system accuracy.

### Answer Evaluation

- **5/5** predefined expected-answer checks passed.
- **3/3** manually reviewed unknown-information responses behaved appropriately in the initial tests.

### Run Tests

```bash
python test_rag.py
python test_answers.py
python test_unknown.py
```

Some tests call the OpenRouter language model and require an API key. Results may vary between runs.

## Project Structure

```text
uniguide-rag/
├── documents/
│   └── 10 university-related text files
├── app.py
├── rag.py
├── chunking.py
├── test.py
├── test_chunking.py
├── test_rag.py
├── test_answers.py
├── test_unknown.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations

- Retrieval and answer quality depend on the available documents.
- University schedules, requirements, and policies may change.
- Not every document or statement has been independently verified.
- Source titles represent retrieved documents and do not provide claim-level citations.
- Conversation context is limited to recent messages within the active session.
- Language model behavior may vary between requests.
- The system currently supports English-language questions and answers.
- The application is a prototype, not a production university information service.

## Future Improvements

- More comprehensive retrieval and answer evaluation.
- Better handling of ambiguous questions.
- Verified source links and claim-level citations.
- Improved reliability and API error handling.
- Persistent conversation storage.
- Public deployment and performance optimization.

## Project Purpose

UniGuide AI was developed as a practical AI engineering project to explore **RAG systems, information retrieval, LLM integration, conversational AI, evaluation, and application development**.

The project demonstrates the development of an end-to-end university information assistant, from document processing to an interactive conversational interface.