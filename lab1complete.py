#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import getpass
import time
import shutil
from collections import defaultdict


class Student:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.students = defaultdict(list)  # Dictionary to store student data
        self.load_data()

    def load_data(self):
        """Loads data from CSV into a dictionary."""
        with open(self.csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                email, first_name, last_name, course_id, grade, marks = row
                self.students[email].append({
                    "first_name": first_name,
                    "last_name": last_name,
                    "course_id": course_id,
                    "grade": grade,
                    "marks": int(marks)
                })

    def display_records(self, email):
        """Displays student records based on email and tracks search time."""
        start_time = time.time()  # Start time tracking
        
        if email in self.students:
            records = self.students[email]
            print(f"Email ID: {email}")
            print(f"First Name: {records[0]['first_name']}")
            print(f"Last Name: {records[0]['last_name']}")
            print("Course Details:")
            for record in records:
                print(f"Course ID: {record['course_id']}, Grade: {record['grade']}, Marks: {record['marks']}")
        else:
            print("Student not found.")

        end_time = time.time()  # End time tracking
        print(f"Search completed in {end_time - start_time:.4f} seconds")  # Print time taken

    def add_new_student(self, email, first_name, last_name, courses):
        """Adds a new student with their course details."""
        if email in self.students:
            print("Student already exists.")
            return
        
        for course_id, grade, marks in courses:
            self.students[email].append({
                "first_name": first_name,
                "last_name": last_name,
                "course_id": course_id,
                "grade": grade,
                "marks": int(marks)
            })
        self.save_data()
        print("Student added successfully.")

    def delete_student(self, email):
        """Deletes a student completely."""
        if email in self.students:
            del self.students[email]
            self.save_data()
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def update_student_record(self, email, course_id, new_grade, new_marks):
        """Updates a student's specific course details."""
        if email in self.students:
            for record in self.students[email]:
                if record["course_id"] == course_id:
                    record["grade"] = new_grade
                    record["marks"] = int(new_marks)
                    self.save_data()
                    print("Record updated successfully.")
                    return
            print("Course not found for the student.")
        else:
            print("Student not found.")

    def check_my_marks(self, email):
        """Displays marks and calculates mean & median scores for each course and overall."""
        start_time = time.time()  # Start time tracking
        
        import statistics
        if email not in self.students:
            print("Student not found.")
            return
        
        course_marks = defaultdict(list)
        for records in self.students.values():
            for record in records:
                course_marks[record["course_id"]].append(record["marks"])
        
        print(f"Marks for {email}:")
        student_marks = []
        for record in self.students[email]:
            course = record["course_id"]
            marks = record["marks"]
            student_marks.append(marks)
            mean_course = sum(course_marks[course]) / len(course_marks[course])
            median_course = statistics.median(course_marks[course])
            print(f"Course ID: {course}, Marks: {marks}, Mean: {mean_course:.2f}, Median: {median_course:.2f}")
        
        mean_student = sum(student_marks) / len(student_marks)
        print(f"Overall Student Mean: {mean_student:.2f}")

        end_time = time.time()  # End time tracking
        print(f"Operation completed in {end_time - start_time:.4f} seconds")  # Print time taken

    def check_my_grade(self, email):
        """Displays grades and determines overall student grade based on mean marks."""
        start_time = time.time()  # Start time tracking
        
        if email not in self.students:
            print("Student not found.")
            return
        
        course_marks = defaultdict(list)
        for records in self.students.values():
            for record in records:
                course_marks[record["course_id"]].append(record["marks"])
        
        student_grades = []
        print(f"Grades for {email}:")
        for record in self.students[email]:
            course = record["course_id"]
            marks = record["marks"]
            mean_course = sum(course_marks[course]) / len(course_marks[course])
            
            if marks > mean_course:
                grade = "A"
            elif marks == mean_course:
                grade = "B"
            else:
                grade = "C"
            
            student_grades.append(grade)
            print(f"Course ID: {course}, Marks: {marks}, Assigned Grade: {grade}")
        
        overall_grade = max(set(student_grades), key=student_grades.count)
        print(f"Overall Student Grade: {overall_grade}")

        end_time = time.time()  # End time tracking
        print(f"Operation completed in {end_time - start_time:.4f} seconds")  # Print time taken

    def save_data(self):
        """Saves updated data back to CSV."""
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Email_address", "First_name", "Last_name", "Course.id", "grades", "Marks"])
            for email, records in self.students.items():
                for record in records:
                    writer.writerow([email, record["first_name"], record["last_name"], record["course_id"], record["grade"], record["marks"]])
                    
class CourseDB:
    def __init__(self, filename):
        self.filename = filename

    def load_courses(self):
        """Load courses from a CSV file."""
        courses = []
        with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                courses.append(row)
        return courses

    def display_courses(self):
        """Display available courses and details of a selected course."""
        courses = self.load_courses()
        course_ids = [course['Course_id'] for course in courses]

        print("\nAvailable courses:")
        print("-" * 32)
        for cid in course_ids:
            print(f"     {cid}")

        selected_id = input("\nEnter Course ID to view details: ").strip()
        selected_course = next((course for course in courses if course['Course_id'] == selected_id), None)

        if selected_course:
            print("\nCourse Details:")
            print(f"Course ID: {selected_course['Course_id']}")
            print(f"Course Name: {selected_course['Course_name']}")
            print(f"Description: {selected_course['Description']}")
            print(f"Credits: {selected_course['Credits']}")
        else:
            print("Course ID not found.")

    def add_new_course(self):
        """Add a new course to the CSV file."""
        course_id = input("Enter Course ID: ").strip()
        course_name = input("Enter Course Name: ").strip()
        description = input("Enter Description: ").strip()
        credits = input("Enter Credits: ").strip()

        new_course = {'Course_id': course_id, 'Course_name': course_name, 'Description': description, 'Credits': credits}

        with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Course_id', 'Course_name', 'Description', 'Credits'])
            writer.writerow(new_course)

        print("New course added successfully!")

    def delete_course(self):
        """Delete a course by Course ID and update the CSV file."""
        courses = self.load_courses()
        course_id_to_delete = input("Enter Course ID to delete: ").strip()

        updated_courses = [course for course in courses if course['Course_id'] != course_id_to_delete]

        if len(updated_courses) == len(courses):
            print("Course ID not found.")
            return

        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Course_id', 'Course_name', 'Description', 'Credits'])
            writer.writeheader()
            writer.writerows(updated_courses)

        print("Course deleted successfully and updated in the file!")

    def modify_course_details(self):
        """Modify an existing course's details."""
        courses = self.load_courses()
        course_id_to_modify = input("Enter Course ID to modify: ").strip()

        for course in courses:
            if course['Course_id'] == course_id_to_modify:
                print("\nEnter new details (leave blank to keep existing values):")
                new_name = input(f"New Course Name ({course['Course_name']}): ").strip() or course['Course_name']
                new_description = input(f"New Description ({course['Description']}): ").strip() or course['Description']
                new_credits = input(f"New Credits ({course['Credits']}): ").strip() or course['Credits']

                course['Course_name'] = new_name
                course['Description'] = new_description
                course['Credits'] = new_credits
                break
        else:
            print("Course ID not found.")
            return

        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Course_id', 'Course_name', 'Description', 'Credits'])
            writer.writeheader()
            writer.writerows(courses)

        print("Course details updated successfully!")


def show_professor_details_by_course(course_id):
    """Display professor details for a given course."""
    professors = []

    try:
        # Read professor data
        with open('professor.csv', 'r', encoding='utf-8-sig') as prof_file:
            prof_reader = csv.DictReader(prof_file)

            # Get actual column names from CSV
            headers = prof_reader.fieldnames
            print(f"CSV Headers Found: {headers}")  # Debugging step

            professor_id_col = 'Professor_id' if 'Professor_id' in headers else headers[0]
            professor_name_col = 'professor_Name' if 'professor_Name' in headers else headers[1]
            rank_col = 'Rank' if 'Rank' in headers else headers[2]
            course_id_col = 'course_id' if 'course_id' in headers else headers[3]

            for row in prof_reader:
                if row[course_id_col] == course_id:
                    professors.append({
                        "Professor_id": row[professor_id_col],
                        "Professor_Name": row[professor_name_col],
                        "Rank": row[rank_col]
                    })

    except FileNotFoundError:
        print("Professor data file not found.")
        return

    # Read course data (for validation)
    course_found = False
    try:
        with open('course.csv', 'r', encoding='utf-8-sig') as course_file:
            course_reader = csv.DictReader(course_file)
            for row in course_reader:
                if row['Course_id'] == course_id:
                    course_found = True
                    break
    except FileNotFoundError:
        print("Course data file not found.")
        return

    if not course_found:
        print(f"Course ID '{course_id}' not found.")
        return

    # Display professor details
    if professors:
        print(f"Professor details for course ID '{course_id}':\n")
        for prof in professors:
            print(f"Professor ID: {prof['Professor_id']}")
            print(f"Professor Name: {prof['Professor_Name']}")
            print(f"Rank: {prof['Rank']}\n")
    else:
        print(f"No professor found for course ID '{course_id}'.")                    

        
        
        
        
        
        
        
        
class Professor:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.professors = defaultdict(list)
        self.load_data()

    def load_data(self):
        """Loads data from CSV into a dictionary."""
        with open(self.csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                professor_id, professor_name, rank, course_id = row
                self.professors[professor_id].append({
                    "professor_name": professor_name,
                    "rank": rank,
                    "course_id": course_id
                })

    def display_professors_details(self, professor_id):
        """Displays professor details based on ID."""
        if professor_id in self.professors:
            records = self.professors[professor_id]
            print(f"Professor ID: {professor_id}")
            print(f"Professor Name: {records[0]['professor_name']}")
            print(f"Rank: {records[0]['rank']}")
            print("Courses:", ', '.join([rec['course_id'] for rec in records]))
        else:
            print("Professor not found.")
            
    def add_user(self, user_id, password, role):
        """Adds a new user with a hashed password."""
        if user_id in self.users:
            print("User ID already exists! Choose another.")
            return
        hashed_password = self.hash_password(password)
        self.users[user_id] = {'password': hashed_password, 'role': role}
        self.save_users()
        print(f"User '{user_id}' added successfully!")

    def add_new_professor(self, professor_id, professor_name, rank, courses):
        """Adds a new professor with their course details."""
        for course_id in courses:
            self.professors[professor_id].append({
                "professor_name": professor_name,
                "rank": rank,
                "course_id": course_id.strip()
            })
        self.save_data()
        print("Professor added successfully.")

    def delete_professor(self, professor_id):
        """Deletes a professor completely."""
        if professor_id in self.professors:
            del self.professors[professor_id]
            self.save_data()
            print("Professor deleted successfully.")
        else:
            print("Professor not found.")

    def modify_professor_details(self, professor_id, new_name=None, new_rank=None, new_courses=None):
        """Modifies a professor's details."""
        if professor_id in self.professors:
            for record in self.professors[professor_id]:
                record["professor_name"] = new_name if new_name else record["professor_name"]
                record["rank"] = new_rank if new_rank else record["rank"]
            if new_courses:
                self.professors[professor_id] = [{
                    "professor_name": new_name or record["professor_name"],
                    "rank": new_rank or record["rank"],
                    "course_id": course.strip()
                } for course in new_courses]
            self.save_data()
            print("Professor details modified successfully.")
        else:
            print("Professor not found.")

    def show_course_details_by_professor(self, professor_id, course_csv):
        """Displays course details for a professor."""
        professor_courses = [rec['course_id'] for rec in self.professors.get(professor_id, [])]
        if not professor_courses:
            print("Professor not found!")
            return

        print(f"Professor {professor_id} teaches: {', '.join(professor_courses)}\n")
        print("Course Details:")
        
        with open(course_csv, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Course_id'] in professor_courses:
                    print(f"Course ID: {row['Course_id']}, Name: {row['Course_name']}, Description: {row['Description']}, Credits: {row['Credits']}")

    def save_data(self):
        """Saves updated data back to CSV."""
        with open(self.csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["Professor_id", "professor_Name", "Rank", "course_id"])
            for professor_id, records in self.professors.items():
                for record in records:
                    writer.writerow([professor_id, record["professor_name"], record["rank"], record["course_id"]])


class LoginSystem:
    """Handles user authentication without encryption or decryption."""
    
    def __init__(self, csv_file='login.csv'):
        self.csv_file = csv_file
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from the CSV file."""
        users = {}
        try:
            with open(self.csv_file, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    users[row['user_id']] = {
                        'password': row['password'],
                        'role': row['role']
                    }
        except FileNotFoundError:
            print("User data file not found!")
        return users
    
    def save_users(self):
        """Save users to the CSV file."""
        with open(self.csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'password', 'role'])
            for user_id, data in self.users.items():
                writer.writerow([user_id, data['password'], data['role']])
                
    def add_user(self, user_id, password, role):
            """Adds a new user without hashing the password."""
            if user_id in self.users:
                print("User ID already exists! Choose another.")
                return
            self.users[user_id] = {'password': password, 'role': role}
            self.save_users()
            print(f"User '{user_id}' added successfully!")

    
    def login(self, user_id, password):
        """Authenticate the user."""
        if user_id in self.users:
            stored_password = self.users[user_id]['password']
            if stored_password == password:
                return self.users[user_id]['role']
        return None
    
    def change_password(self, user_id, new_password):
        """Change the password for a user."""
        if user_id in self.users:
            self.users[user_id]['password'] = new_password
            self.save_users()
            print("Password updated successfully!")
        else:
            print("User not found!")

    def logout(self):
        """Logs out the user."""
        print("Logged out successfully!")

    
# Main Menu with options for login, change password, and logout
def main_menu():
    login_db = LoginSystem('login.csv')
    student_db = Student("student.csv")
    course_db = CourseDB('course.csv')
    professor_db = Professor("professor.csv")
    while True:
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("Welcome to Check My Grade App".center(columns))
        print("San Jose State University, Department of Data Analytics".center(columns))
        print("Address: 1 Washington Square, San Jose".center(columns))
        print("Phone: +1650-xxx-xxxx".center(columns))
        print("================================".center(columns))   
        print("\nMain Menu:")
        print("1. Login")
        print("2. Change Password")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            email = input("Enter your email: ")
            password = getpass.getpass("Enter your password: ")
            role = login_db.login(email.strip(), password.strip())
            if role:
                if role == 'student':
                    
                    while True:
                        print("=================================".center(columns))
                        print("Welcome to Check My Grade App".center(columns))
                        print("San Jose State University, Department of Data Analytics".center(columns))
                        print("================================".center(columns))
                        print("\n Check My Grade App Student's Menu:")
                        print("1. Display Student Records")
                        print("2. Display Courses")
                        print("3. Show professor details by course ID")
                        print("4. Check My Marks")
                        print("5. Check My Grade")
                        print("6. Logout")
                        choice = input("Enter your choice: ")
                        if choice == '1':
                            email = input("Enter student email: ")
                            student_db.display_records(email)
                        elif choice == '2':
                            course_db.display_courses()
                        elif choice == '3':
                            course_id_input = input("Enter Course ID: ")
                            show_professor_details_by_course(course_id_input)
                        elif choice == '4':
                            email = input("Enter student email: ")
                            student_db.check_my_marks(email)
                        elif choice == '5':
                            email = input("Enter student email: ")
                            student_db.check_my_grade(email)
                        elif choice == '6':
                                 break
                        else:
                            print("Invalid choice!")
                elif role == 'professor':
                    while True:
                        print("=================================".center(columns))
                        print("Welcome to Check My Grade App".center(columns))
                        print("San Jose State University, Department of Data Analytics".center(columns))
                        print("================================".center(columns))
                        print("\n Check My Grade App Professor Menu:")
                        print("1. Display Professor Details")
                        print("2. Display Student Records")
                        print("3. Add New Student")
                        print("4. Delete Student ")
                        print("5. Update Student Record")
                        print("6. Add New Course")
                        print("7. Delete Course")
                        print("8.Modify Course Details")
                        print("9. Add New Professor")
                        print("10.Delete Professor")
                        print("11.Modify Professor Details")
                        print("12.Show Course Details by Professor")
                        print("13.Add new user")
                        print("14.Logout")
                        choice = input("Enter your choice: ")
                        if choice == '1':
                            professor_id = input("Enter Professor ID: ")
                            professor_db.display_professors_details(professor_id)
                        elif choice == '2':
                            email = input("Enter student email: ")
                            student_db.display_records(email)
                        elif choice == '3':
                            email = input("Enter email: ")
                            first_name = input("Enter first name: ")
                            last_name = input("Enter last name: ")
                            courses = [tuple(input("Enter Course ID, Grade, Marks: ").split(",")) for _ in range(4)]
                            student_db.add_new_student(email, first_name, last_name, courses)
                        elif choice == '4':
                            email = input("Enter student email to delete: ")
                            student_db.delete_student(email)
                        elif choice == '5':
                            email = input("Enter student email: ")
                            course_id =input("Enter course ID to update:")
                            grade =input("Enter new grade:")
                            marks =input("Enter new marks:")
                            student_db.update_student_record(email, course_id, grade, marks)
                        elif choice == '6':
                            course_db.add_new_course()
                        elif choice == '7':
                            course_db.delete_course()
                        elif choice == '8':
                            course_db.modify_course_details()
                        elif choice == '9':
                            professor_id = input("Enter Professor ID: ")
                            professor_name = input("Enter Professor Name: ")
                            rank = input("Enter Rank: ")
                            courses = input("Enter Course IDs (comma separated): ").split(',')
                            professor_db.add_new_professor(professor_id, professor_name, rank, courses)
                        elif choice == '10':
                                professor_id = input("Enter Professor ID to delete: ")
                                professor_db.delete_professor(professor_id)
                        elif choice == '11':
                                professor_id = input("Enter Professor ID to modify: ")
                                new_name = input("Enter new name (leave blank to keep unchanged): ") or None
                                new_rank = input("Enter new rank (leave blank to keep unchanged): ") or None
                                new_courses = input("Enter new Course IDs (comma separated, leave blank to keep unchanged): ")
                                new_courses = new_courses.split(',') if new_courses else None
                                professor_db.modify_professor_details(professor_id, new_name, new_rank, new_courses)
                        elif choice == '12':
                                professor_id = input("Enter Professor ID: ")
                                professor_db.show_course_details_by_professor(professor_id,"course.csv")
                        elif choice == '13':
                                email = input("Enter new user email: ")
                                password = getpass.getpass("Enter password for new user: ")
                                role = input("Enter role (student/professor): ")
                                login_db.add_user(email, password, role)
                        elif choice == '14':
                            break
                        else:
                            print("Invalid choice!")

        elif choice == '2':
            email = input("Enter your email: ")
            new_password = getpass.getpass("Enter new password: ")
            login_db.change_password(email, new_password)
        elif choice == '3':
            login_db.logout()
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()


# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




