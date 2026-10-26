import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
def load_docs(folder):
    docs = {}

    for f in Path(folder).glob("*.txt"):
        docs[f.name] = f.read_text(encoding="utf-8")

    return docs


def chunk(text, size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap

    return chunks

docs = load_docs("documents")
client = chromadb.Client()
col = client.create_collection("docs")

for name, text in docs.items():
    parts = chunk(text)

    for i, c in enumerate(parts):
        col.add(
            ids=[f"{name}-{i}"],
            documents=[c],
            metadatas=[{"source": name}]
        )

def retrieve(question, k=3, max_dist=1.0):
    res = col.query(
        query_texts=[question],
        n_results=k
    )

    rows = zip(
        res["documents"][0],
        res["metadatas"][0],
        res["distances"][0]
    )

    return [
        (d, m)
        for d, m, dist in rows
        if dist <= max_dist
    ]


def build_prompt(question, hits):
    context = "\n\n".join(
        f"[{m['source']}] {d}" for d, m in hits
    )

    return (
        "Answer using ONLY the context below. "
        "If it is not there, say you don't know."
        f"\n\nContext:\n{context}"
        f"\n\nQuestion: {question}"
    )

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

def ask(question):
    hits = retrieve(question)
    if not hits:
        return "I don't know.", []
    answer = llm(build_prompt(question, hits))
    return answer, [m["source"] for _, m in hits]

if __name__ == "__main__":
    question = "Which academic week are we currently in as of October 23, 2026?"
    #"Can I change my registered courses in September 2026?"

    answer, sources = ask(question)
    hits = retrieve(question)
    for i, (text, metadata) in enumerate(hits):
        print(f"\nChunk {i + 1}")
        print("Source:", metadata["source"])
        print("Text:", text)

    print("Answer:", answer)
    print("Sources:", sources)