import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from chunking import chunk_document
import re
load_dotenv()
def load_docs(folder):
    docs = {}

    for f in Path(folder).glob("*.txt"):
        docs[f.name] = f.read_text(encoding="utf-8")

    return docs



docs = load_docs("documents")

client = chromadb.Client()
col = client.create_collection("docs")

SOURCE_TITLES = {
    "academic_calendar.txt": "PTUK Academic Calendar",
    "academic_regulations.txt": "PTUK Academic Regulations",
    "academic_staff.txt": "PTUK Academic Staff",
    "announcements.txt": "PTUK University Announcements",
    "majors_and_tuition.txt": "PTUK Programs and Tuition",
    "practical_training.txt": "PTUK Practical Training Information",
    "registration.txt": "PTUK Registration Information",
    "scholarships_and_loans.txt": "PTUK Scholarships and Loans",
    "student_services.txt": "PTUK Student Services",
    "university_contacts.txt": "PTUK University Contacts"
}

for name, text in docs.items():
    parts = chunk_document(name, text)

    ids = [f"{name}-{i}" for i in range(len(parts))]
    metadatas = [
    {
        "source": name,
        "title": SOURCE_TITLES.get(name, name)
    }
    for _ in parts
    ]

    if parts:
        col.add(
            ids=ids,
            documents=parts,
            metadatas=metadatas
        )

print("Total chunks stored:", col.count())



#print("Files loaded:", len(docs))
#print("Chunks stored:", col.count())


def retrieve(question, k=10):
    res = col.query(
        query_texts=[question],
        n_results=k
    )

    return list(zip(
        res["documents"][0],
        res["metadatas"][0]
    ))


def expand_query(question):
    synonyms = {
        "deadline": ["last day", "final date"],
        "start": ["begins", "first day"],
        "begin": ["starts", "first day"],
        "tuition": ["fees", "cost"],
        "requirements": ["conditions", "eligibility"],
        "major": ["program", "specialization"]
    }

    words = re.findall(r"[a-z0-9]+", question.lower())

    extra_terms = []

    for word in words:
        if word in synonyms:
            extra_terms.extend(synonyms[word])

    if extra_terms:
        return question + " " + " ".join(extra_terms)

    return question


def retrieve_reranked(question, k=3):
    expanded_question = expand_query(question)
    hits = retrieve(expanded_question, k=30)

    words = re.findall(r"[a-z0-9]+", expanded_question.lower())

    stopwords = {
        "what", "where", "when", "how", "many",
        "much", "the", "is", "are", "for",
        "of", "in", "to", "do", "i", "can",
        "my", "a", "an"
    }

    keywords = [w for w in words if w not in stopwords]

    phrases = []

    for n in (2, 3):
        for i in range(len(keywords) - n + 1):
            phrases.append(" ".join(keywords[i:i+n]))

    scored = []

    for rank, (text, metadata) in enumerate(hits):
        normalized = " ".join(
            re.findall(r"[a-z0-9]+", text.lower())
        )

        text_words = set(normalized.split())

        score = sum(
            1 for word in keywords
            if word in text_words
        )

        score += sum(
            5 for phrase in phrases
            if phrase in normalized
        )

        scored.append((score, rank, text, metadata))

    scored.sort(key=lambda item: (-item[0], item[1]))

    return [
        (text, metadata)
        for score, rank, text, metadata in scored[:k]
    ]



