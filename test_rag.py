from rag import retrieve, retrieve_reranked


tests = [
    {
        "question": "How many practical training hours are required for Computer Systems Engineering?",
        "expected_source": "practical_training.txt",
        "expected_text": "400"
    },
    {
        "question": "What is the sibling tuition discount percentage?",
        "expected_source": "scholarships_and_loans.txt",
        "expected_text": "25%"
    },
    {
        "question": "When are the first semester practical midterm examinations?",
        "expected_source": "academic_calendar.txt",
        "expected_text": "October 25"
    },
    {
        "question": "How do I calculate my cumulative GPA?",
        "expected_source": "academic_regulations.txt",
        "expected_text": "credit hours"
    },
    {
        "question": "Where can I find information about the university medical clinic?",
        "expected_source": "student_services.txt",
        "expected_text": "clinic"
    },
    {
        "question": "When does the summer semester add/drop period start in 2027?",
        "expected_source": "academic_calendar.txt",
        "expected_text": "June 21"
    },
    {
        "question": "What is the deadline for first semester late course withdrawal?",
        "expected_source": "registration.txt",
        "expected_text": "December 10"
    },
    {
        "question": "Where can students access the academic portal?",
        "expected_source": "student_services.txt",
        "expected_text": "edugate.ptuk.edu.ps"
    },
    {
        "question": "What is the tuition fee per credit hour for Computer Systems Engineering?",
        "expected_source": "majors_and_tuition.txt",
        "expected_text": "24 JOD"
    },
    {
        "question": "When does second semester add/drop begin?",
        "expected_source": "academic_calendar.txt",
        "expected_text": "January 24"
    }
]



scores = {1: 0, 3: 0, 5: 0}

for i, test in enumerate(tests, start=1):
    hits = retrieve_reranked(test["question"], k=5)

    matching_ranks = [
        rank
        for rank, (text, metadata) in enumerate(hits, start=1)
        if metadata["source"] == test["expected_source"]
        and test["expected_text"].lower() in text.lower()
    ]

    best_rank = min(matching_ranks) if matching_ranks else None

    for k in scores:
        if best_rank is not None and best_rank <= k:
            scores[k] += 1

    status = "PASS" if best_rank is not None else "FAIL"

    print(f"Test {i}: {status}")
    print("Question:", test["question"])
    print("Best matching rank:", best_rank)
    print()

print("=" * 40)

for k, passed in scores.items():
    percentage = passed / len(tests) * 100
    print(f"Hit Rate@{k}: {percentage:.1f}% ({passed}/{len(tests)})")
