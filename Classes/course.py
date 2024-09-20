import json
import re

class Course:

    def __init__(self,course_id,course_name,instructor,enrolled_students):
        #from .student import Student
        #from .instructor import Instructor
        assert(type(course_id) == str), "course_id must a string"
        assert(course_id.strip() != ""), "course_id cannot be empty"
        assert re.match(r"^[a-zA-Z0-9]+$", course_id), "course_id must contain only alphanumeric characters"
        assert(type(course_name) == str), "course name must be a string"
        assert(course_name.strip()!=""), "course name cannot be empty"
        # assert(type(instructor) == Instructor), "instructor must be of type Instructor"
        assert(type(enrolled_students) == list), "enrolled_students must be a list"
        # assert all(isinstance(student, Student) for student in enrolled_students), "All elements in assigned_courses must be of type Student"

       
       
        
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students
    
    def add_student(self,student):
        from .student import Student
        assert(type(student) == Student), "input must be of type Student"

        self.enrolled_students.append(student.student_id)
    
    def to_dict(self):
     
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.to_dict() if self.instructor != None else None,
            'enrolled_students': [student for student in self.enrolled_students]
        }

    
    def save_to_file(self, filename):
        if not self.is_unique_id(filename,self.course_id):
                    raise ValueError("course_id already exists!")
        
        if not self.is_unique_name(filename, self.course_name):
                    raise ValueError("course_name already exists!")
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
    def is_unique_id(cls,filename, course_id):
        
        existing_ids = cls.load_existing_ids(filename)
        return course_id not in existing_ids

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
        
        return {course['course_id'] for course in data}
    
    @classmethod
    def load_course_by_id(cls, filename, course_id):
        with open(filename, 'r') as f:
            data = json.load(f)
        for course_data in data:
            if course_data['course_id'] == course_id:
                from .instructor import Instructor
                instructor_data = course_data['instructor']
                if instructor_data:
                    instructor = Instructor(
                        name=instructor_data['name'],
                        age=instructor_data['age'],
                        email=instructor_data['email'],
                        instructor_id=instructor_data['instructor_id'],
                        assigned_courses=instructor_data['assigned_courses']  
                    )
                else:
                    instructor = None  # Handle case when there's no instructor

                # Create the Course object
                return cls(
                    course_id=course_data['course_id'],
                    course_name=course_data['course_name'],
                    instructor=instructor,
                    enrolled_students=course_data.get('enrolled_students', [])
                )
        return None
    
    @classmethod
    def load_all_courses(cls, filename):
        course_ids = []
        
        with open(filename, 'r') as f:
            try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            except json.JSONDecodeError:
                    data = []
        
        for course_data in data:
            course_id = course_data.get('course_id')
            course_ids.append(course_id)
        
        return  course_ids
    
    @classmethod
    def load_existing_names(cls, filename):
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
        
        return {course['course_name'] for course in data}
    
    @classmethod
    def is_unique_name(cls, filename, course_name):
        existing_names = cls.load_existing_names(filename)
        return course_name not in existing_names
    
    def update(self, filename):
            if not self.is_unique_id(filename, self.course_id):
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
                for i, course_data in enumerate(data):
                    if course_data['course_id'] == self.course_id:
                        # Update existing record
                        
                        data[i] = self.to_dict()
                        break
                else:
                    raise ValueError("Course ID not found!")

                # Save updated data
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
    
    @classmethod
    def load_all_courses_fully(cls, filename):
        courses = []
        
        with open(filename, 'r') as f:
            try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
            except json.JSONDecodeError:
                    data = []
        
        for course_data in data:
            from .instructor import Instructor
            instructor_data = course_data['instructor']
            if instructor_data:
                instructor = Instructor(
                    name=instructor_data['name'],
                    age=instructor_data['age'],
                    email=instructor_data['email'],
                    instructor_id=instructor_data['instructor_id'],
                    assigned_courses=instructor_data['assigned_courses']  
                )
            else:
                instructor = None  # Handle case when there's no instructor

            # Create the Course object
            inst1 = Course(
                course_id=course_data['course_id'],
                course_name=course_data['course_name'],
                instructor=instructor,
                enrolled_students=course_data.get('enrolled_students', [])
            )
            courses.append(inst1)
        
        return  courses
    
    def delete_from_file(self,filename):
            # Delete student record from file
            courses = Course.load_all_courses_fully(filename)
            courses = [c for c in courses if c.course_id != self.course_id]
            with open(filename, 'w') as file:
                json.dump([c.to_dict() for c in courses], file,indent=4)




   