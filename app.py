from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- Sample Data (email added) ---
students = [
    {"id": 1, "name": "Riza Sampiano", "email": "riza@student.com", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "John Dela Cruz", "email": "john@student.com", "grade": 11, "section": "Matthew"}
]

# --- HTML Templates ---
home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management System</title>
    <style>
        body {
            background: linear-gradient(to bottom right, #ffe5b4, #ffd4a3);
            font-family: 'Poppins', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fffaf3;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            width: 320px;
            padding: 30px;
            text-align: center;
        }
        h2 {
            color: #ff8c42;
            font-size: 1.4rem;
            margin-bottom: 20px;
        }
        input {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            background: #fff5e1;
            font-size: 0.9rem;
            text-align: center;
            outline: none;
        }
        input:focus {
            background: #ffe9c6;
            box-shadow: 0 0 5px #ffb26b;
        }
        button {
            width: 90%;
            padding: 10px;
            margin-top: 15px;
            border: none;
            border-radius: 20px;
            background: linear-gradient(to right, #ff9a3c, #ffb26b);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            transform: scale(1.05);
            background: linear-gradient(to right, #ffb26b, #ff9a3c);
        }
        .note {
            font-size: 0.8rem;
            color: #5c4033;
            margin-top: 15px;
        }
        .error {
            color: red;
            font-size: 0.85rem;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Management System</h2>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
        <form action="/login" method="POST">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email Address" required>
            <button type="submit">Login</button>
        </form>
        <p class="note">🍑 Use admin@school.com to log in as admin.</p>
    </div>
</body>
</html>
"""

admin_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <style>
        body {
            background: linear-gradient(to bottom right, #ffe5b4, #ffd4a3);
            font-family: 'Poppins', sans-serif;
            padding: 20px;
        }
        h1 { color: #ff8c42; text-align: center; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            border: 1px solid #ffcf99;
            padding: 10px;
            text-align: center;
        }
        th { background-color: #ffe5b4; }
        tr:nth-child(even) { background-color: #fff5e1; }
        .add {
            display: block;
            text-align: center;
            margin: 20px auto;
            background: #ff9a3c;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
        }
        .add:hover { background: #ffb26b; }
    </style>
</head>
<body>
    <h1>Welcome, Admin 👩‍💻</h1>
    <a href="/" class="add">← Logout</a>
    <table>
        <tr>
            <th>ID</th><th>Name</th><th>Email</th><th>Grade</th><th>Section</th>
        </tr>
        {% for s in students %}
        <tr>
            <td>{{ s.id }}</td>
            <td>{{ s.name }}</td>
            <td>{{ s.email }}</td>
            <td>{{ s.grade }}</td>
            <td>{{ s.section }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

student_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Dashboard</title>
    <style>
        body {
            background: linear-gradient(to bottom right, #ffe5b4, #ffd4a3);
            font-family: 'Poppins', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .card {
            background: #fffaf3;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            padding: 30px;
            width: 280px;
            text-align: center;
        }
        h2 { color: #ff8c42; margin-bottom: 10px; }
        p { color: #5c4033; font-size: 0.95rem; }
        a {
            display: inline-block;
            margin-top: 15px;
            text-decoration: none;
            background: #ff9a3c;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
        }
        a:hover { background: #ffb26b; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Welcome, {{ student.name }} 🍑</h2>
        <p><strong>Email:</strong> {{ student.email }}</p>
        <p><strong>Grade:</strong> {{ student.grade }}</p>
        <p><strong>Section:</strong> {{ student.section }}</p>
        <a href="/">Logout</a>
    </div>
</body>
</html>
"""

# --- Routes ---
@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name').strip().lower()
    email = request.form.get('email').strip().lower()

    if email == "admin@school.com":
        return render_template_string(admin_page, students=students)

    student = next((s for s in students if s["name"].lower() == name and s["email"].lower() == email), None)
    if student:
        return render_template_string(student_page, student=student)
    else:
        return render_template_string(home_page, error="No matching student found. Please try again!")

if __name__ == '__main__':
    app.run(debug=True)
