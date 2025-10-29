from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        year = request.form['year']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, course, year_level, email) VALUES (%s, %s, %s, %s)",
                       (name, course, year, email))
        conn.commit()
        conn.close()

        return redirect('/view')
    return render_template('add_student.html')

@app.route('/view')
def view_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('view_students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
