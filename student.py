from connection import conn
from datetime import datetime
import re
import mysql.connector 




def insert_students_from_df(df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        sql = "INSERT INTO students (name, gender, fathers_name, address, DOB, mobile_number, course_id,Year) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        values = (row['Full_Name'], row['Gender'], row['Father\'s_Name'], row['Address'], row['Date_of_Birth'], row['Mobile Number'], row['course_id'],row['Year'])
        cursor.execute(sql, values)
        conn.commit()

# Insert data into students table

# insert_students_from_df(df)




# Function to add a new student with constraints
def add_student(name, gender, fathers_name, address, date_of_birth, mobile_number, course_id,Year):
    # Check if name and fathers_name contain special characters or numbers
    cursor = conn.cursor()
    if not (name.replace(" ", "").isalpha() and fathers_name.replace(" ", "").isalpha()):
        print("Error: Name and father's name should only contain alphabets.")
        return

    # Check if mobile number starts with +91 and is followed by 10 digits
    if not re.match(r'^\+91\d{10}$', mobile_number):
        print("Error: Mobile number should start with +91 and be followed by 10 digits.")
        return

    # Convert date_of_birth to datetime object
    try:
        date_of_birth = datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    except ValueError:
        print("Error: Date of birth should be in dd-mm-yyyy format.")
        return

    # Set past_course same as course_id
    past_course = course_id

    # Insert SQL query
    sql = "INSERT INTO students (name, gender, fathers_name, address, DOB, mobile_number, course_id, Year, past_course) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (name, gender, fathers_name, address, date_of_birth, mobile_number, course_id, Year, past_course)

    # Execute SQL query
    cursor.execute(sql, values)
    conn.commit()

    print("New student added successfully!")

#add_student("Sanchit Shekhar", "Male", "Janny Depp", "123 Main St", "01-01-2020", "+919876543223", "CS2",'1st')




# Function to update student information with constraints
def update_student_info(student_id, **kwargs):
    cursor = conn.cursor()
    # Check if the student exists
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    if student is None:
        print("Error: Student not found.")
        return

    # Check if 'name' column is included in kwargs
    if 'name' in kwargs:
        print("Error: Name cannot be updated.")
        return

    # Constraints for individual columns
    for key, value in kwargs.items():
        if key == 'fathers_name':
            if not value.replace(" ", "").isalpha():
                print("Error: Father's name should only contain alphabets.")
                return
        elif key == 'DOB':
            try:
                datetime.strptime(value, '%d-%m-%Y')
            except ValueError:
                print("Error: Date of birth should be in dd-mm-yyyy format.")
                return
        elif key == 'mobile_number':
            if not re.match(r'^\+91\d{10}$', value):
                print("Error: Mobile number should start with +91 and be followed by 10 digits.")
                return
        elif key == 'course_id':
            if student[8] != '1st':
                print("Error: Course can be only updated for 1st year students.")
                return

    # Prepare the update query
    update_query = "UPDATE students SET "
    update_values = []
    for key, value in kwargs.items():
        update_query += f"{key} = %s, "
        update_values.append(value)
    if not update_values:
        print("Error: No valid columns to update.")
        return
    update_query = update_query.rstrip(", ") + " WHERE student_id = %s"
    update_values.append(student_id)

    # Execute the update query
    cursor.execute(update_query, update_values)
    conn.commit()
    print("Student information updated successfully!")
# Example:
#update_student_info(student_id=104,fathers_name="New father", DOB="01-01-2010", mobile_number="+919876543210", course_id="CS4")




#Function to list all students based on Course, Year, Gender
def list_students(course=None, year=None, gender=None):
    cursor = conn.cursor()
    # Base SQL query
    sql = "SELECT student_id, name FROM students WHERE 1"

    # Add filters based on parameters
    if course:
        sql += f" AND course_id = '{course}'"
    if year:
        sql += f" AND Year = '{year}'"
    if gender:
        sql += f" AND gender = '{gender}'"

    # Execute SQL query
    cursor.execute(sql)
    students = cursor.fetchall()

    # Print results
    if students:
        print("List of students:")
        for student in students:
            print(f"Student ID: {student[0]}, Name: {student[1]}")
    else:
        print("No students found matching the criteria.")
    
# Example:
#list_students(course = 'CS1',year='1st')  # To list all students



# Function to view specific student details 
def view_student_details(student_id, *columns):
    cursor = conn.cursor()
    # Check if the provided column names are valid
    cursor.execute("SHOW COLUMNS FROM students")
    valid_columns = [column[0] for column in cursor.fetchall()]

    for column in columns:
        if column not in valid_columns:
            print(f"Error: '{column}' column not found.")
            return

    # If no columns specified, fetch all columns
    if not columns:
        columns_str = "name, gender, fathers_name, address, DOB, mobile_number, course_id, Year"
    else:
        # Prepare the list of columns to select
        columns_str = ', '.join(columns)

    # Fetch details for the specified columns and student ID
    cursor.execute(f"SELECT {columns_str} FROM students WHERE student_id = %s AND soft_delete = 0", (student_id,))
    student_details = cursor.fetchone()

    # Print result
    if student_details:
        print("Student Details:")
        for column, value in zip(cursor.column_names, student_details):
            print(f"{column.capitalize()}: {value}")
    else:
        print("No student found with the provided ID.")

# Example:
# view_student_details(102)



def student_past_courses(student_id):
    cursor = conn.cursor()
    # Fetch the student's past course and current course from the database
    cursor.execute("SELECT course_id, past_course FROM students WHERE student_id = %s", (student_id,))
    course_data = cursor.fetchone()

    # Check if the student has past courses and current course
    if course_data:
        course_id, past_course = course_data
        if course_id != past_course:
            print(f"Student has changed course. Past Course: {past_course}")
        else:
            print("Student has not changed course.")
    else:
        print("No student found with the provided ID.")
    
# Example:
#student_past_courses(104)  

# to perform the soft delete:
def delete_student(student_id):
    cursor = conn.cursor()
    try:
        # Update the 'soft_delete' column to 1 for the specified student_id
        cursor.execute("UPDATE students SET soft_delete = 1 WHERE student_id = %s", (student_id,))
        conn.commit()
        print("Student record soft deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    

# Example usage:
#delete_student(103)  # Soft delete student with ID 1
#view_student_details(103)
