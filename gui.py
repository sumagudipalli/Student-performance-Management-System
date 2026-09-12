import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


DATABASE = "students.db"


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Student Performance Management System")
root.geometry("1000x650")
root.minsize(900, 600)


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#f4f6f8"
SIDEBAR_COLOR = "#1f2937"
HEADER_COLOR = "#ffffff"
BUTTON_COLOR = "#2563eb"
TEXT_COLOR = "#111827"


root.configure(bg=BG_COLOR)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=80
)

header.pack(
    side="top",
    fill="x"
)

title = tk.Label(
    header,
    text="Student Performance Management System",
    font=("Arial", 22, "bold"),
    bg=HEADER_COLOR,
    fg=TEXT_COLOR
)

title.pack(
    pady=22
)


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR_COLOR,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


sidebar_title = tk.Label(
    sidebar,
    text="MENU",
    font=("Arial", 15, "bold"),
    bg=SIDEBAR_COLOR,
    fg="white"
)

sidebar_title.pack(pady=25)


# =========================================================
# CONTENT AREA
# =========================================================

content = tk.Frame(
    root,
    bg=BG_COLOR
)

content.pack(
    side="left",
    fill="both",
    expand=True
)


# =========================================================
# CLEAR CONTENT
# =========================================================

def clear_content():

    for widget in content.winfo_children():
        widget.destroy()


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    clear_content()

    heading = tk.Label(
        content,
        text="Dashboard",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )

    heading.pack(
        pady=(30, 20)
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marks")
    marks_count = cursor.fetchone()[0]

    connection.close()

    cards_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    cards_frame.pack(
        pady=20
    )

    create_card(
        cards_frame,
        "Total Students",
        student_count,
        0
    )

    create_card(
        cards_frame,
        "Students With Marks",
        marks_count,
        1
    )

    welcome = tk.Label(
        content,
        text="Welcome to your Student Performance Management System",
        font=("Arial", 16),
        bg=BG_COLOR,
        fg="#4b5563"
    )

    welcome.pack(pady=40)


def create_card(parent, title_text, value, column):

    card = tk.Frame(
        parent,
        bg="white",
        width=250,
        height=130,
        relief="solid",
        bd=1
    )

    card.grid(
        row=0,
        column=column,
        padx=15
    )

    card.pack_propagate(False)

    title_label = tk.Label(
        card,
        text=title_text,
        font=("Arial", 13),
        bg="white",
        fg="#6b7280"
    )

    title_label.pack(
        pady=(20, 5)
    )

    value_label = tk.Label(
        card,
        text=str(value),
        font=("Arial", 30, "bold"),
        bg="white",
        fg=BUTTON_COLOR
    )

    value_label.pack()


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    clear_content()

    tk.Label(
        content,
        text="Add Student",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=25)

    form = tk.Frame(
        content,
        bg="white",
        padx=30,
        pady=25
    )

    form.pack()

    fields = [
        "Name",
        "Age",
        "Gender",
        "Course",
        "Branch",
        "Phone",
        "Email"
    ]

    entries = {}

    for row, field in enumerate(fields):

        tk.Label(
            form,
            text=field + ":",
            font=("Arial", 12),
            bg="white"
        ).grid(
            row=row,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        entry = tk.Entry(
            form,
            width=35,
            font=("Arial", 12)
        )

        entry.grid(
            row=row,
            column=1,
            padx=10,
            pady=8
        )

        entries[field] = entry

    def save_student():

        name = entries["Name"].get().strip()
        age = entries["Age"].get().strip()
        gender = entries["Gender"].get().strip()
        course = entries["Course"].get().strip()
        branch = entries["Branch"].get().strip()
        phone = entries["Phone"].get().strip()
        email = entries["Email"].get().strip()

        if not all([
            name,
            age,
            gender,
            course,
            branch,
            phone,
            email
        ]):
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        try:
            age = int(age)

            if age <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter a valid age."
            )

            return

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

        messagebox.showinfo(
            "Success",
            f"Student added successfully!\nStudent ID: {student_id}"
        )

        dashboard()

    tk.Button(
        form,
        text="Save Student",
        command=save_student,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 12, "bold"),
        width=20,
        pady=8
    ).grid(
        row=len(fields),
        column=0,
        columnspan=2,
        pady=20
    )


# =========================================================
# VIEW STUDENTS
# =========================================================

