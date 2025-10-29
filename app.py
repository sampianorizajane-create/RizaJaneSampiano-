from flask import Flask, jsonify, request

app = Flask(__name__)


# Home route
# -----------------------------
@app.route('/')
def home():
    return "🎓 Welcome to the Student Management System "

# -----------------------------
# Get all students
# -----------------------------
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "count": len(students),
        "students": students
    })

# -----------------------------
# Get a single student by ID
# -----------------------------
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

# -----------------------------
# Add a new student
# -----------------------------
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_id = max([s["id"] for s in students]) + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "age": data.get("age", None),
        "grade": data.get("grade", None),
        "section": data.get("section", None)
    }
    students.append(new_student)
    return jsonify({"message": "Student added successfully!", "student": new_student}), 201

# -----------------------------
# Update existing student
# -----------------------------
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    student.update({
        "name": data.get("name", student["name"]),
        "age": data.get("age", student["age"]),
        "grade": data.get("grade", student["grade"]),
        "section": data.get("section", student["section"])
    })
    return jsonify({"message": "Student updated!", "student": student})

# -----------------------------
# Delete student
# -----------------------------
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": f"Student with ID {student_id} deleted."})

# -----------------------------
# Run server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
  
