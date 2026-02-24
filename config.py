MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "result_analyzer"
CREDIT_COLLECTION = "Subject_Grade"

GRADE_TO_POINT = {
    "S": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C+": 5,
    "C": 4,
    "D": 3,
    "P": 2,
    "F": 0,
    "FE": 0,
    "I": 0,
    "WH": 0
}

GRADE_STATUS = {
    "S": "PASSED",
    "A+": "PASSED",
    "A": "PASSED",
    "B+": "PASSED",
    "B": "PASSED",
    "C+": "PASSED",
    "C": "PASSED",
    "D": "PASSED",
    "P": "PASSED",
    "F": "FAILED",
    "FE": "FAILED",
    "I": "FAILED",
    "WH": "WITHHELD"
}
