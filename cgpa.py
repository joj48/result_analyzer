def load_credit_dict(db, credit_collection_name):
    credit_collection = db[credit_collection_name]
    return {
        doc["Subject Code"]: doc["Credit"]
        for doc in credit_collection.find()
    }


def calculate_student_cgpa(student, credit_dict):

    total_points = 0
    total_credits = 0

    subjects = student.get("subjects", {})

    for subject_code, subject_info in subjects.items():

        grade_point = subject_info.get("grade_point", 0)

        if subject_code in credit_dict:
            credit = credit_dict[subject_code]

            total_points += grade_point * credit
            total_credits += credit

    if total_credits == 0:
        return 0

    return round(total_points / total_credits, 2)


def update_all_cgpa(db, student_collection_name, credit_collection_name):

    student_collection = db[student_collection_name]
    credit_dict = load_credit_dict(db, credit_collection_name)

    for student in student_collection.find():
        cgpa = calculate_student_cgpa(student, credit_dict)

        student_collection.update_one(
            {"_id": student["_id"]},
            {"$set": {"CGPA": cgpa}}
        )
