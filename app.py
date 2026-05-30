import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("student.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll_no TEXT UNIQUE,
    maths INTEGER,
    science INTEGER,
    english INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
)
""")
conn.commit()


# ---------------- GRADE FUNCTION ----------------
def get_grade(per):
    if per >= 80:
        return "A"
    elif per >= 60:
        return "B"
    elif per >= 40:
        return "C"
    else:
        return "F"


# ---------------- UI ----------------
st.title("🎓 Student Result Management System")

menu = st.sidebar.selectbox(
    "Choose Action",
    ["Add Student", "View Students", "Search Student", "Delete Student"]
)

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":
    st.subheader("➕ Add Student")

    name = st.text_input("Name")
    roll = st.text_input("Roll Number")
    maths = st.number_input("Maths", 0, 100)
    science = st.number_input("Science", 0, 100)
    english = st.number_input("English", 0, 100)

    if st.button("Save Student"):
        total = maths + science + english
        per = total / 3
        grade = get_grade(per)

        try:
            cursor.execute("""
            INSERT INTO students VALUES (NULL,?,?,?,?,?,?,?,?)
            """, (name, roll, maths, science, english, total, per, grade))

            conn.commit()
            st.success("Student Added Successfully!")

        except:
            st.error("Roll number already exists!")

# ---------------- VIEW STUDENTS ----------------
elif menu == "View Students":
    st.subheader("📋 All Students")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    for row in data:
        st.write(row)

# ---------------- SEARCH STUDENT ----------------
elif menu == "Search Student":
    st.subheader("🔍 Search Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search"):
        cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll,))
        data = cursor.fetchone()

        if data:
            st.success("Student Found!")
            st.write("ID:", data[0])
            st.write("Name:", data[1])
            st.write("Roll No:", data[2])
            st.write("Maths:", data[3])
            st.write("Science:", data[4])
            st.write("English:", data[5])
            st.write("Total:", data[6])
            st.write("Percentage:", data[7])
            st.write("Grade:", data[8])
        else:
            st.error("Student not found!")

# ---------------- DELETE STUDENT ----------------
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student")

    roll = st.text_input("Enter Roll Number to Delete")

    if st.button("Delete"):
        cursor.execute("DELETE FROM students WHERE roll_no=?", (roll,))
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Student Deleted Successfully!")
        else:
            st.error("Student not found!")