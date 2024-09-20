from PyQt5.QtWidgets import (
    QAbstractItemView, QTableView, QTableWidget, QTableWidgetItem, QComboBox, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt
import sys
import re
import csv
from datetime import datetime
import re
import sqlite3
conn = sqlite3.connect('../Database/schoolsystem.sqlite')
cursor = conn.cursor()

class SchoolManagementApp(QWidget):
    """
    Main application for managing students, instructors, and courses.

    This class serves as the main interface for the school management 
    system. It provides functionality to add, edit, and delete students, 
    instructors, and courses, as well as to display lists of these entities. 
    The application also handles database connections and operations.

    :param parent: The parent widget for the application (default is None).
    """
    def __init__(self):
        """
        Initializes the School Management System application.

        This method sets up the main window for the application, including the 
        title, geometry, and layout. It initializes a QStackedWidget to manage 
        multiple screens (e.g., main menu, forms, and views for students, 
        instructors, and courses). It adds all the necessary UI components and 
        displays the main menu by default.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        # Initialize StackedWidget to hold different frames
        self.stacked_widget = QStackedWidget(self)

        # Main Menu Frame
        self.main_menu_widget = QWidget()
        self.create_main_menu()

        # Student Form Frame
        self.student_widget = QWidget()
        self.create_student_form()

        # Instructor Form Frame
        self.instructor_widget = QWidget()
        self.create_instructor_form()

        # Course Form Frame
        self.course_widget = QWidget()
        self.create_course_form()

        # Register for Course Form Frame
        self.register_course_widget = QWidget()
        self.create_register_course_form()

        # Assign Instructor to Course Form Frame
        self.assign_instructor_widget = QWidget()
        self.create_assign_instructor_form()

        # Add new widgets for displaying all students, instructors, and courses
        self.display_students_widget = QWidget()
        self.create_display_students_view()

        self.display_instructors_widget = QWidget()
        self.create_display_instructors_view()

        self.display_courses_widget = QWidget()
        self.create_display_courses_view()

        # Search Frame
        self.search_widget = QWidget()
        self.create_search_form()

        # Add widgets to the stacked layout
        self.stacked_widget.addWidget(self.main_menu_widget)
        self.stacked_widget.addWidget(self.student_widget)
        self.stacked_widget.addWidget(self.instructor_widget)
        self.stacked_widget.addWidget(self.course_widget)
        self.stacked_widget.addWidget(self.register_course_widget)
        self.stacked_widget.addWidget(self.assign_instructor_widget)

        # Add new widgets for views and search
        self.stacked_widget.addWidget(self.display_students_widget)
        self.stacked_widget.addWidget(self.display_instructors_widget)
        self.stacked_widget.addWidget(self.display_courses_widget)
        self.stacked_widget.addWidget(self.search_widget)

        # Set the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Show main menu initially
        self.show_main_menu()

    def create_main_menu(self):
        """
        Creates the main menu user interface.

        This method creates the main menu with various buttons allowing users 
        to navigate between different functionalities, such as adding students, 
        instructors, courses, registering for courses, viewing records, 
        searching, and exporting data to CSV. Each button is linked to a specific 
        form or action in the application.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout()

        title_label = QLabel("School Management System", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        # Add buttons for navigating to different forms
        self.student_button = QPushButton("Add Student", self)
        self.student_button.clicked.connect(self.show_student_form)
        layout.addWidget(self.student_button)

        self.instructor_button = QPushButton("Add Instructor", self)
        self.instructor_button.clicked.connect(self.show_instructor_form)
        layout.addWidget(self.instructor_button)

        self.course_button = QPushButton("Add Course", self)
        self.course_button.clicked.connect(self.show_course_form)
        layout.addWidget(self.course_button)

        self.register_button = QPushButton("Register for Course", self)
        self.register_button.clicked.connect(self.show_register_course_form)
        layout.addWidget(self.register_button)

        self.assign_instructor_button = QPushButton("Assign Instructor", self)
        self.assign_instructor_button.clicked.connect(self.show_assign_instructor_form)
        layout.addWidget(self.assign_instructor_button)

            # New buttons for viewing all students, instructors, and courses
        self.view_students_button = QPushButton("View All Students", self)
        self.view_students_button.clicked.connect(self.display_all_students)
        layout.addWidget(self.view_students_button)

        self.view_instructors_button = QPushButton("View All Instructors", self)
        self.view_instructors_button.clicked.connect(self.display_all_instructors)
        layout.addWidget(self.view_instructors_button)

        self.view_courses_button = QPushButton("View All Courses", self)
        self.view_courses_button.clicked.connect(self.display_all_courses)
        layout.addWidget(self.view_courses_button)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.show_search_form)
        layout.addWidget(self.search_button)

            # Export to CSV button
        self.export_csv_button = QPushButton("Export to CSV", self)
        self.export_csv_button.clicked.connect(self.export_to_csv)
        layout.addWidget(self.export_csv_button)


        # Set layout for the main menu widget
        self.main_menu_widget.setLayout(layout)

    def create_student_form(self):
        """
        Creates the form to add a new student.

        This method generates a user interface for adding students. It provides 
        input fields for the student's name, age, email, and student ID, along 
        with buttons for submitting the data or returning to the main menu. 
        Validation is performed on the input before submission.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout()

        title_label = QLabel("Add Student", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(title_label)

        # Fields
        self.student_name_field = QLineEdit(self)
        self.student_name_field.setPlaceholderText("Name")
        layout.addWidget(self.student_name_field)

        self.student_age_field = QLineEdit(self)
        self.student_age_field.setPlaceholderText("Age")
        layout.addWidget(self.student_age_field)

        self.student_email_field = QLineEdit(self)
        self.student_email_field.setPlaceholderText("Email")
        layout.addWidget(self.student_email_field)

        self.student_id_field = QLineEdit(self)
        self.student_id_field.setPlaceholderText("Student ID")
        layout.addWidget(self.student_id_field)

        # Add button to submit
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self.add_student)
        layout.addWidget(add_button)

        # Back button
        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the student widget
        self.student_widget.setLayout(layout)

    def create_instructor_form(self):
        """
        Creates the form to add a new instructor.

        This method generates a user interface for adding instructors. It provides 
        input fields for the instructor's name, age, email, and instructor ID, 
        along with buttons to submit the form and return to the main menu. 
        Input validation is performed to ensure data correctness.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout()

        title_label = QLabel("Add Instructor", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(title_label)

        # Fields
        self.instructor_name_field = QLineEdit(self)
        self.instructor_name_field.setPlaceholderText("Name")
        layout.addWidget(self.instructor_name_field)

        self.instructor_age_field = QLineEdit(self)
        self.instructor_age_field.setPlaceholderText("Age")
        layout.addWidget(self.instructor_age_field)

        self.instructor_email_field = QLineEdit(self)
        self.instructor_email_field.setPlaceholderText("Email")
        layout.addWidget(self.instructor_email_field)

        self.instructor_id_field = QLineEdit(self)
        self.instructor_id_field.setPlaceholderText("Instructor ID")
        layout.addWidget(self.instructor_id_field)

        # Add button to submit
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self.add_instructor)
        layout.addWidget(add_button)

        # Back button
        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the instructor widget
        self.instructor_widget.setLayout(layout)

    def create_course_form(self):
        """
        Creates the form to add a new course.

        This method generates a user interface for adding new courses. It provides 
        input fields for the course ID and course name. A button is included for 
        submitting the form data, which validates the input before storing the 
        course information.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout()

        title_label = QLabel("Add Course", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(title_label)

        # Fields
        self.course_id_field = QLineEdit(self)
        self.course_id_field.setPlaceholderText("Course ID")
        layout.addWidget(self.course_id_field)

        self.course_name_field = QLineEdit(self)
        self.course_name_field.setPlaceholderText("Course Name")
        layout.addWidget(self.course_name_field)

        # Add button to submit
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self.add_course)
        layout.addWidget(add_button)

        # Back button
        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the course widget
        self.course_widget.setLayout(layout)

    def create_register_course_form(self):
        """
        Creates the form to register a student for a course.

        This method generates a user interface that allows students to register 
        for courses. The form includes fields for the student ID and a dropdown 
        list of available courses. A button for registration and another for 
        returning to the main menu are included.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout(self.register_course_widget)

        register_course_label = QLabel("Register for Course", self)
        register_course_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(register_course_label)

        self.register_student_id_field = QLineEdit(self)
        self.register_student_id_field.setPlaceholderText("Student ID")
        layout.addWidget(self.register_student_id_field)

        self.register_course_dropdown = QComboBox(self)
        self.load_courses_into_dropdown(self.register_course_dropdown)
        layout.addWidget(self.register_course_dropdown)

        register_button = QPushButton("Register", self)
        register_button.clicked.connect(self.register_student_for_course)
        layout.addWidget(register_button)

        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)
    
    def create_assign_instructor_form(self):
        """
        Creates the form to assign an instructor to a course.

        This method generates a user interface that allows assigning instructors 
        to courses. It includes input fields for the instructor ID and a dropdown 
        list of available courses. Buttons for assigning the instructor and 
        returning to the main menu are also included.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout(self.assign_instructor_widget)

        assign_instructor_label = QLabel("Assign Instructor to Course", self)
        assign_instructor_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(assign_instructor_label)

        self.assign_instructor_id_field = QLineEdit(self)
        self.assign_instructor_id_field.setPlaceholderText("Instructor ID")
        layout.addWidget(self.assign_instructor_id_field)

        self.assign_course_dropdown = QComboBox(self)
        self.load_courses_into_dropdown(self.assign_course_dropdown)
        layout.addWidget(self.assign_course_dropdown)

        assign_button = QPushButton("Assign", self)
        assign_button.clicked.connect(self.assign_instructor_to_course)
        layout.addWidget(assign_button)

        back_button = QPushButton("Back to Main Menu", self)
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

    def create_display_students_view(self):      
        """
        Displays the table view of all students.

        This method creates a table view that lists all students stored in the 
        system. It fetches student data from the database and uses a QTableView 
        to present the information. A back button is included to return to the 
        main menu.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.display_all_students()  # This will fetch the data and call create_display_table

    def create_display_instructors_view(self):
        """
        Displays the table view of all instructors.

        This method creates a table view that lists all instructors stored in the 
        system. It fetches instructor data from the database and uses a QTableView 
        to display the information. A back button is included to return to the 
        main menu.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout()

        # Create table view to display instructors
        self.instructors_table = QTableView()
        layout.addWidget(self.instructors_table)

        # Back to Main Menu button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the widget
        self.display_instructors_widget.setLayout(layout)

    def create_display_courses_view(self):
        """
        Displays the table view of all courses.

        This method creates a table view that lists all courses available in the 
        system. It fetches course data from the database and uses a QTableView 
        to present the information. A back button is included to return to the 
        main menu.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        layout = QVBoxLayout()

        # Create table view to display courses
        self.courses_table = QTableView()
        layout.addWidget(self.courses_table)

        # Back to Main Menu button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the widget
        self.display_courses_widget.setLayout(layout)

    def show_main_menu(self):
        """
        Displays the main menu.

        This method sets the current widget to the main menu widget, allowing the
        user to navigate to different parts of the application from the main menu.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    def show_student_form(self):
        """
        Displays the student form.

        This method switches the current widget to the student form widget, where 
        users can add or view student information.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.student_widget)

    def show_instructor_form(self):
        """
        Displays the instructor form.

        This method switches the current widget to the instructor form widget, 
        allowing users to add or view instructor details.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.instructor_widget)

    def show_course_form(self):
        """
        Displays the course form.

        This method switches the current widget to the course form widget, where 
        users can add or manage courses in the system.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.course_widget)

    def show_register_course_form(self):
        """
        Displays the course registration form.

        This method refreshes the available courses list and switches the current 
        widget to the course registration form, where students can register for courses.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.refresh_courses()
        self.stacked_widget.setCurrentWidget(self.register_course_widget)

    def show_assign_instructor_form(self):
        """
        Displays the instructor assignment form.

        This method refreshes the list of available courses and switches the current 
        widget to the instructor assignment form, allowing administrators to assign 
        instructors to courses.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.refresh_courses()
        self.stacked_widget.setCurrentWidget(self.assign_instructor_widget)
     
    def show_display_students(self):
        """
        Displays the student records view.

        This method switches the current widget to the view displaying the list of 
        all students in the system.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.display_students_widget)

    def show_display_instructors(self):
        """
        Displays the instructor records view.

        This method switches the current widget to the view displaying the list of 
        all instructors in the system.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.display_instructors_widget)

    def show_display_courses(self):
        """
        Displays the course records view.

        This method switches the current widget to the view displaying the list of 
        all courses available in the system.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.display_courses_widget)

    def show_search_form(self):
        """
        Displays the search form.

        This method switches the current widget to the search form, allowing the 
        user to search for students, instructors, or courses within the system.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.stacked_widget.setCurrentWidget(self.search_widget)
    
    # Event handlers for adding a Student
    def add_student(self):
        """
        Adds a student to the system.

        This method collects input data (name, age, email, student ID) from the 
        student form, validates it, and then inserts the student record into the 
        database. If validation fails or an error occurs during insertion, an error 
        message is shown.

        :raises AssertionError: If any field is invalid or empty.
        :raises Exception: If there's any database or validation error.
        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        name = self.student_name_field.text()
        age = self.student_age_field.text()
        email = self.student_email_field.text()
        student_id = self.student_id_field.text()

        # Simple validation
        if name and age and email and student_id:
            try:
                assert(student_id.strip() != ""), "student_id cannot be empty"
                assert re.match(r"^[a-zA-Z0-9]+$", student_id), "student_id must contain only alphanumeric characters"
                assert (type(name) == str), "Name must be a string" 
                assert(name.strip() != ""), "name cannot be empty"
                assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                age = int(age)
                assert (age >= 0), "Age cannot be negative"
                regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                assert(re.match(regex, email) is not None), "Wrong email format"
                cursor.execute("INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)", (student_id, name, age, email))
                conn.commit()
                QMessageBox.information(self, "Success", "Student added successfully")
                self.clear_student_fields()
                self.show_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled")

    def clear_student_fields(self):
        """
        Clears the student form fields.

        This method resets the input fields (name, age, email, and student ID) in the
        student form, making them ready for the next entry.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.student_name_field.clear()
        self.student_age_field.clear()
        self.student_email_field.clear()
        self.student_id_field.clear()

    # Event handlers for adding an Instructor
    def add_instructor(self):
        """
        Adds an instructor to the system.

        This method collects input data (name, age, email, instructor ID) from the 
        instructor form, validates it, and then inserts the instructor record into 
        the database. If validation fails or an error occurs during insertion, an 
        error message is shown.

        :raises AssertionError: If any field is invalid or empty.
        :raises Exception: If there's any database or validation error.
        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        name = self.instructor_name_field.text()
        age = self.instructor_age_field.text()
        email = self.instructor_email_field.text()
        instructor_id = self.instructor_id_field.text()

        # Simple validation
        if name and age and email and instructor_id:
            try:
                assert(instructor_id.strip() != ""), "student_id cannot be empty"
                assert re.match(r"^[a-zA-Z0-9]+$", instructor_id), "student_id must contain only alphanumeric characters"
               
                assert (type(name) == str), "Name must be a string" 
                assert(name.strip() != ""), "name cannot be empty"
                assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                age = int(age)
                assert (age >= 0), "Age cannot be negative"
                regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                assert(re.match(regex, email) is not None), "Wrong email format"
                cursor.execute("INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)", (instructor_id, name, age, email))
                conn.commit()
                QMessageBox.information(self, "Success", "Instructor added successfully")
                self.clear_instructor_fields()
                self.show_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled")

    def clear_instructor_fields(self):
        """
        Clears the instructor form fields.

        This method resets the input fields (name, age, email, and instructor ID) in the
        instructor form, making them ready for the next entry.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.instructor_name_field.clear()
        self.instructor_age_field.clear()
        self.instructor_email_field.clear()
        self.instructor_id_field.clear()

    # Event handlers for adding a Course
    def add_course(self):
        """
        Adds a course to the system.

        This method collects input data (course ID and course name) from the course 
        form, validates it, and then inserts the course record into the database. 
        If validation fails or an error occurs during insertion, an error message is shown.

        :raises AssertionError: If any field is invalid or empty.
        :raises Exception: If there's any database or validation error.
        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        course_id = self.course_id_field.text()
        course_name = self.course_name_field.text()

        # Simple validation
        if course_id and course_name:
            
            try:
                assert (type(course_name) == str), "Name must be a string" 
                assert(course_name.strip() != ""), "name cannot be empty"
                assert re.match(r"^[a-zA-Z\s]+$", course_name), "Name must contain only alphabetic characters and spaces"
                assert(course_id.strip() != ""), "student_id cannot be empty"
                assert re.match(r"^[a-zA-Z0-9]+$", course_id), "student_id must contain only alphanumeric characters"
               
                cursor.execute("INSERT INTO courses (course_id, course_name) VALUES (?, ?)", (course_id, course_name))
                conn.commit()
                QMessageBox.information(self, "Success", "Course added successfully")
                self.clear_course_fields()
                self.show_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled")

    def clear_course_fields(self):
        """
        Clears the course form fields.

        This method resets the input fields (course ID and course name) in the course form, 
        making them ready for the next entry.

        :param None: This function does not accept parameters.
        :returns: None
        :rtype: None
        """
        self.course_id_field.clear()
        self.course_name_field.clear()

    # Load available courses into the dropdown
    def load_courses_into_dropdown(self, dropdown):
        """
        Loads available courses into a dropdown menu.

        Queries the database for all course IDs and populates the given dropdown menu with them.
        If no courses are found, it adds a "No available courses" message.

        :param dropdown: The dropdown widget to populate with course data.
        :type dropdown: QComboBox
        :raises sqlite3.Error: If there's a problem querying the database.
        :returns: None
        """
        dropdown.clear()
        try:
            cursor.execute("SELECT course_id FROM courses")
            courses_data = cursor.fetchall() 
            courses = [course[0] for course in courses_data]  
           
        
        except sqlite3.Error as e:
            print(f"An error occurred while loading courses: {e}")
            courses=[] 
        if courses:
            for course in courses:
                dropdown.addItem(course)
        else:
            dropdown.addItem("No available courses")

    # Register student for course
    def register_student_for_course(self):
        """
        Registers a student for a selected course.

        Performs validation to ensure both student ID and course ID are valid,
        then registers the student in the `student_courses` table.

        :raises sqlite3.Error: If there's an issue with database operations.
        :returns: None
        """
        student_id = self.register_student_id_field.text()
        selected_course_id = self.register_course_dropdown.currentText()
        if not student_id or not selected_course_id:
             QMessageBox.warning(self, "Warning", "Please fill in all fields")
        # Simple validation
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
                    QMessageBox.information(self, "Success", "Student registered for the course successfully")
                    self.show_register_course_form()  # Refresh form
                else:
                    QMessageBox.critical(self, "Error", "Student or Course not found")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
      
    # Assign instructor to course
    def assign_instructor_to_course(self):
        """
        Assigns an instructor to a selected course.

        Performs validation to ensure both instructor ID and course ID are valid,
        and that no instructor is already assigned to the course. Then updates the course with the new instructor.

        :raises sqlite3.Error: If there's an issue with database operations.
        :returns: None
        """
        instructor_id = self.assign_instructor_id_field.text()
        selected_course_id = self.assign_course_dropdown.currentText()
        if not instructor_id or not selected_course_id:
             QMessageBox.warning(self, "Warning", "Please fill in all fields")
        # Simple validation
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
                    QMessageBox.information(self, "Success", f"Instructor  assigned to course successfully")
                    self.show_assign_instructor_form()  # Refresh form
                else:
                    QMessageBox.critical(self, "Error", "Instructor or Course not found or already there is an instructor")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
      
           

    # Create display table function for students, instructors, and courses
    def create_display_table(self, headers, data, category):
        """
        Creates a display table for students, instructors, or courses.

        This function creates a table and populates it with data. It also provides
        Edit, Delete, and Back buttons to manage records.

        :param headers: The column headers for the table.
        :type headers: list[str]
        :param data: The table's data to be displayed.
        :type data: list[tuple]
        :param category: The type of entity being displayed (student, instructor, or course).
        :type category: str
        :returns: None
        """
        display_widget = QWidget()  # Create a new widget for the table and controls
        layout = QVBoxLayout()

        # Create the table and populate it with data
        self.display_table = QTableWidget()
        self.display_table.setRowCount(len(data))
        self.display_table.setColumnCount(len(headers))
        self.display_table.setHorizontalHeaderLabels(headers)
        self.display_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make item non-editable
                self.display_table.setItem(row_index, col_index, item)

        layout.addWidget(self.display_table)
        # Add Edit and Delete buttons
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.save_edit(category))  # Handles edit logic
        layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_record(category))  # Handles delete logic
        layout.addWidget(delete_button)

        # Add a Back to Main Menu button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the display widget
        display_widget.setLayout(layout)

        # Add the new widget to the stacked widget and display it
        self.stacked_widget.addWidget(display_widget)
        self.stacked_widget.setCurrentWidget(display_widget)

    # Display all students, instructors, courses
    def display_all_students(self):
        """
        Displays all students with their registered courses.

        Fetches student data from the database and compiles a list of courses each student is registered for.
        The result is displayed in a table format.

        :returns: None
        """
        cursor.execute("SELECT * FROM students;")
        students = cursor.fetchall()
        data=[]
        for s in students:
            #print(s[0])
            cursor.execute("SELECT course_id from student_courses where student_id  = ?",(s[0],))
            courses = cursor.fetchall()
            # Prepare the data for display
           
            data.append((s[0], s[1], s[2], s[3], ', '.join([course[0] for course in courses])))
        headers = ["Student ID", "Name", "Age", "Email", "Registered Courses"] 
        self.create_display_table(headers, data,"student")

    def display_all_instructors(self):
        """
        Displays all instructors with the courses they teach.

        Fetches instructor data from the database and compiles a list of courses each instructor teaches.
        The result is displayed in a table format.

        :returns: None
        """
        cursor.execute("SELECT * FROM instructors;")
        instructors = cursor.fetchall()
        data=[]
        for i in instructors:
            cursor.execute("SELECT course_id from courses where instructor_id = ?",(i[0],))
            courses = cursor.fetchall()
        # Prepare the data for display
            
            data.append((i[0], i[1], i[2], i[3], ', '.join([course[0] for course in courses])))
        headers = ["Instructor ID", "Name", "Age", "Email", "Courses Taught"]
        self.create_display_table(headers, data,"instructor")

    def display_all_courses(self):
        """
        Displays all courses along with their enrolled students.

        Fetches course data from the database and compiles a list of students enrolled in each course.
        The result is displayed in a table format.

        :returns: None
        """
        cursor.execute("SELECT * FROM courses;")
        courses = cursor.fetchall()
        data=[]
        for c in courses:
            cursor.execute("SELECT student_id from student_courses where course_id = ?",(c[0],))
            students = cursor.fetchall()
        # Prepare the data for display
            data.append((c[0], c[1], c[2], ', '.join([student[0] for student in students])))

        headers = ["Course ID", "Course Name", "Instructor ID", "Enrolled Students"]
        self.create_display_table(headers, data,"course")

     # Function to perform the search
 
    # Search functionality
    def create_search_form(self):
        """
        Creates a form to search for students, instructors, or courses.

        Provides dropdowns to choose search criteria (ID or Name) and the category to search (Student, Instructor, or Course).
        Includes an input field for entering the search value.

        :returns: None
        """
        layout = QVBoxLayout()

        search_by_label = QLabel("Search By")
        layout.addWidget(search_by_label)

        # Dropdown to select search by (ID or Name)
        self.search_by_dropdown = QComboBox()
        self.search_by_dropdown.addItems(["ID", "Name"])
        layout.addWidget(self.search_by_dropdown)

        search_in_label = QLabel("Search In")
        layout.addWidget(search_in_label)

        # Dropdown to select search in (Student, Instructor, Course)
        self.search_in_dropdown = QComboBox()
        self.search_in_dropdown.addItems(["Student", "Instructor", "Course"])
        layout.addWidget(self.search_in_dropdown)

        # Search value input
        self.search_value_input = QLineEdit()
        self.search_value_input.setPlaceholderText("Enter value to search")
        layout.addWidget(self.search_value_input)

        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        # Back to Main Menu button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

        # Set layout for the search widget
        self.search_widget.setLayout(layout)

    def perform_search(self):
        """
        Performs a search for students, instructors, or courses based on user input.

        Queries the database based on selected category and search criteria (ID or Name),
        and displays the results in a table.

        :raises sqlite3.Error: If there's an issue with database operations.
        :returns: None
        """
        search_by = self.search_by_dropdown.currentText()
        search_in = self.search_in_dropdown.currentText()
        search_value = self.search_value_input.text()

        if not search_value:
            QMessageBox.warning(self, "Warning", "Please enter a search value.")
            return

        # Perform search based on category and search_by
       
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
                self.create_display_table(headers, data,"student") 
            else:
                QMessageBox.information(self, "No Results", "No student found.")

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
                    self.create_display_table(headers, data,"instructor")

            else:
                QMessageBox.information(self, "No Results", "No instructor found.")

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
                self.create_display_table(headers, data,"course")
            else:
                QMessageBox.information(self,"No Results", "No course found.")

    def save_edit(self, category):
        """
        Saves edits made to a student, instructor, or course record.

        Opens an edit dialog for the selected record, allowing users to make changes.
        After saving, it refreshes the relevant table display.

        :param category: The type of entity being edited (student, instructor, or course).
        :type category: str
        :returns: None
        """
        selected_items = self.display_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", f"No {category} selected for editing.")
            return
        # Get the selected row
        selected_row = self.display_table.currentRow()
        if selected_row == -1:  # Check if a row is actually selected
            QMessageBox.warning(self, "Warning", f"No {category} selected for deletion.")
            return

        selected_data = [item.text() for item in selected_items]
        dialog = EditDialog(category, selected_data, self)
        if dialog.exec_() == QDialog.Accepted:
            if category == "student":
                self.display_all_students()
            elif category == "instructor":
                self.display_all_instructors()
            elif category == "course":
                self.display_all_courses()

    def delete_record(self, category):
        """
        Deletes a student, instructor, or course record.

        Prompts the user for confirmation, and if confirmed, deletes the selected record
        from the database and refreshes the relevant table display.

        :param category: The type of entity being deleted (student, instructor, or course).
        :type category: str
        :raises sqlite3.Error: If there's an issue with database operations.
        :returns: None
        """
        selected_items = self.display_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", f"No {category} selected for deletion.")
            return
        # Get the selected row
        selected_row = self.display_table.currentRow()
        if selected_row == -1:  # Check if a row is actually selected
            QMessageBox.warning(self, "Warning", f"No {category} selected for deletion.")
            return
       
        selected_id = selected_items[0].text()
       


       
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete this {category}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if category == "student":
                    cursor.execute("DELETE FROM students where student_id = ?",(selected_id,))
                    conn.commit()
                elif category == "instructor":
                    cursor.execute("DELETE FROM instructors where instructor_id = ?",(selected_id,))
                    conn.commit()
                elif category == "course":
                    cursor.execute("DELETE FROM courses where course_id = ?",(selected_id,))
                    conn.commit()
                    

                QMessageBox.information(self, "Success", f"{category.capitalize()} deleted successfully!")
                if category == "student":
                    self.display_all_students()
                elif category == "instructor":
                    self.display_all_instructors()
                elif category == "course":
                    self.display_all_courses()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
       
    def refresh_courses(self):
        """
        Refreshes the course dropdowns for registering students or assigning instructors.

        Reloads available courses into the `assign_course_dropdown` and `register_course_dropdown` widgets.

        :returns: None
        """
        self.load_courses_into_dropdown(self.assign_course_dropdown)
        self.load_courses_into_dropdown(self.register_course_dropdown)

    def load_courses_from_db(self):
        """
        Loads course data from the database.

        Retrieves course details, including the course name, ID, instructor information, and enrolled students.

        :returns: list[tuple]: A list of course data, including course name, ID, instructor email, instructor ID, and enrolled students.
        """
        cursor.execute("""
            SELECT c.course_name, c.course_id, i.email, i.instructor_id,
            GROUP_CONCAT(sc.student_id) as enrolled_students
            FROM courses c
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            LEFT JOIN student_courses sc ON sc.course_id = c.course_id
            GROUP BY c.course_id;
        """)
        return cursor.fetchall()

    def load_instructors_from_db(self):
        """
        Loads instructor data from the database.

        Retrieves instructor details, including the instructor's name, age, email, and courses assigned to them.

        :returns: list[tuple]: A list of instructor data, including name, age, email, instructor ID, and assigned courses.
        """
        cursor.execute("""
            SELECT i.name, i.age, i.email, i.instructor_id,
            GROUP_CONCAT(c.course_id) as assigned_courses
            FROM instructors i
            LEFT JOIN courses c ON c.instructor_id = i.instructor_id
            GROUP BY i.instructor_id;
        """)
        return cursor.fetchall()

    def load_students_from_db(self):
        """
        Loads student data from the database.

        Retrieves student details, including the student's name, age, email, and registered courses.

        :returns: list[tuple]: A list of student data, including name, age, email, student ID, and registered courses.
        """
        cursor.execute("""
            SELECT s.name, s.age, s.email, s.student_id,
            GROUP_CONCAT(sc.course_id) as registered_courses
            FROM students s
            LEFT JOIN student_courses sc ON sc.student_id = s.student_id
            GROUP BY s.student_id;
        """)
        return cursor.fetchall()

    def export_to_csv(self):
        """
        Exports data for students, instructors, and courses to CSV files.

        Fetches the relevant data from the database and exports them into separate CSV files for students, instructors, and courses.
        Filenames include a timestamp for uniqueness.

        :raises Exception: If an error occurs during data export.
        :returns: None
        """
        try:
            # Get current timestamp for filenames
            timestamp = datetime.now().strftime("%f")
            
            # Define filenames for each type
            filenames = {
                'students': f"CSV/students_{timestamp}.csv",
                'instructors': f"CSV/instructors_{timestamp}.csv",
                'courses': f"CSV/courses_{timestamp}.csv"
            }

            # Export courses
            courses = self.load_courses_from_db()  # Updated to fetch data from DB
            self.export_data(filenames['courses'], courses, 
                            ['Course Name', 'Course ID', 'Instructor Email', 'Instructor ID', 'Enrolled Students'], 
                            lambda course: {
                                'Course Name': course[0],
                                'Course ID': course[1],
                                'Instructor Email': course[2] if course[2] else '',
                                'Instructor ID': course[3] if course[3] else '',
                                'Enrolled Students': course[4]
                            })

            # Export instructors
            instructors = self.load_instructors_from_db()  # Updated to fetch data from DB
            self.export_data(filenames['instructors'], instructors,
                            ['Name', 'Age', 'Email', 'Instructor ID', 'Assigned Courses'],
                            lambda instructor: {
                                'Name': instructor[0],
                                'Age': instructor[1],
                                'Email': instructor[2],
                                'Instructor ID': instructor[3],
                                'Assigned Courses': instructor[4]
                            })

            # Export students
            students = self.load_students_from_db()  # Updated to fetch data from DB
            self.export_data(filenames['students'], students,
                            ['Name', 'Age', 'Email', 'Student ID', 'Registered Courses'],
                            lambda student: {
                                'Name': student[0],
                                'Age': student[1],
                                'Email': student[2],
                                'Student ID': student[3],
                                'Registered Courses': student[4]
                            })

            # Show success message
            self.show_message_box("Success", "Data successfully exported to CSV files.", QMessageBox.Information)

        except Exception as e:
            # Show error message if something goes wrong
            self.show_message_box("Error", f"Failed to export data: {str(e)}", QMessageBox.Critical)

    def export_data(self, filename, data, fieldnames, row_mapper):
        """
        Exports a list of data to a CSV file.

        Writes the data to a CSV file with the specified fieldnames and uses the provided row_mapper
        to convert data rows into dictionaries.

        :param filename: The file path for the CSV file.
        :type filename: str
        :param data: The data to be written to the CSV file.
        :type data: list[tuple]
        :param fieldnames: The header names for the CSV file.
        :type fieldnames: list[str]
        :param row_mapper: A function that maps a data tuple to a dictionary for CSV export.
        :type row_mapper: function
        :returns: None
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(row_mapper(item))

    # Helper function to show message boxes
    def show_message_box(self, title, message, icon_type):
        """
        Displays a message box with the given title, message, and icon type.

        :param title: The title of the message box.
        :type title: str
        :param message: The message to display in the box.
        :type message: str
        :param icon_type: The icon type (information, warning, or critical).
        :type icon_type: QMessageBox.Icon
        :returns: None
        """
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon_type)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class EditDialog(QDialog):
    """
    Dialog for editing student, instructor, or course information.

    This dialog allows users to modify the details of a selected entity 
    (student, instructor, or course). It presents input fields based on 
    the specified category and includes functionality to validate and 
    update the data in the database.

    :param category: The category of the item to be edited (e.g., "student", "instructor", "course").
    :param data: The original data of the item to be edited, which is displayed in the input fields.
    :param parent: The parent widget for the dialog (default is None).
    """
    def __init__(self, category, data, parent=None):
        """
        Initializes the EditDialog.

        :param category: The category of the item to be edited.
        :param data: The original data of the item to be edited.
        :param parent: The parent widget for the dialog.
        """
        super().__init__(parent)
        self.setWindowTitle(f"Edit {category.capitalize()}")
        self.category = category
        self.original_data = data
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface for the edit dialog.

        This method sets up the layout and input fields based on the selected
        category (student, instructor, or course). It includes buttons for 
        saving changes and going back to the previous screen.

        :raises QMessageBox: If an unknown category is provided.
        """
        layout = QFormLayout()

        # Create and populate fields based on category
        self.fields = {}
        if self.category == "student":
            labels = ["Name", "Age", "Email"]
            indices = [1,2,3]
        elif self.category == "instructor":
            labels = ["Name", "Age", "Email"]
            indices = [1,2,3]
        elif self.category == "course":
            labels = ["Course Name"]
            indices = [1]
        else:
            QMessageBox.critical(self, "Error", "Unknown category for editing.")
            self.reject()
            return

        for label, index in zip(labels, indices):
            layout.addRow(QLabel(label), self.create_line_edit(self.original_data[index]))

        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        layout.addRow(save_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.reject)  # Close dialog
        layout.addRow(back_button)

        self.setLayout(layout)

    def create_line_edit(self, text):
        """
        Creates a line edit widget pre-populated with text.

        :param text: The text to display in the line edit.
        :return: A QLineEdit widget.
        """
        line_edit = QLineEdit()
        line_edit.setText(text)
        self.fields[text] = line_edit
        return line_edit

    def save_changes(self):
        """
         Save the changes made in the dialog and update the database.

        This method validates the input data based on the selected category
        and updates the corresponding record in the database. Validations include:
        
        - For students and instructors:
          - Name must be a non-empty string containing only alphabetic characters.
          - Age must be a non-negative integer.
          - Email must follow a valid format.
        
        - For courses:
          - Course name must be a non-empty string.

        Displays a success message upon successful update, or an error message 
        if validation fails or an error occurs during the database operation.

        :raises Exception: If there is an error during the database update.
        :return: None
        """
        try:
            updated_data = [field.text() for field in self.fields.values()]
            id = self.original_data[0]
            if self.category == "student":
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
            elif self.category == "instructor":
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
                   
            elif self.category == "course":
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    cursor.execute("UPDATE courses SET course_name = ? where course_id = ?",(name,id,))
                    conn.commit()

            QMessageBox.information(self, "Success", f"{self.category.capitalize()} updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def main():
    """
    Run the main application.

    This function initializes the QApplication, creates the main window,
    and starts the application event loop. The application will exit when
    the main window is closed.

    :returns: None
    """
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()