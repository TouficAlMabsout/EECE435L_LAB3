from .person import Person

import json
import re

class Instructor(Person):

    def __init__(self,name,age,email,instructor_id,assigned_courses):
        from .course import Course
        super().__init__(name,age,email)
        assert (type(instructor_id) == str), "instructor_id must be a string"
        assert(instructor_id.strip() != ""), "instructor_id cannot be empty"
        assert re.match(r"^[a-zA-Z0-9]+$", instructor_id), "instructor_id must contain only alphanumeric characters"
        assert (type(assigned_courses) == list), "assigned_courses must be a list"
        # assert all(isinstance(course, Course) for course in assigned_courses), "All elements in assigned_courses must be of type Course"

        
        
        
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses
     

    def assign_course(self,course): 
        from .course import Course
        assert (type(course) == Course), "input must be of type Course"

        if course.instructor == None:
            course.instructor = self
            self.assigned_courses.append(course.course_id)
            course.update('Storage/courses.json')
            self.update('Storage/instructors.json')
        elif course.instructor.instructor_id == self.instructor_id:
            raise ValueError('you are already assigned for for the course')
        else:
            raise ValueError('The course already has an instructor assigned')
    
    def to_dict(self):
        
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course for course in self.assigned_courses]
        }

   

    def save_to_file(self, filename):
        if not self.is_unique_id(filename,self.instructor_id):
                    raise ValueError("instructor_id already exists!")
        
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
            json.dump(data, f, indent=4)  


  
    
    @classmethod
    def is_unique_id(cls, filename, instructor_id):
        
        existing_ids = cls.load_existing_ids(filename)
        return instructor_id not in existing_ids

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
        
        return {instructor['instructor_id'] for instructor in data}
    
    @classmethod
    def load_instructor_by_id(cls, filename, instructor_id):
        with open(filename, 'r') as f:
            try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            except json.JSONDecodeError:
                    data = []
        for instructor_data in data:
            if instructor_data['instructor_id'] == instructor_id:
                return Instructor(instructor_data['name'],instructor_data['age'],instructor_data['email'],instructor_data['instructor_id'],instructor_data.get('assigned_courses',[]))
        return None
    
    @classmethod
    def is_unique_email(cls, filename, email):
        from .student import Student
        existing_emails = cls.load_existing_emails(filename)
        existing_std_emails = Student.load_existing_emails('Storage/students.json')
        return (email not in existing_emails and email not in existing_std_emails)

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
        
        return {instructor['email'] for instructor in data}
    
    def update(self, filename):
            if not self.is_unique_id(filename, self.instructor_id):
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
                for i, instructor_data in enumerate(data):
                    if instructor_data['instructor_id'] == self.instructor_id:
                        # Update existing record
                        data[i] = self.to_dict()
                        break
                else:
                    raise ValueError("Instructor ID not found!")

                # Save updated data
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
    
    @classmethod
    def load_all_instructors(cls, filename):
        instructors = []
        
        with open(filename, 'r') as f:
            try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            except json.JSONDecodeError:
                    data = []
        
        for instructor_data in data:
            inst1 = Instructor(instructor_data['name'],instructor_data['age'],instructor_data['email'],instructor_data['instructor_id'],instructor_data.get('assigned_courses',[]))
            
            instructors.append(inst1)
        
        return  instructors
    
    def delete_from_file(self,filename):
            # Delete student record from file
            instructors = Instructor.load_all_instructors(filename)
            instructors = [i for i in instructors if i.instructor_id != self.instructor_id]
            with open(filename, 'w') as file:
                json.dump([i.to_dict() for i in instructors], file,indent=4)





