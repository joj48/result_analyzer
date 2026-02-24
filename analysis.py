def add_ranking(db, student_collection_name):

    collection = db[student_collection_name]

    students = list(collection.find().sort("CGPA", -1))

    rank = 1
    for student in students:
        collection.update_one(
            {"_id": student["_id"]},
            {"$set": {"Rank": rank}}
        )
        rank += 1


def get_pass_percentage(db, student_collection_name):

    collection = db[student_collection_name]

    total = collection.count_documents({})
    passed = collection.count_documents({"CGPA": {"$gt": 0}})

    if total == 0:
        return 0

    return round((passed / total) * 100, 2)


def get_department_average(db, student_collection_name):

    collection = db[student_collection_name]

    pipeline = [
        {"$group": {"_id": None, "avg_cgpa": {"$avg": "$CGPA"}}}
    ]

    result = list(collection.aggregate(pipeline))

    if result:
        return round(result[0]["avg_cgpa"], 2)

    return 0
