from pymongo import MongoClient
import logging
import os
import re

# ---------------- GRADE POINT MAP ---------------- #

GRADE_POINTS = {
    "S": 10,
    "A+": 9.0,
    "A": 8.5,
    "B+": 8.0,
    "B": 7.5,
    "C+": 7.0,
    "C": 6.5,
    "D": 6.0,
    "P": 5.5,
    "PASS": 5.5,
    "F": 0.0,
    "FAIL": 0.0,
    "FE": 0.0,
    "I": 0.0,
    "ABSENT": 0.0,
    "WITHHELD": 0.0,
    "TBP": 0.0
}

# ---------------- GRADE CONVERSION ---------------- #

def convert_grade_to_points(value):
    """
    Always returns a float.
    Unknown / missing / special values -> 0.0
    """
    if value is None:
        return 0.0

    value_str = str(value).strip().upper()
    return float(GRADE_POINTS.get(value_str, 0.0))


# Use environment variable if available (recommended)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

DB_NAME = "result_analyzer"

logger = logging.getLogger(__name__)


def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]
def get_collection_name(department_name):
    return re.sub(
        r"[^a-z0-9_]",
        "",
        department_name.lower().replace(" ", "_")
    )


# ---------------- SAVE TO MONGODB ---------------- #

def save_structured_records_to_mongodb(students, department_name):
    """
    Saves structured student records (nested subjects) into MongoDB.
    """

    db = get_db()

    collection_name = get_collection_name(department_name)

    collection = db[collection_name]

    # Clear old records
    collection.delete_many({})

    # Insert structured documents directly
    if students:
        collection.insert_many(students)

    logger.info(
        f"Inserted {len(students)} structured records into '{collection_name}'"
    )

    return len(students)
