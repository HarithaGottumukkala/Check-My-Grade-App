import time
import csv
from lab1complete import Student, CourseDB, Professor

def test_student_records():
    student_db = Student("student.csv")
    
    print("Checking student records...")
    num_students = sum(len(records) for records in student_db.students.values())
    print(f"Total student records found: {num_students}")
    
    if num_students == 1000:
        print("Student records check passed. There are exactly 1000 students.")
    else:
        print(f"Warning: Expected 1000 records, but found {num_students}.")

    print("Sorting student records...")
    start_time = time.time()
    sorted_students = sorted(student_db.students.items(), key=lambda x: x[1][0]['marks'])
    end_time = time.time()
    print(f"Sorting by marks took {end_time - start_time:.4f} seconds")

    start_time = time.time()
    sorted_students_email = sorted(student_db.students.items(), key=lambda x: x[0], reverse=True)
    end_time = time.time()
    print(f"Sorting by email took {end_time - start_time:.4f} seconds")

def test_student_operations():
    student_db = Student("student.csv")
    print("Adding a new student...")
    email = input("Enter student email: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    courses = [tuple(input("Enter Course ID, Grade, Marks: ").split(",")) for _ in range(1)]
    student_db.add_new_student(email, first_name, last_name, courses)

    print("Updating student record...")
    email = input("Enter student email to update: ")
    course_id = input("Enter course ID: ")
    new_grade = input("Enter new grade: ")
    new_marks = input("Enter new marks: ")
    student_db.update_student_record(email, course_id, new_grade, new_marks)

    print("Deleting student record...")
    email = input("Enter student email to delete: ")
    student_db.delete_student(email)

def test_course_operations():
    course_db = CourseDB("course.csv")
    print("Adding a new course...")
    course_db.add_new_course()
    
    print("Modifying course details...")
    course_db.modify_course_details()
    
    print("Deleting a course...")
    course_db.delete_course()

def test_professor_operations():
    professor_db = Professor("professor.csv")
    print("Adding a new professor...")
    professor_id = input("Enter Professor ID: ")
    professor_name = input("Enter Professor Name: ")
    rank = input("Enter Rank: ")
    courses = input("Enter Course IDs (comma separated): ").split(',')
    professor_db.add_new_professor(professor_id, professor_name, rank, courses)

    print("Modifying professor details...")
    professor_id = input("Enter Professor ID to modify: ")
    new_name = input("Enter new name (leave blank to keep unchanged): ") or None
    new_rank = input("Enter new rank (leave blank to keep unchanged): ") or None
    new_courses = input("Enter new Course IDs (comma separated, leave blank to keep unchanged): ")
    new_courses = new_courses.split(',') if new_courses else None
    professor_db.modify_professor_details(professor_id, new_name, new_rank, new_courses)

    print("Deleting a professor...")
    professor_id = input("Enter Professor ID to delete: ")
    professor_db.delete_professor(professor_id)

if __name__ == "__main__":
    print("Running tests...")
    test_student_records()
    test_student_operations()
    test_course_operations()
    test_professor_operations()
    print("All tests completed successfully!")
