#OOPs in Python

# ==============================
# 1. Lists vs classes
# ==============================


#Data of student in the format Name,Grade
student_1=['Madhav',10]
student_2=['Visha',12]

print(student_1[0],'is in class',student_1[1])
#Another way of printing statements
print(f'{student_2[0]} is in class {student_2[1]}')


# ==============================
# 2. Creating a class (hardcoded values)
# ==============================

#Using OOPs
#class-a blueprint/template, basically it is used by the user to create their own data type such as built in data type like integer, think of struct in C
#object-a particular example of a class

#1. Creating a student record
#defining a class
class Student:
  name='Madhav'
  grade=10
#↑ hardcoded

#defining an object
student1=Student()

#Accessing an element in the class
print(student1.name,student1.grade)


# ==============================
# 3. Class with __init__
# ==============================

#How to create a class with user defined variables?
#We do this by defining functions in the class, called methods

class Student:
  def __init__(self,name,grade): #init initialises the values, it always must be done with the parameter self, as self refers to the current object
    self.name=name
    self.grade=grade
    # ^attributes
std1=Student('Madhav',10)
print(std1.name,std1.grade)
std2=Student('Viva',1)
print(std2.name,std2.grade)
N=input("Enter a name: ")
A=int(input("Enter the grade: "))
std3=Student(N,A)
print(std3.name,std3.grade)



class Student:
  def __init__(self,name,grade,per):
    self.name=name
    self.grade=grade
    self.per=per
  def student_details(self):
    print(self.name,'is in grade',self.grade,'with percentage as',self.per)
  def increase_grade(self):
    self.grade+=1

#modifying inside
std1=Student('Madhav',10,90)
std1.student_details()
std1.increase_grade()
std1.student_details()

#printing it in the form of dictionary
print(std1.__dict__)

#modifying outside
std1.per=100
std1.student_details()

#delete an object property
print(std1.__dict__)
del std1.per
print(std1.__dict__)

#delete an object
#del std1
print(std1)




class Student:
  def __init__(self,name,grade,per,team):
    self.name=name
    self.grade=grade
    self.per=per
    self.team=team
  def student_details(self):
    print(self.name,'is in grade',self.grade,'with percentage as',self.per,'and is in team',self.team)
  def increase_grade(self):
    self.grade+=1


team1='A'
team2='B'
std1=Student('Madhav',10,90,team1)
std2=Student('Miya',11,94,team2)
std1.student_details()
std2.student_details()