def build_prompt(question, hits):
    context = "\n\n".join(
        f"[Source: {m['source']}]\n{d}"
        for d, m in hits
    )

    return f"""
You are UniGuide AI, a university assistant for
Palestine Technical University - Kadoorie (PTUK),
Tulkarm Main Campus.

Your job is to help students understand university
information using ONLY the provided context.

RULES:

1. Answer in English only.

2. Use ONLY information from the provided context.
   Never invent dates, fees, policies, requirements,
   or contact details.

3. CLARIFICATION IS REQUIRED:
   If essential information is missing and different
   answers apply to different cases, ask ONE short
   clarification question BEFORE providing an answer.

   Examples:
   - Add/drop dates without a semester:
     Ask which semester and academic year.
   - Training hours without a major:
     Ask for the student's degree program and major.

4. When clarification is required:
   - Do NOT list possible answers.
   - Do NOT provide examples from other programs.
   - Do NOT guess missing details.
   - Return ONLY the clarification question.

5. If the question is already clear,
   answer it directly without asking
   unnecessary clarification questions.

6. If the context does not contain enough
   information to answer, clearly say that
   the information is not available in
   the provided university sources.

7. Keep answers clear, accurate, and concise.
   Include relevant conditions when needed.
   
8. If the student's question is unrelated to PTUK
   or university academic services, respond with
   exactly this single token:

   OUT_OF_SCOPE

9. If the question is about PTUK but the provided
   context lacks the answer, explain that the
   information is unavailable. Do not use
   OUT_OF_SCOPE for these questions.


CONTEXT:
{context}

STUDENT QUESTION:
{question}

RESPONSE:
"""


ai = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

def llm(prompt):
    reply = ai.chat.completions.create(
        model="recursive/flint-v1.0:free",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    print("Model used:", reply.model)
    print("Finish reason:", reply.choices[0].finish_reason)
    return reply.choices[0].message.content



def rewrite_question(question, history):
    if not history:
        return question

    recent_history = history[-6:]
    conversation = []

    for message in recent_history:
        if isinstance(message, dict):
            role = message.get("role", "user")
            content = message.get("content", "")

            if isinstance(content, str):
                conversation.append(f"{role}: {content}")

            elif isinstance(content, list):
                text_parts = [
                    part["text"]
                    for part in content
                    if isinstance(part, dict)
                    and isinstance(part.get("text"), str)
                ]

                if text_parts:
                    conversation.append(
                        f"{role}: {' '.join(text_parts)}"
                    )

        elif isinstance(message, (list, tuple)) and len(message) == 2:
            user_message, assistant_message = message
            conversation.append(f"user: {user_message}")
            conversation.append(f"assistant: {assistant_message}")

    conversation_text = "\n".join(conversation)

    prompt = f"""
You rewrite follow-up questions for a university
RAG assistant.

Use the conversation history to understand what
the student's latest message refers to.

RULES:
1. Rewrite the latest question as a complete,
   standalone English question.
2. Preserve the student's original intention.
3. Use relevant details from the conversation.
4. Do not invent missing information.
5. If the latest question is already standalone,
   return it unchanged.
6. Do not answer the question.
7. Return ONLY the rewritten question.

EXAMPLE:
History:
user: When is the first semester add/drop period for 2026/2027?
assistant: September 13–17, 2026.

Latest message:
And what about summer?

Standalone question:
When is the add/drop period for the summer semester of 2026/2027?

CONVERSATION HISTORY:
{conversation_text}

LATEST STUDENT MESSAGE:
{question}

STANDALONE QUESTION:
"""

    rewritten = llm(prompt)

    if not isinstance(rewritten, str) or not rewritten.strip():
        return question

    return rewritten.strip()




def ask(question):
    hits = retrieve_reranked(question)

    if not hits:
        return (
            "I couldn't find relevant university information.",
            []
        )

    answer = llm(build_prompt(question, hits))

    if not isinstance(answer, str) or not answer.strip():
        return (
            "I couldn't generate an answer right now.",
            []
        )

    answer = answer.strip()

    if answer == "OUT_OF_SCOPE":
        return (
            "I'm UniGuide AI, an academic assistant for PTUK. "
            "I can help you with university-related questions!",
            []
        )

    sources = list(dict.fromkeys(
        m["title"] for _, m in hits
    ))

    return answer, sources



if __name__ == "__main__":
    questions = [
    "When is the add/drop period for the first semester of 2026/2027?"
    ]

    for question in questions:
        answer, sources = ask(question)

        print("\n" + "=" * 60)
        print("Question:", question)
        print("Answer:", answer)
        print("Sources:", sources)

