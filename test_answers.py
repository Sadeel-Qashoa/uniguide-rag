
from rag import ask

tests = [
    {
        "question": "How many practical training hours are required for Computer Systems Engineering?",
        "expected": "400"
    },
    {
        "question": "What is the sibling tuition discount percentage?",
        "expected": "25%"
    },
    {
        "question": "When is the deadline for first semester late course withdrawal?",
        "expected": "December 10"
    },
    {
        "question": "When does the second semester add/drop period begin in 2027?",
        "expected": "January 24"
    },
    {
        "question": "When are the first semester practical midterm examinations?",
        "expected": "October 25"
    }
]

passed = 0

for i, test in enumerate(tests, start=1):
    answer, sources = ask(test["question"])

    success = (
        isinstance(answer, str)
        and test["expected"].lower() in answer.lower()
    )

    if success:
        passed += 1

    print("\n" + "=" * 50)
    print(f"Test {i}: {'PASS' if success else 'FAIL'}")
    print("Question:", test["question"])
    print("Answer:", answer)
    print("Sources:", sources)

print("\n" + "=" * 50)
print(f"Answer Checks Passed: {passed}/{len(tests)}")
