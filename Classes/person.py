import re

class Person:

    def __init__(self,name,age,email):
        assert (type(name) == str), "Name must be a string" 
        assert(name.strip() != ""), "name cannot be empty"
        assert re.match(r"^[a-zA-Z\s]+$", name), "Name must contain only alphabetic characters and spaces"
        assert (type(age) == int), "Age must be an integer" 
        assert (age >= 0), "Age cannot be negative"
        assert (type(email) == str), "Email must be a string"
        assert(email.strip() != ""), "Email cannot be empty"
        assert self.is_valid_email(email), "Invalid email format"

        self.name = name
        self.age = age
        self._email = email

    @staticmethod
    def is_valid_email(email):
      
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None
    
    def introduce(self):
        print("Person Name: "+self.name+"\nPerson Age: "+str(self.age))

    def __str__(self):
         return "Person Name: "+self.name+"\nPerson Age: "+str(self.age)
    

