import re
def chunk_staff(text, size=1000):
    chunks = []
    current = []
    faculty = ""
    department = ""

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("=== FACULTY"):
            if current:
                chunks.append("\n".join(current))

            faculty = line
            department = ""
            current = [faculty]
            continue

        if line.startswith("Department:"):
            department = line

        if current and len("\n".join(current + [line])) > size:
            chunks.append("\n".join(current))
            current = []

            if faculty:
                current.append(faculty)

            if department and department != line:
                current.append(department)

        current.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks



def chunk_majors(text):
    chunks = []
    faculty = ""
    degree = ""
    record = []

    def save_record():
        if record:
            chunks.append("\n".join(
                [faculty, degree] + record
            ))

    for line in text.splitlines():
        line = line.strip()

        if not line or set(line) == {"="}:
            continue

        if line.startswith("Faculty of "):
            save_record()
            record = []
            faculty = line

        elif line.startswith(("BACHELOR PROGRAMS", "DIPLOMA PROGRAMS")):
            save_record()
            record = []
            degree = line

        elif line.startswith("Program |"):
            save_record()
            record = [line]

        elif record:
            record.append(line)

    save_record()
    return chunks



def chunk_calendar(text):
    chunks = []
    semester = ""
    event = []

    def save_event():
        if event:
            chunks.append("\n".join([semester] + event))

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if not paragraph or paragraph == "---":
            continue

        if paragraph.startswith("## ") and "SEMESTER" in paragraph:
            save_event()
            event = []
            semester = paragraph
            continue

        if paragraph.startswith("**") and " | " in paragraph:
            save_event()
            event = [paragraph]
        elif event:
            event.append(paragraph)

    save_event()
    return chunks



def chunk_sections(text, size=1500, overlap=1):
    chunks = []
    current = []
    heading = ""

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip() and p.strip() != "---"
    ]

    def save_chunk():
        if current:
            chunks.append("\n\n".join(current))

    for paragraph in paragraphs:
        if paragraph.startswith("## "):
            save_chunk()
            heading = paragraph.splitlines()[0]
            current = [paragraph]
            continue

        if current and len("\n\n".join(current + [paragraph])) > size:
            save_chunk()

            previous = [
                p for p in current
                if p != heading
            ]

            current = [heading] if heading else []

            if overlap > 0:
                current.extend(previous[-overlap:])

        current.append(paragraph)

    save_chunk()

    return chunks


def chunk_announcements(text):
    chunks = []
    current = []
    header = []

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## CURRENT-ANNOUNCEMENT RESPONSE RULES"):
            break

        if not line:
            continue

        if line.startswith("## ANNOUNCEMENT"):
            if current:
                chunks.append("\n".join(current))

            current = header.copy()
            current.append(line)
            continue

        if current:
            current.append(line)
        else:
            header.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks



def chunk_scholarships(text):
    chunks = []
    current = []
    section = ""
    intro = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or line == "---":
            continue

        if re.match(r"^=== 9\.", line):
            break

        if re.match(r"^=== \d+\.", line):
            if current:
                chunks.append("\n".join(current))

            section = line
            current = [section]
            continue

        is_exemption = (
            section.startswith(("=== 2.", "=== 3."))
            and line.endswith(":")
            and " | " in line
            and "source" not in line.lower()
        )

        if is_exemption and len(current) > 1:
            chunks.append("\n".join(current))
            current = [section]

        if section:
            current.append(line)
        else:
            intro.append(line)

    if intro:
        chunks.insert(0, "\n".join(intro))

    if current:
        chunks.append("\n".join(current))

    return chunks



def chunk_training(text):
    chunks = []
    current = []
    section = ""

    def save_chunk():
        if current:
            chunks.append("\n".join(current))

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or line == "---":
            continue

        if line.startswith("=== 10. UNIGUIDE AI RESPONSE NOTES"):
            break

        if re.match(r"^=== \d+\.", line):
            save_chunk()
            section = line
            current = [line]
            continue

        if re.match(r"^PROGRAM \d+", line):
            save_chunk()
            current = [section, line] if section else [line]
            continue

        if line.startswith("OTHER TULKARM PROGRAMS"):
            save_chunk()
            current = [section, line] if section else [line]
            continue

        current.append(line)

    save_chunk()

    return chunks

def chunk_by_sections(text):
    chunks = []
    current = []
    heading = ""

    def save_chunk():
        if current:
            chunks.append("\n".join(current).strip())

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or line == "---":
            continue

        is_heading = (
            re.match(r"^## \d+\.", line)
            or re.match(r"^=== \d+\.", line)
        )

        if is_heading:
            if "UNIGUIDE" in line.upper():
                break

            save_chunk()
            heading = line
            current = [heading]
        else:
            current.append(line)

    save_chunk()

    return chunks

def chunk_academic_details(name, text):
    sections = chunk_by_sections(text)
    result = []

    for section in sections:
        if (
            name == "academic_regulations.txt"
            and section.startswith("=== 1. ACADEMIC GRADES")
        ):
            headings = [
                "Cumulative Average (Cumulative GPA)",
                "Semester Average",
                "Weighted GPA Calculation",
                "Pass/Fail Courses",
                "Bachelor's Degree Grade Categories",
                "Intermediate Diploma Grade Categories"
            ]

            lines = section.splitlines()
            title = lines[0]
            source_lines = [
                line for line in lines
                if line.startswith(("Source:", "Terminology:"))
            ]

            current = []

            for line in lines[1:]:
                if line.startswith(("Source:", "Terminology:")):
                    continue

                if any(line.startswith(h) for h in headings):
                    if current:
                        result.append(
                            "\n".join([title] + current + source_lines)
                        )
                    current = [line]
                else:
                    current.append(line)

            if current:
                result.append(
                    "\n".join([title] + current + source_lines)
                )

        elif (
            name == "registration.txt"
            and section.startswith("## 6. ACADEMIC COURSE LOAD")
        ):
            marker = "**Summer Semester | الفصل الصيفي**"

            if marker in section:
                before, after = section.split(marker, 1)
                title = section.splitlines()[0]

                result.append(before.strip())
                result.append(
                    title + "\n" + marker + after
                )
            else:
                result.append(section)

        else:
            result.append(section)

    return result



def chunk_document(name, text):
    if name == "academic_staff.txt":
        return chunk_staff(text)

    elif name == "majors_and_tuition.txt":
        return chunk_majors(text)

    elif name == "academic_calendar.txt":
        return chunk_calendar(text)

    elif name == "announcements.txt":
        return chunk_announcements(text)

    elif name == "scholarships_and_loans.txt":
        return chunk_scholarships(text)

    elif name == "practical_training.txt":
        return chunk_training(text)

    elif name in (
        "registration.txt",
        "academic_regulations.txt",
        "student_services.txt",
        "university_contacts.txt"
    ):
        return chunk_academic_details(name, text)

    else:
        raise ValueError(f"Unknown document: {name}")