def view_students():

    clear_content()

    tk.Label(
        content,
        text="All Students",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=20)

    table_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "ID",
        "Name",
        "Age",
        "Gender",
        "Course",
        "Branch",
        "Phone",
        "Email"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=100
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=scrollbar.set
    )

    table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            age,
            gender,
            course,
            branch,
            phone,
            email
        FROM students
        ORDER BY id
    """)

    students = cursor.fetchall()

    connection.close()

    for student in students:

        table.insert(
            "",
            "end",
            values=student
        )


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    clear_content()

    tk.Label(
        content,
        text="Search Student",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=25)

    search_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    search_frame.pack()

    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 12)
    )

    search_entry.grid(
        row=0,
        column=0,
        padx=10
    )

    result_label = tk.Label(
        content,
        text="",
        font=("Arial", 13),
        bg=BG_COLOR
    )

    result_label.pack(pady=30)

    def search():

        value = search_entry.get().strip()

        if not value:
            result_label.config(
                text="Enter a student ID or name."
            )
            return

        connection = get_connection()
        cursor = connection.cursor()

        if value.isdigit():

            cursor.execute("""
                SELECT *
                FROM students
                WHERE id = ?
            """, (int(value),))

        else:

            cursor.execute("""
                SELECT *
                FROM students
                WHERE name LIKE ?
            """, (f"%{value}%",))

        students = cursor.fetchall()

        connection.close()

        if not students:

            result_label.config(
                text="No student found."
            )

            return

        text = ""

        for student in students:

            text += (
                f"ID: {student[0]}\n"
                f"Name: {student[1]}\n"
                f"Age: {student[2]}\n"
                f"Gender: {student[3]}\n"
                f"Course: {student[4]}\n"
                f"Branch: {student[5]}\n"
                f"Phone: {student[6]}\n"
                f"Email: {student[7]}\n"
                f"{'-' * 40}\n"
            )

        result_label.config(
            text=text
        )

    tk.Button(
        search_frame,
        text="Search",
        command=search,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20
    ).grid(
        row=0,
        column=1
    )


# =========================================================
# VIEW PERFORMANCE
# =========================================================

def view_performance():

    clear_content()

    tk.Label(
        content,
        text="Student Performance",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=25)

    search_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    search_frame.pack()

    tk.Label(
        search_frame,
        text="Student ID:",
        font=("Arial", 12),
        bg=BG_COLOR
    ).grid(row=0, column=0, padx=10)

    student_entry = tk.Entry(
        search_frame,
        width=15,
        font=("Arial", 12)
    )

    student_entry.grid(
        row=0,
        column=1,
        padx=10
    )

    result_label = tk.Label(
        content,
        text="",
        font=("Arial", 13),
        bg=BG_COLOR,
        justify="left"
    )

    result_label.pack(pady=30)

    def show_performance():

        try:
            student_id = int(
                student_entry.get()
            )

        except ValueError:

            result_label.config(
                text="Enter a valid student ID."
            )

            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
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

            result_label.config(
                text="Student or marks not found."
            )

            return

        name = result[0]
        course = result[1]
        branch = result[2]

        python_marks = result[3]
        sql_marks = result[4]
        analytics_marks = result[5]
        communication_marks = result[6]

        total = (
            python_marks
            + sql_marks
            + analytics_marks
            + communication_marks
        )

        percentage = total / 400 * 100

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "F"

        status = "PASS" if all(
            mark >= 40
            for mark in [
                python_marks,
                sql_marks,
                analytics_marks,
                communication_marks
            ]
        ) else "FAIL"

        text = (
            f"Name: {name}\n"
            f"Course: {course}\n"
            f"Branch: {branch}\n\n"
            f"Python: {python_marks}\n"
            f"SQL: {sql_marks}\n"
            f"Data Analytics: {analytics_marks}\n"
            f"Communication: {communication_marks}\n\n"
            f"Total: {total}/400\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"Result: {status}"
        )

        result_label.config(
            text=text
        )

    tk.Button(
        search_frame,
        text="View",
        command=show_performance,
        bg=BUTTON_COLOR,
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20
    ).grid(
        row=0,
        column=2,
        padx=10
    )


# =========================================================
# SIDEBAR BUTTON
# =========================================================

def menu_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=SIDEBAR_COLOR,
        fg="white",
        activebackground=BUTTON_COLOR,
        activeforeground="white",
        border=0,
        font=("Arial", 12),
        anchor="w",
        padx=25,
        pady=12
    )

    button.pack(
        fill="x"
    )


menu_button("🏠  Dashboard", dashboard)
menu_button("➕  Add Student", add_student)
menu_button("👨‍🎓  View Students", view_students)
menu_button("🔍  Search Student", search_student)
menu_button("📊  Performance", view_performance)


# =========================================================
# EXIT BUTTON
# =========================================================

def exit_application():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()


menu_button("❌  Exit", exit_application)


# =========================================================
# START
# =========================================================

dashboard()

root.mainloop()