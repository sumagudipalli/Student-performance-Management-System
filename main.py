import sqlite3


# =========================================================
# DATABASE CONNECTION
# =========================================================

DATABASE = "students.db"


def get_connection():
    return sqlite3.connect(DATABASE)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            branch TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Marks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            python REAL NOT NULL,
            sql REAL NOT NULL,
            data_analytics REAL NOT NULL,
            communication REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# VALIDATE MARKS
# =========================================================

def get_mark(subject):

    while True:

        try:
            mark = float(input(f"Enter {subject} marks (0-100): "))

            if 0 <= mark <= 100:
                return mark

            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    print("\n" + "=" * 45)
    print("             ADD STUDENT")
    print("=" * 45)

    name = input("Enter student name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter student name: ").strip()

    while True:
        try:
            age = int(input("Enter age: "))

            if age > 0:
                break

            print("Age must be greater than 0.")

        except ValueError:
            print("Please enter a valid age.")

    gender = input("Enter gender: ").strip()
    course = input("Enter course: ").strip()
    branch = input("Enter branch: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, age, gender, course, branch, phone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        course,
        branch,
        phone,
        email
    ))

    connection.commit()

    student_id = cursor.lastrowid

    connection.close()

    print("\nStudent added successfully! ✅")
    print("Student ID:", student_id)


# =========================================================
# VIEW STUDENTS
# =========================================================

def view_students():

    print("\n" + "=" * 45)
    print("             ALL STUDENTS")
    print("=" * 45)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, age, gender, course, branch, phone, email
        FROM students
        ORDER BY id
    """)

    students = cursor.fetchall()

    connection.close()

    if not students:
        print("No students found.")
        return

    for student in students:

        print("\n" + "-" * 45)
        print("ID     :", student[0])
        print("Name   :", student[1])
        print("Age    :", student[2])
        print("Gender :", student[3])
        print("Course :", student[4])
        print("Branch :", student[5])
        print("Phone  :", student[6])
        print("Email  :", student[7])


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    print("\n" + "=" * 45)
    print("             SEARCH STUDENT")
    print("=" * 45)

    search = input("Enter student ID or name: ").strip()

    connection = get_connection()
    cursor = connection.cursor()

    if search.isdigit():

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id = ?
        """, (int(search),))

    else:

        cursor.execute("""
            SELECT *
            FROM students
            WHERE name LIKE ?
        """, (f"%{search}%",))

    students = cursor.fetchall()

    connection.close()

    if not students:

        print("\nNo student found. ❌")
        return

    for student in students:

        print("\n" + "-" * 45)
        print("ID     :", student[0])
        print("Name   :", student[1])
        print("Age    :", student[2])
        print("Gender :", student[3])
        print("Course :", student[4])
        print("Branch :", student[5])
        print("Phone  :", student[6])
        print("Email  :", student[7])


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student():

    print("\n" + "=" * 45)
    print("             UPDATE STUDENT")
    print("=" * 45)

    try:
        student_id = int(input("Enter student ID: "))

    except ValueError:
        print("Please enter a valid ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:

        print("Student not found. ❌")
        connection.close()
        return

    print("\nCurrent student:")
    print("Name:", student[1])

    print("\nEnter new details.")

    name = input("Enter student name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter student name: ").strip()

    while True:

        try:
            age = int(input("Enter age: "))

            if age > 0:
                break

            print("Age must be greater than 0.")

        except ValueError:
            print("Please enter a valid age.")

    gender = input("Enter gender: ").strip()
    course = input("Enter course: ").strip()
    branch = input("Enter branch: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    cursor.execute("""
        UPDATE students
        SET
            name = ?,
            age = ?,
            gender = ?,
            course = ?,
            branch = ?,
            phone = ?,
            email = ?
        WHERE id = ?
    """, (
        name,
        age,
        gender,
        course,
        branch,
        phone,
        email,
        student_id
    ))

    connection.commit()
    connection.close()

    print("\nStudent updated successfully! ✅")


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():

    print("\n" + "=" * 45)
    print("             DELETE STUDENT")
    print("=" * 45)

    try:
        student_id = int(input("Enter student ID: "))

    except ValueError:
        print("Please enter a valid ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:

        print("Student not found. ❌")
        connection.close()
        return

    print("Student:", student[0])

    confirmation = input(
        "Are you sure you want to delete this student? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":

        # Delete marks first
        cursor.execute("""
            DELETE FROM marks
            WHERE student_id = ?
        """, (student_id,))

        # Delete student
        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        connection.commit()

        print("\nStudent deleted successfully! ✅")

    else:

        print("\nDeletion cancelled.")

    connection.close()


# =========================================================
# ADD MARKS
# =========================================================

def add_marks():

    print("\n" + "=" * 45)
    print("               ADD MARKS")
    print("=" * 45)

    try:
        student_id = int(input("Enter student ID: "))

    except ValueError:
        print("Please enter a valid student ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:

        print("Student not found. ❌")
        connection.close()
        return

    print("\nStudent Name:", student[0])

    # Check whether marks already exist
    cursor.execute("""
        SELECT id
        FROM marks
        WHERE student_id = ?
    """, (student_id,))

    existing_marks = cursor.fetchone()

    if existing_marks:

        print("\nMarks already exist for this student.")
        print("Use option 7 to view performance.")

        connection.close()
        return

    print("\nEnter marks:")

    python_marks = get_mark("Python")
    sql_marks = get_mark("SQL")
    analytics_marks = get_mark("Data Analytics")
    communication_marks = get_mark("Communication")

    cursor.execute("""
        INSERT INTO marks
        (student_id, python, sql, data_analytics, communication)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student_id,
        python_marks,
        sql_marks,
        analytics_marks,
        communication_marks
    ))

    connection.commit()
    connection.close()

    print("\nMarks added successfully! ✅")


