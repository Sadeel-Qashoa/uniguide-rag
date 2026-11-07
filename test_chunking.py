from pathlib import Path
from chunking import chunk_academic_details

for name in [
    "academic_regulations.txt",
    "registration.txt"
]:
    text = Path("documents", name).read_text(encoding="utf-8")
    parts = chunk_academic_details(name, text)

    print(f"\n{name}: {len(parts)} chunks")

    for i, part in enumerate(parts, 1):
        print(
            f"Chunk {i}: {len(part)} characters | "
            f"{part.splitlines()[0][:75]}"
        )





