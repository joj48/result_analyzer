import pdfplumber
import re
import logging
import os
from datetime import datetime
from config import GRADE_TO_POINT, GRADE_STATUS

# ---------------- LOGGING SETUP ---------------- #

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(LOG_DIR, log_filename)

logging.basicConfig(
    filename=log_path,
    filemode="w",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

logger.info("Core parser initialized")


# ---------------- REGEX PATTERNS ---------------- #

DEPT_PATTERN = re.compile(
    r"(.+?)\s*ENGINEERING\s*\[Full Time\]",
    re.IGNORECASE
)

REG_NO_PATTERN = re.compile(
    r"^[A-Z]+\d{2}[A-Z]{2}\d{3}"
)

GRADE_PATTERN = re.compile(
    r"([A-Z]{3}\d{3})\s*\(([^)]+)\)"
)

IGNORE_KEYWORDS = [
    "APJ ABDUL KALAM",
    "Thiruvananthapuram",
    "Exam Centre",
    "Course Code",
    "To Be Published",
    "Register No",
    "The following table",
    "Page"
]




# ---------------- HELPERS ---------------- #

def clean_text(text: str) -> str:
    return " ".join(text.split())


# ---------------- PASS 1 ---------------- #

def get_available_departments(pdf_path: str):
    logger.info(f"Scanning PDF for departments: {pdf_path}")
    departments = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                logger.warning(f"Empty text on page {page_no}")
                continue

            for line in text.split("\n"):
                match = DEPT_PATTERN.search(line)
                if match:
                    dept = match.group(1).strip().upper() + " ENGINEERING"
                    if dept not in departments:
                        departments.append(dept)
                        logger.info(f"Department detected: {dept}")

    logger.info(f"Total departments found: {len(departments)}")
    return departments


# ---------------- PASS 2 ---------------- #

def extract_raw_lines_for_dept(pdf_path: str, target_dept_name: str):
    logger.info(f"Starting extraction for department: {target_dept_name}")

    extracted_data = []
    extracting = False
    current_reg_no = None
    current_grades = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                logger.warning(f"Empty text on page {page_no}")
                continue

            for line in text.split("\n"):
                line = line.strip()
                if not line:
                    continue

                dept_match = DEPT_PATTERN.search(line)
                if dept_match:
                    found = dept_match.group(1).strip().upper() + " ENGINEERING"

                    if extracting:
                        if current_reg_no:
                            extracted_data.append(
                                (current_reg_no, clean_text(" ".join(current_grades)))
                            )
                            logger.info(f"Final student saved: {current_reg_no}")
                        logger.info("Next department reached. Stopping extraction.")
                        return extracted_data

                    if found == target_dept_name:
                        extracting = True
                        logger.info(f"Entered department section: {found}")
                    continue

                if not extracting:
                    continue

                reg_match = REG_NO_PATTERN.match(line)
                if reg_match:
                    if current_reg_no:
                        extracted_data.append(
                            (current_reg_no, clean_text(" ".join(current_grades)))
                        )
                        logger.info(f"Student parsed: {current_reg_no}")

                    current_reg_no = reg_match.group(0)
                    current_grades = []

                    rest = line[len(current_reg_no):].strip()
                    rest = rest.lstrip(",").lstrip('"').strip()
                    if rest:
                        current_grades.append(rest)

                elif current_reg_no:
                    if not any(k.lower() in line.lower() for k in IGNORE_KEYWORDS):
                        current_grades.append(line)

        if extracting and current_reg_no:
            extracted_data.append(
                (current_reg_no, clean_text(" ".join(current_grades)))
            )
            logger.info(f"Last student saved: {current_reg_no}")

    logger.info(f"Total students extracted: {len(extracted_data)}")
    return extracted_data


# ---------------- PASS 3 ---------------- #

def create_matrix_data(raw_data):
    logger.info("Creating structured student data")

    parsed_students = []
    all_subjects = set()

    for reg_no, text_blob in raw_data:

        student = {
            "reg_no": reg_no,
            "subjects": {}
        }

        matches = GRADE_PATTERN.findall(text_blob)

        for subject, grade in matches:

            grade = grade.strip()

            student["subjects"][subject] = {
                "grade": grade,
                "grade_point": GRADE_TO_POINT.get(grade, 0),
                "status": GRADE_STATUS.get(grade, "UNKNOWN")
            }

            all_subjects.add(subject)

        parsed_students.append(student)

    logger.info(
        f"Structured data created for {len(parsed_students)} students "
        f"with {len(all_subjects)} subjects"
    )

    return sorted(all_subjects), parsed_students