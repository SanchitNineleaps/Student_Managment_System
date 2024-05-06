from connection import conn
from datetime import datetime
import mysql.connector 
import re


def add_teacher(name, address, mobile_number, gender, teaching_specialties, date_of_joining):
    cursor = conn.cursor()
    # Check name does not contain special characters or numbers
    if not name.replace(" ", "").isalpha():
        print("Error: Name should only contain alphabets.")
        return
    
    # Check mobile number format
    if not re.match(r'^\+91\d{10}$', mobile_number):
        print("Error: Mobile number should start with +91 and be followed by 10 digits.")
        return
    
    # Check teaching_specialties format
    specialties = teaching_specialties.split(',')
    if len(specialties) == 1:
        print("Error: Teaching specialties should contain more than one value separated by commas.")
        return

    try:
        datetime.strptime(date_of_joining, '%d-%m-%Y')
    except ValueError:
        print("Error: Date of joining should be in dd-mm-yyyy format.")
        return

   
    # Insert new teacher details into the table
    cursor.execute("INSERT INTO teachers (name, address, mobile_number, gender, teaching_specialties, date_of_joining) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (name, address, mobile_number, gender, teaching_specialties, date_of_joining))
    conn.commit()
    print("New teacher added successfully!")

    # Fetch the auto-generated teacher ID
    teacher_id = cursor.lastrowid

    # Insert corresponding data into the subject_allotment table
    cursor.execute("INSERT INTO subject_allotment (teacher_id, teacher_name, teaching_specialization) VALUES (%s, %s, %s)", 
                            (teacher_id, name, teaching_specialties))
    conn.commit()
    print("Corresponding data added to subject_allotment table successfully!")
    
# Example usage:
#add_teacher('John Danny', '123 Main St', '+919876543210', 'Male', 'Math,Physics', '04-02-2023')



def view_teacher_details(teacher_id, *fields):
    cursor = conn.cursor()
    try:
        if fields:
            fields_str = ', '.join(fields) + ', sa.course_allotted'
            sql_query = f"SELECT {fields_str}, sa.course_allotted FROM teachers t LEFT JOIN subject_allotment sa ON t.id = sa.teacher_id WHERE t.id = %s AND t.soft_delete = false"
        else:
            sql_query = "SELECT *, sa.course_allotted FROM teachers t LEFT JOIN subject_allotment sa ON t.id = sa.teacher_id WHERE t.id = %s AND t.soft_delete = false"

        cursor.execute(sql_query, (teacher_id,))
        teacher_details = cursor.fetchone()

        if teacher_details:
            print("Teacher Details:")
            if fields:
                for field, value in zip(fields, teacher_details[:-1]):
                    print(f"{field.capitalize()}: {value}")
                    
            else:
                print(f"ID: {teacher_details[0]}")
                print(f"Name: {teacher_details[1]}")
                print(f"Address: {teacher_details[2]}")
                print(f"Mobile Number: {teacher_details[3]}")
                print(f"Gender: {teacher_details[4]}")
                print(f"Teaching Specialties: {teacher_details[5]}")
                print(f"Date of Joining: {teacher_details[6]}")
                print(f"Course Allotted: {teacher_details[-1]}")
            print()
        else:
            print(f"No teacher found with ID {teacher_id}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
   
  
#example:
#view_teacher_details(8,'name','course_allotted')  # Specify fields
#view_teacher_details(1)  # No specified fields, display all details



def update_teacher_info(teacher_id, **kwargs):
    cursor = conn.cursor()
    try:
        # Check if the teacher exists
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        teacher = cursor.fetchone()
        if teacher is None:
            print("Error: Teacher not found.")
            return

        # Check if 'name' column is included in kwargs
        if 'name' in kwargs:
            print("Error: Name cannot be updated.")
            return

        # Check constraints for mobile_number
        if 'mobile_number' in kwargs and (not kwargs['mobile_number'].startswith("+91") or not kwargs['mobile_number'][3:].isdigit() or len(kwargs['mobile_number']) != 13):
            print("Error: Mobile number should start with +91 and be followed by 10 digits.")
            return

        # Check if course_allotted contains multiple values
        if 'course_allotted' in kwargs and len(kwargs['course_allotted'].split(',')) == 1:
            print("Error: Course allotted should contain more than one value separated by commas.")
            return

        # Construct the update query
        update_query = "UPDATE teachers t LEFT JOIN subject_allotment sa ON t.id = sa.teacher_id SET "
        update_values = []
        for key, value in kwargs.items():
            if key == 'course_allotted':
                update_query += f"sa.{key} = %s, "
            else:
                update_query += f"t.{key} = %s, "
            update_values.append(value)
        if not update_values:
            print("Error: No valid columns to update.")
            return
        update_query = update_query.rstrip(", ") + " WHERE t.id = %s"
        update_values.append(teacher_id)

        # Execute the update query
        cursor.execute(update_query, update_values)
        conn.commit()
        print("Teacher information updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
#example
#update_teacher_info(6, mobile_number="+919876543219", teaching_specialties="CS1,CS2,CS4", course_allotted="CS1,CS2")
#update_teacher_info(7,course_allotted="CS1,CS2")



def delete_teacher_record(teacher_id):
    cursor = conn.cursor()
    try:
        # Check if the teacher exists and has worked for at least 1 month
        cursor.execute("SELECT date_of_joining FROM teachers WHERE id = %s", (teacher_id,))
        join_date = cursor.fetchone()
        if join_date is None:
            print("Error: Teacher not found.")
            return

        # Convert join_date to datetime object
        join_date = datetime.strptime(join_date[0], '%d-%m-%Y').date()

        # Get the current date
        current_date = datetime.now().date()

        # Calculate the duration of employment
        employment_duration = (current_date - join_date).days

        # Check if employment duration is less than 30 days (1 month)
        if employment_duration < 30:
            print("Error: Teacher cannot be deleted as they have worked for less than 1 month.")
            return

        # Soft delete the teacher record by updating the soft_delete column
        cursor.execute("UPDATE teachers SET soft_delete = true WHERE id = %s", (teacher_id,))

        # Soft delete the teacher record from subject_allotment table
        cursor.execute("UPDATE subject_allotment SET soft_delete = true WHERE teacher_id = %s", (teacher_id,))

        # Commit the transaction
        conn.commit()
        print("Teacher record and subject allotment soft-deleted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
   

# Example usage:
#delete_teacher_record(8)


def list_teachers(gender=None, course_allotted=None):
    cursor = conn.cursor()
    try:
        # Base SQL query
        sql_query = "SELECT t.id, t.name, t.gender, sa.course_allotted FROM teachers t LEFT JOIN subject_allotment sa ON t.id = sa.teacher_id WHERE t.soft_delete = false"

        # Add filters based on parameters
        if gender:
            sql_query += f" AND t.gender = '{gender}'"
        if course_allotted:
            sql_query += f" AND sa.course_allotted LIKE '%{course_allotted}%'"

        # Execute SQL query
        cursor.execute(sql_query)
        teachers = cursor.fetchall()

        # Print results
        if teachers:
            print("List of Teachers:")
            for teacher in teachers:
                print(f"ID: {teacher[0]}, Name: {teacher[1]}")
        else:
            print("No teachers found matching the criteria.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
#list_teachers(course_allotted = 'CS1')
