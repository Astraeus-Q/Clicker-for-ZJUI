from json import *


# Login
jf_l = open("JSON_Base/account.json", "w+")
dict_l = {"admin":"e10adc3949ba59abbe56e057f20f883e", "Rigel":"e10adc3949ba59abbe56e057f20f883e"} # Md5 encoding  ：  123456
dump(dict_l, jf_l, indent=4)
print("ok")

# Course
jf_c = open("JSON_Base/admin/course.json", "w+")
# Class number : [Date, Topic, # should come, # came, attendance]
dict_ECE_110 = {1:["2023-5-7", "Default Topic", 4, 4, 1]}
dict_CS_240 = {}
dict_Test = {}
dict_c = {"ECE 110":dict_ECE_110, "CS 240":dict_CS_240, "Test Clicker":dict_Test}
dump(dict_c, jf_c, indent=4)
print("ok")

# Student
jf_s = open("JSON_Base/admin/ECE_110/student.json", "w+")
# ID : Name
dict_student = {111:"Zhou Qishen", 112:"Qiu Yue", 113:"Li Bowen", 114:"Xie Mu"}


# Answer
jf_a = open("JSON_Base/admin/ECE_110/1.json", "w+")

# question number : [Correct Answer, Answer #, Correct Answer #, Point, Answer time]
dict_ques_c = {"1":['A', 4, 2, 3, 20], "2":['B', 4, 3, 3, 15], "3":['D', 4, 1, 5, 30]} 

dict_Z_c = {"1":'A', "2":'B' , "3":"C"} # Answers for questions in class 1

dict_Q_c = {"1":'A', "2":'D', "3":"D"} 

dict_L_c = {"1":'D', "2":'B', "3":"A"} 

dict_X_c = {"1":'D', "2":'B', "3":"A"} 

dict_student_c = {"Zhou Qishen":dict_Z_c, "Qiu Yue":dict_Q_c, "Li Bowen":dict_L_c, "Xie Mu":dict_X_c}
dict_a = {"Question":dict_ques_c, "Student": dict_student_c}
dump(dict_a, jf_a, indent=4)
print("ok")
