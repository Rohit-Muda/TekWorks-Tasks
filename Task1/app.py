import streamlit as st
from mysql import connector
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

def createTable():
    con = connection()
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rollno INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            subject VARCHAR(50) NOT NULL,
            marks INT NOT NULL
        )
    """)

    con.commit()
    cursor.close()
    con.close()

def connection():
    try:
        return connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
    except connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None
    
def collect_info():
    try:
        con=connection()
        cursor=con.cursor()
        if con is None:
            return
        st.title("Student Details")
        name=st.text_input("Enter your name: ")
        rollno=st.number_input("Enter your roll number: ")
        subject=st.radio("Select Subject: ", ["Math", "Science", "English"])
        marks=st.number_input("Enter your marks: ", min_value=0, max_value=100, step=1)
        if st.button("Submit"):
            if name == "" or subject == "" or marks is None:
                st.error("All fields are required.")
                return
            
            cursor.execute("INSERT INTO marks (rollno, name, subject, marks) VALUES (%s, %s, %s, %s)", (rollno, name, subject, marks))
            con.commit()
            st.success("Details submitted successfully.")
    except connection.error as e:
        st.error(f"Error submitting details: {e}")

def view_students():
    try:
        con=connection()
        cursor=con.cursor()
        if con is None:
            return
        st.title("Student Records")

        cursor.execute("SELECT * FROM marks")
        records = cursor.fetchall()

        df = pd.DataFrame(
            records,
            columns=["ID", "ROLL NO", "NAME", "SUBJECT", "MARKS"]
        )

        st.write(df)
    except connection.error as e:
        st.error(f"Error retrieving records: {e}")

def update_student():
    try:
        con=connection()
        cursor=con.cursor()
        if con is None:
            return
        st.title("Update Student Marks")
        rollno=st.number_input("Enter your roll number to update: ")
        
        st.title("update Details ")
        new_name=st.text_input("Enter Update name: ")
        new_subject=st.text_input("Enter Update subject: ")
        new_marks=st.number_input("Enter new marks: ", min_value=0, max_value=100, step=1)
        
        if st.button("Update"):
            cursor.execute("UPDATE marks SET name=%s, subject=%s, marks=%s WHERE rollno=%s", (new_name, new_subject, new_marks, rollno))
            con.commit()
            st.success("Marks updated successfully.")
    except connection.error as e:
        st.error(f"Error updating marks: {e}")

def delete_student():
    try:
        con=connection()
        cursor=con.cursor()
        if con is None:
            return
        st.title("Delete Student Record")
        rollno=st.number_input("Enter your roll number to delete: ")
        
        if st.button("Delete"):
            cursor.execute("DELETE FROM marks WHERE rollno=%s", (rollno,))
            con.commit()
            st.success("Record deleted successfully.")
    except connection.error as e:
        st.error(f"Error deleting record: {e}")

def results_analysis():
    try:
        con = connection()
        cursor = con.cursor()

        if con is None:
            return

        st.title("Results Analysis")
        cursor.execute("SELECT subject, AVG(marks) FROM marks GROUP BY subject")
        records = cursor.fetchall()

        df = pd.DataFrame(
            records,
            columns=["SUBJECT", "AVERAGE MARKS"]
        )

        st.write(df)

    except connector.Error as e:
        st.error(f"Error analyzing results: {e}")



def calculate():
    con = connection()
    cursor = con.cursor()

    st.title("Student Analytics")

    cursor.execute("SELECT name, subject, marks FROM marks")
    data = cursor.fetchall()

    if not data:
        st.write("No data")
        return

    total_marks = 0
    pass_count = 0
    subject_sum = {}
    subject_count = {}
    student_total = {}

    for name, subject, marks in data:
        total_marks += marks

        if marks >= 40:
            pass_count += 1

        subject_sum[subject] = subject_sum.get(subject, 0) + marks
        subject_count[subject] = subject_count.get(subject, 0) + 1

        student_total[name] = student_total.get(name, 0) + marks

    pass_percentage = (pass_count / len(data)) * 100
    top_student = max(student_total, key=student_total.get)

    st.write("Pass Percentage:", round(pass_percentage, 2), "%")
    st.write("Top Scorer:", top_student)

    subjects = list(subject_sum.keys())
    averages = [subject_sum[s] / subject_count[s] for s in subjects]

    st.subheader("Subject vs Average Marks")
    fig1, ax1 = plt.subplots()
    ax1.bar(subjects, averages)
    st.pyplot(fig1)

    st.subheader("Pass / Fail Ratio")
    fig2, ax2 = plt.subplots()
    ax2.pie(
        [pass_count, len(data) - pass_count],
        labels=["Pass", "Fail"],
        autopct="%1.1f%%"
    )
    st.pyplot(fig2)

    cursor.close()
    con.close()

def main():
    load_dotenv()
    createTable()
    st.title("Student Management System")

    menu = ["Collect Info", "View Students", "Update Student", "Delete Student", "Results Analysis", "Student Analytics"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Collect Info":
        collect_info()
    elif choice == "View Students":
        view_students()
    elif choice == "Update Student":
        update_student()
    elif choice == "Delete Student":
        delete_student()
    elif choice == "Results Analysis":
        results_analysis()
    elif choice == "Student Analytics":
        calculate()

if __name__ == "__main__":
    main()
