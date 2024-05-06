from student import *
from teacher import *
from validation import authenticate_user
from connection import conn


# Define the menu function
def display_menu():
    print("Menu:")
    print("1. Add Student")
    print("2. Update Student Information")
    print("3. View Student Details")
    print("4. List Students")
    print("5. View Student's Past Courses")
    print("6. Delete Student")
    print("7. Add Teacher")
    print("8. Update Teacher Information")
    print("9. View Teacher Details")
    print("10. List Teachers")
    print("11. Delete Teacher Record")
    print("0. Exit")
    choice = input("Enter the number of the function you want to execute: ")
    return choice

# Main function to execute the selected function
def main():
    # Authenticate the user only if not already authenticated
    if not authenticate_user():
        print("Authentication failed. Access denied.")
        return  # Exit main program if authentication fails

    # User authentication successful
    print("Authentication successful. Proceeding with main program...")
    cursor = conn.cursor()
    while True:
    
        choice = display_menu()
        if choice == '0':

            break  # Exit the loop and end the program
        elif choice == '1':
            
            # Call add_student function
            name = input('enter new student name: ')
            gender = input('Male/Female: ')
            fathers_name = input('enter father name: ')
            address = input('enter address: ')
            date_of_birth = input('enter DOB: ')
            mobile_number = "+91" + input('enter mobile number: ')
            course_id = input('enter course details: ')
            Year = input('enter year of admission: ')
            add_student(name, gender, fathers_name, address, date_of_birth, mobile_number, course_id,Year)
            #add_student("Sanchit Shekhar", "Male", "Janny Depp", "123 Main St", "01-01-2020", "+919876543223", "CS2", '1st')
        
        elif choice == '2':
        # Call update_student_info function
            student_id = input('Enter student ID: ')
            update_fields = {}
            # Prompt the user for fields to update
            print("Enter the fields you want to update and their new values, or leave blank to stop:")
            while True:
                field = input("Field name ('fathers_name', 'DOB', 'mobile_number', 'course_id') or leave blank to stop: ").strip()
                if not field:
                    break
                value = input(f"Enter new value for {field}: ").strip()
                update_fields[field] = value
            update_student_info(student_id, **update_fields)


        elif choice == '3':
            # Call view_student_details function
            student_id = input("Enter student ID: ")
            valid_columns = ['name', 'gender', 'fathers_name', 'address', 'DOB', 'mobile_number', 'course_id', 'Year']
            print("Valid column options:", valid_columns)
            columns = input("Enter the columns you want to view (comma-separated), or leave blank to view all details: ").strip().split(',')
            view_student_details(student_id, *columns)

        elif choice == '4':
            filters = {}
            print("Enter the filters you want to apply (optional), or leave blank to skip:")
            course = input("Enter course ID CS1/2/3/4 ME1/2/3/4: ").strip()
            if course:
                filters['course'] = course
            
            year = input("Enter year of study: ").strip()
            if year:
                filters['year'] = year
            
            gender = input("Enter gender: ").strip()
            if gender:
                filters['gender'] = gender
            
            list_students(**filters)


        elif choice == '5':
            # Call student_past_courses function
            past_course = int(input('Enter the student_id :'))
            student_past_courses(past_course)
        elif choice == '6':
            # Call delete_student function
            delete = int(input('Enter the student_id :'))
            delete_student(delete)
        elif choice == '7':
    # Call add_teacher function
            print("Enter the details for the new teacher:")
            name = input("Name: ")
            address = input("Address: ")
            mobile_number = '+91' + input("Mobile Number (10 digits): ")
            gender = input("Gender: ")
            teaching_specialties = input("Teaching Specialties (comma-separated): ")
            date_of_joining = input("Date of Joining (in dd-mm-yyyy format): ")
            add_teacher(name, address, mobile_number, gender, teaching_specialties, date_of_joining)

        elif choice == '8':
            # Call update_teacher_info function
            teacher_id = input('Enter teacher ID: ')
            update_fields = {}
            # Prompt the user for fields to update
            print("Enter the fields you want to update and their new values, or leave blank to stop:")
            while True:
                field = input("Field name ('name', 'address', 'mobile_number', 'gender', 'teaching_specialties', 'date_of_joining', 'course_allotted') or leave blank to stop: ").strip()
                if not field:
                    break
                value = input(f"Enter new value for {field}: ").strip()
                update_fields[field] = value
            update_teacher_info(teacher_id, **update_fields)


        elif choice == '9':       
            # Print available fields for viewing teacher details
            available_fields = ['name', 'address', 'mobile_number', 'gender', 'teaching_specialties', 'date_of_joining', 'course_allotted']
            print("Available fields for viewing teacher details:", ', '.join(available_fields))

            # Call view_teacher_details function
            teacher_id = input('Enter teacher ID: ')
            fields_input = input("Enter the fields you want to view (comma-separated), or leave blank to view all details: ").strip()
            selected_fields = fields_input.split(',') if fields_input else None
            view_teacher_details(teacher_id, *selected_fields if selected_fields else ())

        elif choice == '10':
            # Prompt the user for criteria to list teachers
            gender = input("Enter gender (optional, press Enter to skip): ").strip()
            course_allotted = input("Enter course allotted (optional, press Enter to skip): ").strip()

            # Call list_teachers function with user-provided criteria
            list_teachers(gender, course_allotted)

        elif choice == '11':
            delete = int(input('enter teacher_id :'))
            delete_teacher_record(delete)
        else:
            print("Invalid choice. Please enter a valid option.")
    cursor.close()
    conn.close()
if __name__ == "__main__":
    main()
