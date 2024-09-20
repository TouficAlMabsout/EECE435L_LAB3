from .person import Person

import json
import re

class Student(Person):
       
        def __init__(self,name,age,email,student_id,registered_courses):
                #from .course import Course
                super().__init__(name,age,email)
                assert (type(student_id) == str), "student_id must be a string"
                assert(student_id.strip() != ""), "student_id cannot be empty"
                assert re.match(r"^[a-zA-Z0-9]+$", student_id), "student_id must contain only alphanumeric characters"
                assert (type(registered_courses) == list), "registered_courses must be a list"
                # assert all(isinstance(course, Course) for course in registered_courses), "All elements in registered_courses must be of type Course"

               
                
                
                self.student_id = student_id
                self.registered_courses = registered_courses
               
       
        def register_course(self,course):  
                from .course import Course
                assert (type(course) == Course), "input must be of type Course"
                
                for student_id in course.enrolled_students:
                    if student_id == self.student_id:
                        raise ValueError("Already registered student")
                    
                self.registered_courses.append(course.course_id)
                course.add_student(self)
                course.update('Storage/courses.json')
                self.update('Storage/students.json')

        
        def to_dict(self):

            return {
                'name': self.name,
                'age': self.age,
                'email': self._email,
                'student_id': self.student_id,
                'registered_courses': [course for course in self.registered_courses]
            }

       
        def save_to_file(self, filename):
            if not self.is_unique_id(filename,self.student_id):
                    raise ValueError("student_id already exists!")
            
            if not self.is_unique_email(filename, self._email):
                    raise ValueError("email already exists!")
            
            try:
                with open(filename, 'r') as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
            except FileNotFoundError:
                data = []
            
            data.append(self.to_dict())
            
            with open(filename, 'w') as f:
                json.dump(data, f,indent=4)

    

        @classmethod
        def is_unique_id(cls,filename, student_id):
            
            existing_ids = cls.load_existing_ids(filename)
            return student_id not in existing_ids

        @classmethod
        def load_existing_ids(cls, filename):
            try:
                with open(filename, 'r') as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
            except FileNotFoundError:
                data = []
            
            return {student['student_id'] for student in data}
        
        @classmethod
        def load_student_by_id(cls, filename, student_id):
            with open(filename, 'r') as f:
                data = json.load(f)
            for student_data in data:
                if student_data['student_id'] == student_id:
                    return Student(student_data['name'],student_data['age'],student_data['email'],student_data['student_id'],student_data['registered_courses'])
            return None
        
        @classmethod
        def is_unique_email(cls, filename, email):
            from .instructor import Instructor
            existing_emails = cls.load_existing_emails(filename)
            existing_inst_emails = Instructor.load_existing_emails('Storage/instructors.json')
            return (email not in existing_emails and email not in existing_inst_emails)

        @classmethod
        def load_existing_emails(cls, filename):
            try:
                with open(filename, 'r') as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
            except FileNotFoundError:
                data = []
            
            return {student['email'] for student in data}
        

        def update(self, filename):
            if not self.is_unique_id(filename, self.student_id):
                # Load existing data
                try:
                    with open(filename, 'r') as f:
                        try:
                            data = json.load(f)
                            if not isinstance(data, list):
                                data = []
                        except json.JSONDecodeError:
                            data = []
                except FileNotFoundError:
                    data = []

                # Check if student with the given ID exists
                for i, student_data in enumerate(data):
                    if student_data['student_id'] == self.student_id:
                        # Update existing record
                        data[i] = self.to_dict()
                        break
                else:
                    raise ValueError("Student ID not found!")

                # Save updated data
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
        
        @classmethod
        def load_all_students(cls, filename):
            students = []
            
            with open(filename, 'r') as f:
                try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                except json.JSONDecodeError:
                        data = []
            
            for student_data in data:
                std1 = Student(student_data['name'],student_data['age'],student_data['email'],student_data['student_id'],student_data['registered_courses'])
                
                students.append(std1)
            
            return  students
        
        def delete_from_file(self,filename):
            # Delete student record from file
            students = Student.load_all_students(filename)
            students = [s for s in students if s.student_id != self.student_id]
            with open(filename, 'w') as file:
                json.dump([s.to_dict() for s in students], file,indent=4)





          
        
    
           
                    