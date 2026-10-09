#Features in OOPS

#1. Abstraction- Hiding unneccessary details from the user using methods or classes
class Student:
  def __init__(self,name,grade,per,team):
    self.name=name
    self.grade=grade
    self.per=per
    self.team=team
  def student_details(self):
    print(self.name,'is in grade',self.grade,'with percentage as',self.per+2,'and is in team',self.team)
std1=Student('Madhav',10,90,'A')
std2=Student('Miya',11,94,'B')
std1.student_details()

#2. Encapsulation- protecting the data by binding the attributes and the methods and restricting access accordingly
class Student:
  def __init__(self,name,grade,per,team):
    self.name=name
    self.grade=grade
    self.__per=per   #private(only i can use)
    self.team=team
  def student_details(self):
    print(self.name,'is in grade',self.grade,'with percentage as',self.per,'and is in team',self.team)
  def get_per(self):
    return self.__per

std1=Student('Madhav',10,90,'A')
std2=Student('Miya',11,94,'B')

#print(std1.__per)
#print(std1.per)
#^Both will raise error

print(std1.get_per())

#3. Inheritance- getting properties of another class (parent-child type)
class Student:  #parent   (is-of type)
  def __init__(self,name,grade,per,team):
    self.name=name
    self.grade=grade
    self.per=per
    self.team=team
  def student_details(self):
    print(self.name,'is in grade',self.grade,'with percentage as',self.per,'and is in team',self.team)

class Graduate(Student):  #child
  def __init__(self,name,grade,per,team,stream):
    super().__init__(name,grade,per,team)    #wanting details from parent class
    self.stream=stream
  def student_details(self):
    super().student_details()  #inherting method from parent class
    print("Stream: ",self.stream)

Gstd1=Graduate("Madhav",10,90,'A','PCM')
print(Gstd1.stream)
Gstd1.student_details()

#4. Polymorphisim- same function name in 2 different classes is allowed
class Student:  #parent   (is-of type)
  def __init__(self,name,grade,per,team):
    self.name=name
    self.grade=grade
    self.per=per
    self.team=team
  def student_details(self):
    print(self.name,'is in grade',self.grade,'with percentage as',self.per,'and is in team',self.team)

class Graduate(Student):  #child
  def __init__(self,name,grade,per,team,stream):
    super().__init__(name,grade,per,team)    #wanting details from parent class
    self.stream=stream
  def student_details(self):#function w same name
    print(self.name,'is in grade',self.grade,'with percentage as',self.per,'and is in team',self.team,'\nThey are in the stream: ',self.stream)
#object of Student
std1=Student('Madhav',10,90,'A')

#object of Graduate
Gstd1=Graduate('Keshav',11,99,'B','PCM')

std1.student_details()
Gstd1.student_details() #calls function of graduate not of student