# =========================================================
# CALCULATE GRADE
# =========================================================

def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"

    elif percentage >= 80:
        return "A"

    elif percentage >= 70:
        return "B"

    elif percentage >= 60:
        return "C"

    elif percentage >= 50:
        return "D"

    else:
        return "F"


# =========================================================
# VIEW PERFORMANCE
# =========================================================

def view_performance():

    print("\n" + "=" * 45)
    print("          STUDENT PERFORMANCE")
    print("=" * 45)

    try:
        student_id = int(input("Enter student ID: "))

    except ValueError:
        print("Please enter a valid student ID.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            students.id,
            students.name,
            students.course,
            students.branch,
            marks.python,
            marks.sql,
            marks.data_analytics,
            marks.communication
        FROM students
        INNER JOIN marks
        ON students.id = marks.student_id
        WHERE students.id = ?
    """, (student_id,))

    result = cursor.fetchone()

    connection.close()

    if not result:

        print("\nStudent or marks not found. ❌")
        return

    student_id = result[0]
    name = result[1]
    course = result[2]
    branch = result[3]

    python_marks = result[4]
    sql_marks = result[5]
    analytics_marks = result[6]
    communication_marks = result[7]

    total = (
        python_marks
        + sql_marks
        + analytics_marks
        + communication_marks
    )

    average = total / 4
    percentage = total / 400 * 100
    grade = calculate_grade(percentage)

    if (
        python_marks >= 40
        and sql_marks >= 40
        and analytics_marks >= 40
        and communication_marks >= 40
    ):
        result_status = "PASS"

    else:
        result_status = "FAIL"

    print("\n" + "-" * 45)
    print("Student ID        :", student_id)
    print("Name              :", name)
    print("Course            :", course)
    print("Branch            :", branch)

    print("\nSubject Marks")
    print("-" * 45)

    print("Python            :", python_marks)
    print("SQL               :", sql_marks)
    print("Data Analytics    :", analytics_marks)
    print("Communication     :", communication_marks)

    print("\n" + "-" * 45)
    print("Total Marks       :", total, "/ 400")
    print("Average           :", round(average, 2))
    print("Percentage        :", round(percentage, 2), "%")
    print("Grade             :", grade)
    print("Result            :", result_status)
    print("-" * 45)


# =========================================================
# ANALYTICS
# =========================================================

def analytics():

    print("\n" + "=" * 45)
    print("                ANALYTICS")
    print("=" * 45)

    connection = get_connection()
    cursor = connection.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    print("\nTotal Students:", total_students)

    if total_students == 0:

        print("No student data available.")
        connection.close()
        return

    # Students with marks
    cursor.execute("""
        SELECT
            students.id,
            students.name,
            marks.python,
            marks.sql,
            marks.data_analytics,
            marks.communication
        FROM students
        INNER JOIN marks
        ON students.id = marks.student_id
    """)

    results = cursor.fetchall()

    if not results:

        print("No marks have been added yet.")
        connection.close()
        return

    # Subject totals
    python_total = 0
    sql_total = 0
    analytics_total = 0
    communication_total = 0

    student_results = []

    for row in results:

        student_id = row[0]
        name = row[1]

        python_marks = row[2]
        sql_marks = row[3]
        analytics_marks = row[4]
        communication_marks = row[5]

        total = (
            python_marks
            + sql_marks
            + analytics_marks
            + communication_marks
        )

        percentage = total / 400 * 100

        python_total += python_marks
        sql_total += sql_marks
        analytics_total += analytics_marks
        communication_total += communication_marks

        student_results.append(
            (student_id, name, total, percentage)
        )

    number_of_students = len(results)

    print("\nStudents With Marks:", number_of_students)

    print("\nSubject-wise Average")
    print("-" * 45)

    print(
        "Python           :",
        round(python_total / number_of_students, 2)
    )

    print(
        "SQL              :",
        round(sql_total / number_of_students, 2)
    )

    print(
        "Data Analytics   :",
        round(analytics_total / number_of_students, 2)
    )

    print(
        "Communication    :",
        round(communication_total / number_of_students, 2)
    )

    # Top student
    top_student = max(
        student_results,
        key=lambda student: student[3]
    )

    print("\nTop Performing Student")
    print("-" * 45)

    print("ID         :", top_student[0])
    print("Name       :", top_student[1])
    print("Total      :", top_student[2], "/ 400")
    print("Percentage :", round(top_student[3], 2), "%")
    print(
        "Grade      :",
        calculate_grade(top_student[3])
    )

    # Pass and fail count
    pass_count = 0
    fail_count = 0

    for result in results:

        marks = result[2:]

        if all(mark >= 40 for mark in marks):
            pass_count += 1

        else:
            fail_count += 1

    print("\nResult Analysis")
    print("-" * 45)
    print("Passed Students :", pass_count)
    print("Failed Students :", fail_count)

    # Grade distribution
    grade_counts = {
        "A+": 0,
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0
    }

    for student in student_results:

        grade = calculate_grade(student[3])

        grade_counts[grade] += 1

    print("\nGrade Distribution")
    print("-" * 45)

    for grade, count in grade_counts.items():

        print(f"{grade:5} : {count}")

    connection.close()


# =========================================================
# MENU
# =========================================================

def show_menu():

    print("\n")
    print("=" * 45)
    print("     STUDENT PERFORMANCE MANAGEMENT")
    print("=" * 45)

    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Add Marks")
    print("7. View Performance")
    print("8. Analytics")
    print("9. Exit")

    print("=" * 45)


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    create_database()

    while True:

        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            add_student()

        elif choice == "2":

            view_students()

        elif choice == "3":

            search_student()

        elif choice == "4":

            update_student()

        elif choice == "5":

            delete_student()

        elif choice == "6":

            add_marks()

        elif choice == "7":

            view_performance()

        elif choice == "8":

            analytics()

        elif choice == "9":

            print("\nThank you for using")
            print("Student Performance Management System! 👋")
            break

        else:

            print("\nInvalid choice.")
            print("Please enter a number from 1 to 9.")


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":
    main()