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
            id = input('enter sturent  id: ')
            f_name = input('enter father name: ') 
            Date = input('enter DOB in DD-MM-YYYY format: ') 
            m_number = '+91' + input('enter mobile no: ')
            c_id = input('enter course id: ')
            update_student_info(student_id=id,fathers_name=f_name, DOB=Date, mobile_number=m_number, course_id=c_id)
            # update_student_info(student_id=104, fathers_name="New father", DOB="01-01-2010", mobile_number="+919876543210", course_id="CS4")
        elif choice == '3':
            # Call view_student_details function
            view_student_details(102)
        elif choice == '4':
            # Call list_students function
            course_id = input('enter course id CS1/2/3/4 ME1/2/3/4: ')
            year_of_study = input('enter year')
            list_students(course=course_id, year=year_of_study)
        elif choice == '5':
            # Call student_past_courses function
            student_past_courses(104)
        elif choice == '6':
            # Call delete_student function
            delete_student(103)
        elif choice == '7':
            # Call add_teacher function
            add_teacher('John Danny', '123 Main St', '+919876543210', 'Male', 'Math,Physics', '04-02-2023')
        elif choice == '8':
            # Call update_teacher_info function
            update_teacher_info(6, mobile_number="+919876543219", teaching_specialties="CS1,CS2,CS4", course_allotted="CS1,CS2")
        elif choice == '9':
            # Call view_teacher_details function
            view_teacher_details(8,'name','course_allotted')
        elif choice == '10':
            # Call list_teachers function
            list_teachers(course_allotted = 'CS1')
        elif choice == '11':
            # Call delete_teacher_record function
            delete_teacher_record(8)
        else:
            print("Invalid choice. Please enter a valid option.")
    cursor.close()
    conn.close()
    
if __name__ == "__main__":
    main()