from json import *
import shutil

# Login
jf_l = open("JSON_Base/account.json", "w+")
dict_l = {"*": "*", "admin":"e10adc3949ba59abbe56e057f20f883e", "Rigel":"e10adc3949ba59abbe56e057f20f883e"} # Md5 encoding  ：  123456
dump(dict_l, jf_l, indent=4)
print("ok")

account = 1
if account == 1:
    # -------------------admin-------------------
    # Course
    jf_c = open("JSON_Base/admin/course.json", "w+")
    # Class number : [Date, Topic, # should come, # came, attendance]
    dict_ECE_110 = {1:["2023-5-7", "Default Topic"]}
    dict_CS_240 = {}
    dict_Test = {}
    dict_c = {"ME_200":dict_ECE_110, "Test_Clicker":dict_Test}
    dump(dict_c, jf_c, indent=4)
    print("ok")

    # Student
    jf_s_1 = open("JSON_Base/admin/ME_200/student.json", "w+")
    jf_s_2 = open("JSON_Base/admin/Test_Clicker/student.json", "w+")
    # ID : Name
    dict_student = {"1111111":"Zhou Qishen", "2004629":"Qiu Yue", "2000277":"Li Bowen", "0000001":"Xie Mu"}
    dump(dict_student, jf_s_1, indent=4)
    dump(dict_student, jf_s_2, indent=4)
    print("ok")

    # Answer
    jf_a = open("JSON_Base/admin/ME_200/1.json", "w+")

    # question number : [Correct Answer, Answer #, Correct Answer #, Point, Answer time]
    dict_ques_c = {"1":['A', 4, 2, 3, 20], "2":['B', 4, 3, 3, 15], "3":['D', 4, 1, 5, 30]} 

    dict_Z_c = {"1":'D', "2":'C', "3":'A'} # Answers for questions in class 1

    dict_Q_c = {"1":'B', "2":'C', "3":'D'} 

    dict_L_c = {"1":'A', "2":'B', "3":'C'} 

    dict_X_c = {"1":'C', "2":'D', "3":'A'} 

    dict_student_c = {"Zhou Qishen":dict_Z_c, "Qiu Yue":dict_Q_c, "Li Bowen":dict_L_c, "Xie Mu":dict_X_c}
    dict_a = {"Question":dict_ques_c, "Student": dict_student_c}
    dump(dict_a, jf_a, indent=4)
    print("ok")
    # -------------------admin-------------------


else:
    # -------------------Rigel-------------------
    # Course
    jf_c = open("JSON_Base/Rigel/course.json", "w+")
    # Class number : [Date, Topic, # should come, # came, attendance]
    dict_ECE_110 = {1:["2023-5-7", "Default Topic"]}
    dict_CS_240 = {}
    dict_Test = {}
    dict_c = {"ECE_110":dict_ECE_110, "CS_240":dict_CS_240, "Test_Clicker_R":dict_Test}
    dump(dict_c, jf_c, indent=4)
    print("ok")

    # Student
    jf_s_1 = open("JSON_Base/Rigel/ECE_110/student.json", "w+")
    jf_s_2 = open("JSON_Base/Rigel/CS_240/student.json", "w+")
    jf_s_3 = open("JSON_Base/Rigel/Test_Clicker_R/student.json", "w+")
    # ID : Name
    dict_student = {"1111111":"Zhou Qishen", "2004629":"Qiu Yue", "2000277":"Li Bowen", "0000001":"Xie Mu"}
    dump(dict_student, jf_s_1, indent=4)
    dump(dict_student, jf_s_2, indent=4)
    dump(dict_student, jf_s_3, indent=4)
    print("ok")

    # Answer
    jf_a = open("JSON_Base/Rigel/ECE_110/1.json", "w+")

    # question number : [Correct Answer, Answer #, Correct Answer #, Point, Answer time]
    dict_ques_c = {"1":['A', 4, 2, 3, 20], "2":['B', 4, 3, 3, 15], "3":['D', 4, 1, 5, 30]} 

    dict_Z_c = {"1":'A', "2":'B', "3":'C'} # Answers for questions in class 1

    dict_Q_c = {"1":'C', "2":'D', "3":'D'} 

    dict_L_c = {"1":'A', "2":'B', "3":'A'} 

    dict_X_c = {"1":'A', "2":'B', "3":'A'} 

    dict_student_c = {"Zhou Qishen":dict_Z_c, "Qiu Yue":dict_Q_c, "Li Bowen":dict_L_c, "Xie Mu":dict_X_c}
    dict_a = {"Question":dict_ques_c, "Student": dict_student_c}
    dump(dict_a, jf_a, indent=4)
    print("ok")
    # -------------------Rigel-------------------



# Picture
# shutil.copy("D:/CS/Clicker/Repo/JSON_Base/BackUp/1-1.png", "D:/CS/Clicker/Repo/JSON_Base/admin/ECE_110/")
# shutil.copy("D:/CS/Clicker/Repo/JSON_Base/BackUp/1-2.png", "D:/CS/Clicker/Repo/JSON_Base/admin/ECE_110/")
# shutil.copy("D:/CS/Clicker/Repo/JSON_Base/BackUp/1-3.png", "D:/CS/Clicker/Repo/JSON_Base/admin/ECE_110/")
# print("ok")


