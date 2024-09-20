import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import re
import sqlite3
conn = sqlite3.connect('Database/schoolsystem.sqlite')
cursor = conn.cursor()
class SchoolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.state('zoomed')

        
        self.main_menu_frame = tk.Frame(self.root)
        # Frames for each form
        self.student_frame = tk.Frame(self.root)
        self.instructor_frame = tk.Frame(self.root)
        self.course_frame = tk.Frame(self.root)

        # Create a frame for the buttons at the bottom
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="bottom", pady=10)
        # Frame for displaying all records
        self.display_frame = tk.Frame(self.root)


       

        # Main Menu Buttons
        tk.Label(self.main_menu_frame, text="School Management System", font=("Arial", 20, "bold")).pack(pady=20)
        self.student_button = tk.Button(self.main_menu_frame, text="Add Student", command=self.show_student_form)
        self.student_button.pack(pady=5)

        self.instructor_button = tk.Button(self.main_menu_frame, text="Add Instructor", command=self.show_instructor_form)
        self.instructor_button.pack(pady=5)

        self.course_button = tk.Button(self.main_menu_frame, text="Add Course", command=self.show_course_form)
        self.course_button.pack(pady=5)

        self.register_button = tk.Button(self.main_menu_frame, text="Register for Course", command=self.show_register_course_form)
        self.register_button.pack(pady=5)

        self.assign_instructor_button = tk.Button(self.main_menu_frame, text="Assign Instructor", command=self.show_assign_instructor_form)
        self.assign_instructor_button.pack(pady=5)

        self.display_students_button = tk.Button(self.main_menu_frame, text="View All Students", command=self.display_all_students)
        self.display_students_button.pack(pady=5)

        self.display_instructors_button = tk.Button(self.main_menu_frame, text="View All Instructors", command=self.display_all_instructors)
        self.display_instructors_button.pack(pady=5)

        self.display_courses_button = tk.Button(self.main_menu_frame, text="View All Courses", command=self.display_all_courses)
        self.display_courses_button.pack(pady=5)
        
        self.search_button = tk.Button(self.main_menu_frame, text="Search", command=self.show_search_form)
        self.search_button.pack(pady=5)


        self.main_menu_frame.pack(fill="both", expand=True)

        # Create tabs for each form
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()
        self.create_register_course_form()
        self.create_assign_instructor_form()
        self.create_search_form()

    # Create form to add a Student
    def create_student_form(self):
        tk.Label(self.student_frame, text="Add Student", font=("Arial", 16)).pack(pady=10)
        
        self.student_name_var = tk.StringVar()
        self.student_age_var = tk.IntVar()
        self.student_email_var = tk.StringVar()
        self.student_id_var = tk.StringVar()

        tk.Label(self.student_frame, text="Name").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_name_var).pack()

        tk.Label(self.student_frame, text="Age").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_age_var).pack()

        tk.Label(self.student_frame, text="Email").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_email_var).pack()

        tk.Label(self.student_frame, text="Student ID").pack(pady=5)
        tk.Entry(self.student_frame, textvariable=self.student_id_var).pack()

        tk.Button(self.student_frame, text="Add", command=self.add_student).pack(pady=10)
         # Back Button
        tk.Button(self.student_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    # Create form to add an Instructor
    def create_instructor_form(self):
        tk.Label(self.instructor_frame, text="Add Instructor", font=("Arial", 16)).pack(pady=10)
        
        self.instructor_name_var = tk.StringVar()
        self.instructor_age_var = tk.IntVar()
        self.instructor_email_var = tk.StringVar()
        self.instructor_id_var = tk.StringVar()

        tk.Label(self.instructor_frame, text="Name").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_name_var).pack()

        tk.Label(self.instructor_frame, text="Age").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_age_var).pack()

        tk.Label(self.instructor_frame, text="Email").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_email_var).pack()

        tk.Label(self.instructor_frame, text="Instructor ID").pack(pady=5)
        tk.Entry(self.instructor_frame, textvariable=self.instructor_id_var).pack()

        tk.Button(self.instructor_frame, text="Add", command=self.add_instructor).pack(pady=10)
         # Back Button
        tk.Button(self.instructor_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    # Create form to add a Course
    def create_course_form(self):
        tk.Label(self.course_frame, text="Add Course", font=("Arial", 16)).pack(pady=10)
        
        self.course_id_var = tk.StringVar()
        self.course_name_var = tk.StringVar()

        tk.Label(self.course_frame, text="Course ID").pack(pady=5)
        tk.Entry(self.course_frame, textvariable=self.course_id_var).pack()

        tk.Label(self.course_frame, text="Course Name").pack(pady=5)
        tk.Entry(self.course_frame, textvariable=self.course_name_var).pack()

        tk.Button(self.course_frame, text="Add", command=self.add_course).pack(pady=10)
         # Back Button
        tk.Button(self.course_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)

    def create_register_course_form(self):
        self.register_course_frame = tk.Frame(self.root)

        tk.Label(self.register_course_frame, text="Register for Course", font=("Arial", 16)).pack(pady=10)

        self.register_student_id_var = tk.StringVar()
        self.selected_course_var = tk.StringVar()

        tk.Label(self.register_course_frame, text="Student ID").pack(pady=5)
        tk.Entry(self.register_course_frame, textvariable=self.register_student_id_var).pack()

        tk.Label(self.register_course_frame, text="Select Course").pack(pady=5)

        # Load available courses for the dropdown
        courses = self.load_courses_sql()
        
        # Check if courses are available
        if courses:
            self.selected_course_var.set(courses[0])  # Set default to the first course
            self.course_dropdown = tk.OptionMenu(self.register_course_frame, self.selected_course_var, *courses)
        else:
            self.selected_course_var.set("No available courses")
            self.course_dropdown = tk.OptionMenu(self.register_course_frame, self.selected_course_var, "No available courses")

        self.course_dropdown.pack()

        tk.Button(self.register_course_frame, text="Register", command=self.register_student_for_course).pack(pady=10)
         # Back Button
        tk.Button(self.register_course_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)
 
    def create_assign_instructor_form(self):
        self.assign_instructor_frame = tk.Frame(self.root)

        tk.Label(self.assign_instructor_frame, text="Assign Instructor to Course", font=("Arial", 16)).pack(pady=10)

        self.assign_instructor_id_var = tk.StringVar()
        self.assign_course_var = tk.StringVar()

        tk.Label(self.assign_instructor_frame, text="Instructor ID").pack(pady=5)
        tk.Entry(self.assign_instructor_frame, textvariable=self.assign_instructor_id_var).pack()

        tk.Label(self.assign_instructor_frame, text="Select Course").pack(pady=5)

        # Load available courses for the dropdown
        courses = self.load_courses_sql()
        if courses:
            self.assign_course_var.set(courses[0])  # Set default to the first course
            self.assign_course_dropdown = tk.OptionMenu(self.assign_instructor_frame, self.assign_course_var, *courses)
        else:
            self.assign_course_var.set("No available courses")
            self.assign_course_dropdown = tk.OptionMenu(self.assign_instructor_frame, self.assign_course_var, "No available courses")

        self.assign_course_dropdown.pack()

        tk.Button(self.assign_instructor_frame, text="Assign", command=self.assign_instructor_to_course).pack(pady=10)

        # Button to go back to main menu
        tk.Button(self.assign_instructor_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)
        
    def create_display_treeview(self, headers, data, category):
        # Clear the previous frame content
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Create the treeview and store it as an instance attribute
        self.tree = ttk.Treeview(self.display_frame, columns=headers, show='headings')

        # Define the headings
        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=100)  # Adjust width if needed

        # Insert the data rows
        for row in data:
            self.tree.insert('', tk.END, values=row)

        self.tree.pack(fill="both", expand=True)

        # Add Edit and Delete buttons
        self.save_edit_button = tk.Button(self.display_frame, text="Edit", command=lambda: self.save_edit(category))
        self.save_edit_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.delete_button = tk.Button(self.display_frame, text="Delete", command=lambda: self.delete_record(category))
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Button to go back to the main menu
        tk.Button(self.display_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5, pady=10)

        self.hide_all_frames()
        self.display_frame.pack(fill="both", expand=True)
  
    def create_search_form(self):
        self.search_frame = tk.Frame(self.root)

        tk.Label(self.search_frame, text="Search", font=("Arial", 16)).pack(pady=10)

        # Search by options (ID, Name)
        self.search_by_var = tk.StringVar(value="ID")
        tk.Label(self.search_frame, text="Search By").pack(pady=5)
        search_by_dropdown = ttk.Combobox(self.search_frame, textvariable=self.search_by_var, values=["ID", "Name"])
        search_by_dropdown.pack()

        # Search in options (Student, Instructor, Course)
        self.search_in_var = tk.StringVar(value="Student")
        tk.Label(self.search_frame, text="Search In").pack(pady=5)
        search_in_dropdown = ttk.Combobox(self.search_frame, textvariable=self.search_in_var, values=["Student", "Instructor", "Course"])
        search_in_dropdown.pack()

        # Entry field for search value
        self.search_value_var = tk.StringVar()
        tk.Label(self.search_frame, text="Enter value").pack(pady=5)
        tk.Entry(self.search_frame, textvariable=self.search_value_var).pack()

        # Search button
        tk.Button(self.search_frame, text="Search", command=self.perform_search).pack(pady=10)
        # Button to go back to main menu
        tk.Button(self.search_frame, text="Back to Main Menu", command=self.show_main_menu).pack(pady=10)
        
    # Event handlers for adding a Student
    def add_student(self):
        name = self.student_name_var.get()
        age = self.student_age_var.get()
        email = self.student_email_var.get()
        student_id = self.student_id_var.get()

        # Simple validation
        if name and age and email and student_id:
            try:
                assert (type(name) == str), "Name must be a string" 
                assert(name.strip() != ""), "name cannot be empty"
                assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                age = int(age)
                assert (age >= 0), "Age cannot be negative"
                regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                assert(re.match(regex, email) is not None), "Wrong email format"
                cursor.execute("INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)", (student_id, name, age, email))
                conn.commit()
                messagebox.showinfo("Success", "Student added successfully")
                self.clear_student_fields()
                self.show_main_menu() 
            except Exception as e:
                messagebox.showerror("Error please make sure of the inputs")
        else:
            messagebox.showwarning("Warning", "All fields must be filled")

    # Event handlers for adding an Instructor
    def add_instructor(self):
        name = self.instructor_name_var.get()
        age = self.instructor_age_var.get()
        email = self.instructor_email_var.get()
        instructor_id = self.instructor_id_var.get()

        # Simple validation
        if name and age and email and instructor_id:
            try:
                assert (type(name) == str), "Name must be a string" 
                assert(name.strip() != ""), "name cannot be empty"
                assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                age = int(age)
                assert (age >= 0), "Age cannot be negative"
                regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                assert(re.match(regex, email) is not None), "Wrong email format"
                cursor.execute("INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)", (instructor_id, name, age, email))
                conn.commit()
                messagebox.showinfo("Success", "Instructor added successfully")
                self.clear_instructor_fields()
                self.show_main_menu()  
            except Exception as e:
                messagebox.showerror("Error please make sure of the inputs")
        else:
            messagebox.showwarning("Warning", "All fields must be filled")

    # Event handlers for adding a Course
    def add_course(self):
        course_id = self.course_id_var.get()
        course_name = self.course_name_var.get()

        # Simple validation
        if course_id and course_name:
            try:
                assert (type(course_name) == str), "Name must be a string" 
                assert(course_name.strip() != ""), "name cannot be empty"
                assert re.match(r"^[a-zA-Z\s]+$", course_name), "Name must contain only alphabetic characters and spaces"
                
                cursor.execute("INSERT INTO courses (course_id, course_name) VALUES (?, ?)", (course_id, course_name))
                conn.commit()
                messagebox.showinfo("Success", "Course added successfully")
                self.clear_course_fields()
                self.show_main_menu()
            except Exception as e:
                messagebox.showerror("Error, course cannot be registered. Make sure of the inputs")
        else:
            messagebox.showwarning("Warning", "All fields must be filled")
    
    def hide_all_frames(self):
        self.main_menu_frame.pack_forget()  # Hide the main menu
        self.student_frame.pack_forget()    # Hide the student form
        self.instructor_frame.pack_forget() # Hide the instructor form
        self.course_frame.pack_forget()     # Hide the course form
        self.register_course_frame.pack_forget()  # Hide the course registration form
        self.assign_instructor_frame.pack_forget() # Hide the instructor assignment form
        self.display_frame.pack_forget()
        self.search_frame.pack_forget()

    def show_student_form(self):
        self.hide_all_frames()
        self.student_frame.pack(fill="both", expand=True)

    def show_instructor_form(self):
        self.hide_all_frames()
        self.instructor_frame.pack(fill="both", expand=True)

    def show_course_form(self):
        self.hide_all_frames()
        self.course_frame.pack(fill="both", expand=True)

     # Show search form
    
    def show_search_form(self):
        self.hide_all_frames()
        self.search_frame.pack(fill="both", expand=True)
    
    def show_register_course_form(self):
        self.hide_all_frames()
        self.create_register_course_form()
        self.register_course_frame.pack(fill="both", expand=True)

    def show_assign_instructor_form(self):
        self.hide_all_frames()
        self.create_assign_instructor_form()
        self.assign_instructor_frame.pack(fill="both", expand=True)
    # Show main menu
    def show_main_menu(self):
        self.hide_all_frames()  # Hide all other frames first
        self.main_menu_frame.pack(fill="both", expand=True)

    def clear_student_fields(self):
        self.student_name_var.set("")
        self.student_age_var.set(0)
        self.student_email_var.set("")
        self.student_id_var.set("")
    
    def clear_instructor_fields(self):
        self.instructor_name_var.set("")
        self.instructor_age_var.set(0)
        self.instructor_email_var.set("")
        self.instructor_id_var.set("")
    
    def clear_course_fields(self):
        self.course_id_var.set("")
        self.course_name_var.set("")

    def register_student_for_course(self):
        student_id = self.register_student_id_var.get()
        selected_course_id = self.selected_course_var.get()
        if not student_id or not selected_course_id:
             messagebox.showwarning("Student or course not selected.")
        else:
            try:
                # Simple validation
                cursor.execute("SELECT student_id from students where student_id = ?",(student_id,))
                student_data = cursor.fetchone() 
                cursor.execute("SELECT course_id from courses where course_id = ?",(selected_course_id,))
                course_data = cursor.fetchone() 

                if student_data is not None and course_data is not None:
                    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",(student_id,selected_course_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Student {student_id} registered for {selected_course_id}")
                else:
                    messagebox.showerror("Student or course doesn't exists.")
            except Exception as e:
                messagebox.showerror("Error occured")

    def assign_instructor_to_course(self):
        instructor_id = self.assign_instructor_id_var.get()
        selected_course_id = self.assign_course_var.get()

        # Simple validation
        if not instructor_id or not selected_course_id:
            messagebox.showwarning("instructor or course not selected")
           
        else:
            try:
                        # Simple validation
                    cursor.execute("SELECT instructor_id from instructors where instructor_id = ?",(instructor_id,))
                    instructor_data = cursor.fetchone() 
                    cursor.execute("SELECT course_id from courses where course_id = ?",(selected_course_id,))
                    course_data = cursor.fetchone() 
                    cursor.execute("SELECT instructor_id from courses where course_id = ? ",(selected_course_id,))
                    current_inst = cursor.fetchone()
               
                    if instructor_data is not None and course_data is not None and current_inst[0] is None:
                        cursor.execute("UPDATE courses SET instructor_id = ? WHERE course_id = ?",(instructor_id,selected_course_id,))
                        conn.commit()
                        messagebox.showinfo("Success", f"Instructor {instructor_id} registered for {selected_course_id}")
                    else:
                        messagebox.showerror("instructor or course doesn't exists.")
                    self.assign_instructor_id_var.set("")  # Clear the instructor ID input
                    self.assign_course_var.set("")  # Clear the selected course
                    self.show_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_all_students(self):
        cursor.execute("SELECT * FROM students;")
        students = cursor.fetchall()
        data=[]
        for s in students:
            print(s[0])
            cursor.execute("SELECT course_id from student_courses where student_id  = ?",(s[0],))
            courses = cursor.fetchall()
            # Prepare the data for display
           
            data.append((s[0], s[1], s[2], s[3], ', '.join([course[0] for course in courses])))
        headers = ["Student ID", "Name", "Age", "Email", "Registered Courses"] 
        self.create_display_treeview(headers, data,"student")

    def display_all_instructors(self):
        cursor.execute("SELECT * FROM instructors;")
        instructors = cursor.fetchall()
        data=[]
        for i in instructors:
            cursor.execute("SELECT course_id from courses where instructor_id = ?",(i[0],))
            courses = cursor.fetchall()
        # Prepare the data for display
            
            data.append((i[0], i[1], i[2], i[3], ', '.join([course[0] for course in courses])))
        headers = ["Instructor ID", "Name", "Age", "Email", "Courses Taught"]
        self.create_display_treeview(headers, data,"instructor")

    def display_all_courses(self):
        cursor.execute("SELECT * FROM courses;")
        courses = cursor.fetchall()
        data=[]
        for c in courses:
            cursor.execute("SELECT student_id from student_courses where course_id = ?",(c[0],))
            students = cursor.fetchall()
        # Prepare the data for display
            data.append((c[0], c[1], c[2], ', '.join([student[0] for student in students])))

        headers = ["Course ID", "Course Name", "Instructor ID", "Enrolled Students"]
        self.create_display_treeview(headers, data,"course")

     # Function to perform the search
    
    def perform_search(self):
        search_by = self.search_by_var.get()
        search_in = self.search_in_var.get()
        search_value = self.search_value_var.get()

        if not search_value:
            messagebox.showwarning("Warning", "Please enter a search value.")
            return

        # Load data based on the selected category (Student, Instructor, or Course)
        if search_in == "Student":

            
            if search_by == "ID":
                cursor.execute("SELECT * FROM students where student_id = ?;",(search_value,))
                students = cursor.fetchall()
            else:  # Search by Name
                cursor.execute("SELECT * FROM students where name = ?;",(search_value,))
                students = cursor.fetchall()

            if students:
                data=[]
                for s in students:
                    cursor.execute("SELECT course_id from student_courses where student_id  = ?",(s[0],))
                    courses = cursor.fetchall()
                    data.append((s[0], s[1], s[2], s[3], ', '.join([course[0] for course in courses])))

                headers = ["Student ID", "Name", "Age", "Email", "Registered Courses"] 
                self.create_display_treeview(headers, data,"student")
            else:
                messagebox.showinfo("No Results", "No student found.")

        elif search_in == "Instructor":
            if search_by == "ID":
                cursor.execute("SELECT * FROM instructors where instructor_id = ?;",(search_value,))
                instructors = cursor.fetchall()
            else:  # Search by Name
                cursor.execute("SELECT * FROM instructors where name = ?;",(search_value,))
                instructors = cursor.fetchall()

            if instructors:
                data=[]
                for i in instructors:
                    cursor.execute("SELECT course_id from courses where instructor_id = ?",(i[0],))
                    courses = cursor.fetchall()
                # Prepare the data for display
                    
                    data.append((i[0], i[1], i[2], i[3], ', '.join([course[0] for course in courses])))
                headers = ["Instructor ID", "Name", "Age", "Email", "Courses Taught"]
                self.create_display_treeview(headers, data,"instructor")

                  
            else:
                messagebox.showinfo("No Results", "No instructor found.")

        elif search_in == "Course":
            if search_by == "ID":
                cursor.execute("SELECT * FROM courses where course_id = ?;",(search_value,))
                courses = cursor.fetchall()
            else:  # Search by Name
                cursor.execute("SELECT * FROM courses where course_name = ?;",(search_value,))
                courses = cursor.fetchall()
            data=[]
            if courses:
                for c in courses:
                    cursor.execute("SELECT student_id from student_courses where course_id = ?",(c[0],))
                    students = cursor.fetchall()
                # Prepare the data for display
                    data.append((c[0], c[1], c[2], ', '.join([student[0] for student in students])))

                headers = ["Course ID", "Course Name", "Instructor ID", "Enrolled Students"]
                self.create_display_treeview(headers, data,"course")
            else:
                messagebox.showinfo("No Results", "No course found.")

    def delete_record(self, category):
        # Check if the treeview exists
        if not hasattr(self, 'tree'):
            messagebox.showerror("Error", "No records are currently being displayed.")
            return

        # Get the selected item from the treeview
        selected_item = self.tree.selection()  # Get selected item

        if not selected_item:
            messagebox.showwarning("Warning", f"No {category} selected for deletion.")
            return

        # Retrieve the ID from the selected item (assumed to be in the 4th column)
        selected_id = self.tree.item(selected_item)['values'][0]  # Get the selected ID
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this {category}?"):
            try:
                # Delete the record from the corresponding file
                if category == "student":
                    cursor.execute("DELETE FROM students where student_id = ?",(selected_id,))
                    conn.commit()
                elif category == "instructor":
                    cursor.execute("DELETE FROM instructors where instructor_id = ?",(selected_id,))
                    conn.commit()
                elif category == "course":
                    cursor.execute("DELETE FROM courses where course_id = ?",(selected_id,))
                    conn.commit()
                   

                messagebox.showinfo("Success", f"{category.capitalize()} record deleted successfully")
                if (category == "student"):
                    self.display_all_students()
                elif (category=="instructor"):
                    self.display_all_instructors()
                elif (category=="course"):
                        self.display_all_courses()  # Refresh the record list
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
     

    def save_edit(self, category):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Warning", f"No {category} selected for editing.")
            return

        selected_data = self.tree.item(selected_item)['values']

        # Clear the treeview and display editable fields
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Store the Entry widgets for each field to access the new values
        self.entry_fields = []
        labels = []

        if category == "student":
            fields_to_edit = ["Name", "Age", "Email"]
            # Assuming the indices for name, age, email are 0, 1, 2 (adjust based on your actual data structure)
            indices = [1, 2, 3]
        elif category == "instructor":
            fields_to_edit = ["Name", "Age", "Email"]
            # Assuming the indices for name, age, email are 0, 1, 2
            indices = [1, 2, 3]
        elif category == "course":
            fields_to_edit = ["Course Name"]
            # Assuming the index for the course name is 1 (adjust as needed)
            indices = [1]
        else:
            messagebox.showerror("Error", "Unknown category for editing.")
            return

        # Create labels and entry fields for the selected fields based on the category
        for idx, field in zip(indices, fields_to_edit):
            label = tk.Label(self.display_frame, text=field)
            label.pack()
            labels.append(label)

            entry = tk.Entry(self.display_frame)
            entry.insert(0, selected_data[idx])  # Pre-fill with the selected item's data
            entry.pack(padx=5, pady=5)
            self.entry_fields.append(entry)

        # Save the changes
        save_button = tk.Button(self.display_frame, text="Save Changes", command=lambda: self.save_changes(category, selected_data))
        save_button.pack(padx=5, pady=5)

        # Button to go back to the main menu
        tk.Button(self.display_frame, text="Back to Main Menu", command=self.show_main_menu).pack(side=tk.LEFT, padx=5, pady=10)

    def save_changes(self, category, original_data):
        # Get the updated data from the Entry fields
        id = original_data[0]
        updated_data = [entry.get() for entry in self.entry_fields]
        try:
            if category == "student":
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    age = int(updated_data[1])
                    assert (age >= 0), "Age cannot be negative"
                    email = updated_data[2]
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    assert(re.match(regex, email) is not None), "Wrong email format"
                    cursor.execute("UPDATE students SET name = ?, age = ?, email = ? where student_id = ?",(name,age,email,id,))
                    conn.commit()
            elif category == "instructor":
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    age = int(updated_data[1])
                    assert (age >= 0), "Age cannot be negative"
                    email = updated_data[2]
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    assert(re.match(regex, email) is not None), "Wrong email format"
                    cursor.execute("UPDATE instructors SET name = ?, age = ?, email = ? where instructor_id = ?",(name,age,email,id,))
                    conn.commit()
                   
            elif category == "course":
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    cursor.execute("UPDATE courses SET course_name = ? where course_id = ?",(name,id,))
                    conn.commit()
        except Exception as e:
             messagebox.showerror("Error "+str(e))
             return

        # Refresh the display after saving
        if category == "student":
            self.display_all_students()
        elif category == "instructor":
            self.display_all_instructors()
        elif category == "course":
            self.display_all_courses()

        messagebox.showinfo("Success", f"{category.capitalize()} updated successfully!")

    def load_courses_sql(self):
    
        try:
            cursor.execute("SELECT course_id FROM courses")
            courses_data = cursor.fetchall() 
            courses = [course[0] for course in courses_data]  
            return courses
        
        except sqlite3.Error as e:
            print(f"An error occurred while loading courses: {e}")
            return [] 

    

root = tk.Tk()
app = SchoolManagementApp(root)
root.mainloop()
