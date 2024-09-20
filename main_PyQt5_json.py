from PyQt5.QtWidgets import (
    QAbstractItemView, QTableView, QTableWidget, QTableWidgetItem, QComboBox, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from Classes.course import Course
from Classes.instructor import Instructor
from Classes.student import Student
import sys
import re
import csv
from datetime import datetime
import os
import json

class SchoolManagementApp(QWidget):
    def __init__(self):
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
        """Creates the main menu UI."""
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
        """Creates the form to add a student."""
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
        """Creates the form to add an instructor."""
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
        """Creates the form to add a course."""
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
        """Calls display_all_students, which uses create_display_table to show the student list."""
        self.display_all_students()  # This will fetch the data and call create_display_table

    def create_display_instructors_view(self):
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
        """Display the main menu."""
        self.stacked_widget.setCurrentWidget(self.main_menu_widget)

    def show_student_form(self):
        """Display the student form."""
        self.stacked_widget.setCurrentWidget(self.student_widget)

    def show_instructor_form(self):
        """Display the instructor form."""
        self.stacked_widget.setCurrentWidget(self.instructor_widget)

    def show_course_form(self):
        """Display the course form."""
        self.stacked_widget.setCurrentWidget(self.course_widget)

    def show_register_course_form(self):
        self.refresh_courses()
        self.stacked_widget.setCurrentWidget(self.register_course_widget)

    def show_assign_instructor_form(self):
        self.refresh_courses()
        self.stacked_widget.setCurrentWidget(self.assign_instructor_widget)
     
    def show_display_students(self):
        self.stacked_widget.setCurrentWidget(self.display_students_widget)

    def show_display_instructors(self):
        self.stacked_widget.setCurrentWidget(self.display_instructors_widget)

    def show_display_courses(self):
        self.stacked_widget.setCurrentWidget(self.display_courses_widget)

    def show_search_form(self):
        self.stacked_widget.setCurrentWidget(self.search_widget)
    
    # Event handlers for adding a Student
    def add_student(self):
        name = self.student_name_field.text()
        age = self.student_age_field.text()
        email = self.student_email_field.text()
        student_id = self.student_id_field.text()

        # Simple validation
        if name and age and email and student_id:
            try:
                student = Student(name, int(age), email, student_id, [])
                student.save_to_file('Storage/students.json')
                QMessageBox.information(self, "Success", "Student added successfully")
                self.clear_student_fields()
                self.show_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled")

    def clear_student_fields(self):
        """Clears the input fields in the student form."""
        self.student_name_field.clear()
        self.student_age_field.clear()
        self.student_email_field.clear()
        self.student_id_field.clear()

    # Event handlers for adding an Instructor
    def add_instructor(self):
        """Handles adding an instructor."""
        name = self.instructor_name_field.text()
        age = self.instructor_age_field.text()
        email = self.instructor_email_field.text()
        instructor_id = self.instructor_id_field.text()

        # Simple validation
        if name and age and email and instructor_id:
            try:
                instructor = Instructor(name, int(age), email, instructor_id, [])
                instructor.save_to_file('Storage/instructors.json')
                QMessageBox.information(self, "Success", "Instructor added successfully")
                self.clear_instructor_fields()
                self.show_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled")

    def clear_instructor_fields(self):
        """Clears the input fields in the instructor form."""
        self.instructor_name_field.clear()
        self.instructor_age_field.clear()
        self.instructor_email_field.clear()
        self.instructor_id_field.clear()

    # Event handlers for adding a Course
    def add_course(self):
        """Handles adding a course."""
        course_id = self.course_id_field.text()
        course_name = self.course_name_field.text()

        # Simple validation
        if course_id and course_name:
            try:
                course = Course(course_id, course_name, None, [])
                course.save_to_file('Storage/courses.json')
                QMessageBox.information(self, "Success", "Course added successfully")
                self.clear_course_fields()
                self.show_main_menu()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "All fields must be filled")

    def clear_course_fields(self):
        """Clears the input fields in the course form."""
        self.course_id_field.clear()
        self.course_name_field.clear()

    # Load available courses into the dropdown
    def load_courses_into_dropdown(self, dropdown):
        dropdown.clear()
        courses = Course.load_all_courses('Storage/courses.json')
        if courses:
            for course in courses:
                dropdown.addItem(course)
        else:
            dropdown.addItem("No available courses")

    # Register student for course
    def register_student_for_course(self):
        student_id = self.register_student_id_field.text()
        selected_course_id = self.register_course_dropdown.currentText()

        # Simple validation
        if student_id and selected_course_id:
            try:
                student = Student.load_student_by_id('Storage/students.json', student_id)
                course = Course.load_course_by_id('Storage/courses.json', selected_course_id)
                if student and course:
                    student.register_course(course)
                    QMessageBox.information(self, "Success", "Student registered for the course successfully")
                    self.show_register_course_form()  # Refresh form
                else:
                    QMessageBox.critical(self, "Error", "Student or Course not found")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            
            QMessageBox.warning(self, "Warning", "Please fill in all fields")

    # Assign instructor to course
    def assign_instructor_to_course(self):
        instructor_id = self.assign_instructor_id_field.text()
        selected_course_id = self.assign_course_dropdown.currentText()

        # Simple validation
        if instructor_id and selected_course_id:
            try:
                instructor = Instructor.load_instructor_by_id('Storage/instructors.json', instructor_id)
                course = Course.load_course_by_id('Storage/courses.json', selected_course_id)
                if instructor and course:
                    instructor.assign_course(course)
                    QMessageBox.information(self, "Success", f"Instructor {instructor.name} assigned to course {course.course_name} successfully")
                    self.show_assign_instructor_form()  # Refresh form
                else:
                    QMessageBox.critical(self, "Error", "Instructor or Course not found")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "Please fill in all fields")

    # Create display table function for students, instructors, and courses
    def create_display_table(self, headers, data, category):
        """General function to create a display table for students, instructors, or courses."""
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
        students = Student.load_all_students('Storage/students.json')
        headers = ["Name", "Age", "Email", "Student ID", "Registered Courses"]
        data = [(s.name, s.age, s._email, s.student_id, ', '.join(s.registered_courses)) for s in students]
        self.create_display_table(headers, data, "student")

    def display_all_instructors(self):
        instructors = Instructor.load_all_instructors('Storage/instructors.json')
        headers = ["Name", "Age", "Email", "Instructor ID", "Courses Taught"]
        data = [(i.name, i.age, i._email, i.instructor_id, ', '.join(i.assigned_courses)) for i in instructors]
        self.create_display_table(headers, data, "instructor")

    def display_all_courses(self):
        courses = Course.load_all_courses_fully('Storage/courses.json')
        headers = ["Course ID", "Course Name", "Instructor", "Enrolled Students"]
        data = [(c.course_id, c.course_name, c.instructor.name if c.instructor else 'None', ', '.join(c.enrolled_students)) for c in courses]
        self.create_display_table(headers, data, "course")

    # Search functionality
    def create_search_form(self):
        """Creates the search form UI."""
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
        search_by = self.search_by_dropdown.currentText()
        search_in = self.search_in_dropdown.currentText()
        search_value = self.search_value_input.text()

        if not search_value:
            QMessageBox.warning(self, "Warning", "Please enter a search value.")
            return

        # Perform search based on category and search_by
        if search_in == "Student":
            students = Student.load_all_students('Storage/students.json')
            if search_by == "ID":
                results = [s for s in students if s.student_id == search_value]
            else:
                results = [s for s in students if s.name == search_value]

            if results:
                headers = ["Name", "Age", "Email", "Student ID", "Registered Courses"]
                data = [(s.name, s.age, s._email, s.student_id, ', '.join(s.registered_courses)) for s in results]
                self.create_display_table(headers, data, "student")
            else:
                QMessageBox.information(self, "No Results", "No student found.")

        elif search_in == "Instructor":
            instructors = Instructor.load_all_instructors('Storage/instructors.json')
            if search_by == "ID":
                results = [i for i in instructors if i.instructor_id == search_value]
            else:
                results = [i for i in instructors if i.name == search_value]

            if results:
                headers = ["Name", "Age", "Email", "Instructor ID", "Courses Taught"]
                data = [(i.name, i.age, i._email, i.instructor_id, ', '.join(i.assigned_courses)) for i in results]
                self.create_display_table(headers, data, "instructor")
            else:
                QMessageBox.information(self, "No Results", "No instructor found.")

        elif search_in == "Course":
            courses = Course.load_all_courses_fully('Storage/courses.json')
            if search_by == "ID":
                results = [c for c in courses if c.course_id == search_value]
            else:
                results = [c for c in courses if c.course_name == search_value]

            if results:
                headers = ["Course ID", "Course Name", "Instructor", "Enrolled Students"]
                data = [(c.course_id, c.course_name, c.instructor.name if c.instructor else 'None', ', '.join(c.enrolled_students)) for c in results]
                self.create_display_table(headers, data, "course")
            else:
                QMessageBox.information(self, "No Results", "No course found.")

    def save_edit(self, category):
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
        selected_items = self.display_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", f"No {category} selected for deletion.")
            return
        # Get the selected row
        selected_row = self.display_table.currentRow()
        if selected_row == -1:  # Check if a row is actually selected
            QMessageBox.warning(self, "Warning", f"No {category} selected for deletion.")
            return
        # Assuming ID is in 4th column for students and instructors, and 1st column for courses
        if category == "course":
            selected_id = selected_items[0].text()
        else:
            selected_id = selected_items[3].text()  # For students and instructors

        # Load the record by ID
        record = None
        if category == "student":
            record = Student.load_student_by_id('Storage/students.json', str(selected_id))
        elif category == "instructor":
            record = Instructor.load_instructor_by_id('Storage/instructors.json', str(selected_id))
        elif category == "course":
            record = Course.load_course_by_id('Storage/courses.json', str(selected_id))
        else:
            QMessageBox.critical(self, "Error", "Unknown category")
            return

        if record:
            confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete this {category}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    if category == "student":
                        record.delete_from_file('Storage/students.json')
                    elif category == "instructor":
                        record.delete_from_file('Storage/instructors.json')
                    elif category == "course":
                        record.delete_from_file('Storage/courses.json')

                    QMessageBox.information(self, "Success", f"{category.capitalize()} deleted successfully!")
                    if category == "student":
                        self.display_all_students()
                    elif category == "instructor":
                        self.display_all_instructors()
                    elif category == "course":
                        self.display_all_courses()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.critical(self, "Error", f"{category.capitalize()} not found")
    
    def refresh_courses(self):
        self.load_courses_into_dropdown(self.assign_course_dropdown)
        self.load_courses_into_dropdown(self.register_course_dropdown)

    def load_courses(self):
        # Load courses from JSON with error handling
        try:
            if os.path.exists('Storage/courses.json') and os.path.getsize('Storage/courses.json') > 0:
                with open('Storage/courses.json', 'r') as f:
                    return json.load(f)
            else:
                # Return an empty list if the file doesn't exist or is empty
                return []
        except json.JSONDecodeError:
            # Handle the case where the file is not properly formatted JSON
            print("Error: courses.json is not a valid JSON file.")
            return []

    def load_instructors(self):
        # Load instructors from JSON with error handling
        try:
            if os.path.exists('Storage/instructors.json') and os.path.getsize('Storage/instructors.json') > 0:
                with open('Storage/instructors.json', 'r') as f:
                    return json.load(f)
            else:
                # Return an empty list if the file doesn't exist or is empty
                return []
        except json.JSONDecodeError:
            # Handle the case where the file is not properly formatted JSON
            print("Error: instructors.json is not a valid JSON file.")
            return []

    def load_students(self):
        # Load students from JSON with error handling
        try:
            if os.path.exists('Storage/students.json') and os.path.getsize('Storage/students.json') > 0:
                with open('Storage/students.json', 'r') as f:
                    return json.load(f)
            else:
                # Return an empty list if the file doesn't exist or is empty
                return []
        except json.JSONDecodeError:
            # Handle the case where the file is not properly formatted JSON
            print("Error: students.json is not a valid JSON file.")
            return []

    def export_to_csv(self):
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
            self.export_data(filenames['courses'], self.load_courses(), 
                            ['Course Name', 'Course ID', 'Instructor Email', 'Instructor ID', 'Enrolled Students'], 
                            lambda course: {
                                'Course Name': course['course_name'],
                                'Course ID': course['course_id'],  # Courses don't have an age
                                'Instructor Email': course['instructor']['email'] if course['instructor'] else '',
                                'Instructor ID': course['instructor']['instructor_id'] if course['instructor'] else '',
                                'Enrolled Students': ', '.join(course['enrolled_students']) if course['enrolled_students'] else ''
                            })

            # Export instructors
            self.export_data(filenames['instructors'], self.load_instructors(),
                            ['Name', 'Age', 'Email', 'Instructor ID', 'Assigned Courses'],
                            lambda instructor: {
                                'Name': instructor['name'],
                                'Age': instructor['age'],
                                'Email': instructor['email'],
                                'Instructor ID': instructor['instructor_id'],
                                'Assigned Courses': ', '.join(instructor['assigned_courses']) if instructor['assigned_courses'] else ''
                            })

            # Export students
            self.export_data(filenames['students'], self.load_students(),
                            ['Name', 'Age', 'Email', 'Student ID', 'Registered Courses'],
                            lambda student: {
                                'Name': student['name'],
                                'Age': student['age'],
                                'Email': student['email'],
                                'Student ID': student['student_id'],
                                'Registered Courses': ', '.join(student['registered_courses']) if student['registered_courses'] else ''
                            })

            # Show success message
            self.show_message_box("Success", "Data successfully exported to CSV files.", QMessageBox.Information)

        except Exception as e:
            # Show error message if something goes wrong
            self.show_message_box("Error", f"Failed to export data: {str(e)}", QMessageBox.Critical)

    def export_data(self, filename, data, fieldnames, row_mapper):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(row_mapper(item))

    # Helper function to show message boxes
    def show_message_box(self, title, message, icon_type):
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon_type)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class EditDialog(QDialog):
    def __init__(self, category, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit {category.capitalize()}")
        self.category = category
        self.original_data = data
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        # Create and populate fields based on category
        self.fields = {}
        if self.category == "student":
            labels = ["Name", "Age", "Email"]
            indices = [0, 1, 2]
        elif self.category == "instructor":
            labels = ["Name", "Age", "Email"]
            indices = [0, 1, 2]
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
        line_edit = QLineEdit()
        line_edit.setText(text)
        self.fields[text] = line_edit
        return line_edit

    def save_changes(self):
        try:
            updated_data = [field.text() for field in self.fields.values()]
            if self.category == "student":
                # Load student and update
                student = Student.load_student_by_id('Storage/students.json', str(self.original_data[3]))
                if student:
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    student.name = name
                    age = int(updated_data[1])
                    assert (age >= 0), "Age cannot be negative"
                    student.age = age
                    email = updated_data[2]
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    assert(re.match(regex, email) is not None), "Wrong email format"
                    student._email = email
                    student.update('Storage/students.json')  # Update the student record in the file
                    
            elif self.category == "instructor":
                # Load instructor and update
                instructor = Instructor.load_instructor_by_id('Storage/instructors.json', str(self.original_data[3]))
                if instructor:
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    instructor.name = name
                    age = int(updated_data[1])
                    assert (age >= 0), "Age cannot be negative"
                    instructor.age = age
                    email = updated_data[2]
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    assert(re.match(regex, email) is not None), "Wrong email format"
                    instructor._email = email
                    instructor.update('Storage/instructors.json')

            elif self.category == "course":
                # Load course and update
                course = Course.load_course_by_id('Storage/courses.json', str(self.original_data[0]))
                if course:
                    name = updated_data[0]
                    assert (type(name) == str), "Name must be a string" 
                    assert(name.strip() != ""), "name cannot be empty"
                    assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
                    course.course_name = name
                    course.update('Storage/courses.json')

            QMessageBox.information(self, "Success", f"{self.category.capitalize()} updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


app = QApplication(sys.argv)
window = SchoolManagementApp()
window.show()
sys.exit(app.exec_())
