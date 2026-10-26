from rag import retrieve
from rag import ask
from rag import col

tests = [
    {"q": "When does the first semester add and drop period end?", "has": "2026/09/17"},
    {"q": "When does summer semester registration begin?", "has": "2027/06/18"},
    {"q": "When does the second semester add and drop period end?", "has": "2027/01/28"},
    {"q": "When does late course withdrawal begin in the first semester of 2026/2027?", "has": "2026/09/20"},
    {"q": "Can I change my registered courses in September 2026?", "has": "2026/09/17"}
]

def retrieval_score(k=3):
    found = 0

    for t in tests:
        hits = retrieve(t["q"], k)

        if any(t["has"] in d for d, _ in hits):
            found += 1
        else:
            print("FAIL:", t["q"])

    return found / len(tests)

print("k=1:", retrieval_score(k=1))
print("k=3:", retrieval_score(k=3))

answer_tests = [
    {
        "q": "When does the first semester add and drop period end?",
        "says": "2026/09/17"
    },
    {
        "q": "When does late course withdrawal begin in the first semester of 2026/2027?",
        "says": "2026/09/20"
    },
    {
        "q": "Who won the 2022 World Cup?",
        "says": "know"
    }
]
def run_tests():
    passed = 0

    for t in answer_tests:
        answer, sources = ask(t["q"])

        ok = answer is not None and t["says"].lower() in answer.lower()

        print("PASS" if ok else "FAIL", "-", t["q"])
        print("Answer:", answer)

        passed += ok

    print(passed, "of", len(answer_tests), "passed")

run_tests()

questions = [
    "When does the first semester add and drop period end?",
    "Who won the 2022 World Cup?"
]

for q in questions:
    hits = retrieve(q, k=3)

    print("\nQuestion:", q)
    print("Chunks after filtering:", len(hits))

    answer, sources = ask(q)

    print("Answer:", answer)
    print("Sources:", sources)