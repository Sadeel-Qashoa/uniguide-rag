
from rag import ask

questions = [
    "What is the personal phone number of the university president?",
    "What is the exact location of the university medical clinic?",
    "What is the password of the university Wi-Fi network?"
]

for i, question in enumerate(questions, 1):
    answer, sources = ask(question)

    print("\n" + "=" * 50)
    print(f"Test {i}")
    print("Question:", question)
    print("Answer:", answer)
    print("Sources:", sources)
