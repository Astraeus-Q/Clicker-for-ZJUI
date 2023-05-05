from json import *


# Login
jf_l = open("JSON_Base/account.json", "w+")
dict_l = {"admin":"e10adc3949ba59abbe56e057f20f883e", "Rigel":"e10adc3949ba59abbe56e057f20f883e"} # Md5 encoding  ：  123456
dump(dict_l, jf_l, indent=4)
print("ok")

# Course
jf_c = open("JSON_Base/admin/course.json", "w+")
dict_c = {"ECE 110":"ECE_110.json", "CS 240":"CS_240.json", "Test Clicker":"Test_Clicker.json"}
dump(dict_c, jf_c, indent=4)
print("ok")

# Answer
jf_a = open("JSON_Base/admin/ECE_110.json", "w+")

dict_std_c1 = {"1":['A', 4, 2, 3, 20], "2":['B', 4, 3, 3, 15], "3":['D', 4, 1, 5, 30]} # question number : [Correct Answer, Answer #, Correct Answer #, Point, Answer time]
dict_std = {"1":dict_std_c1}

dict_Z_c1 = {"q1":'A', "q2":'B' , "q3":"C"} # Answers for questions in class 1
dict_Z = {"class1":dict_Z_c1} # Classes

dict_Q_c1 = {"q1":'A', "q2":'D', "q3":"D"} 
dict_Q = {"class1":dict_Q_c1}

dict_L_c1 = {"q1":'D', "q2":'B', "q3":"A"} 
dict_L = {"class1":dict_L_c1}

dict_X_c1 = {"q1":'D', "q2":'B', "q3":"A"} 
dict_X = {"class1":dict_X_c1}

dict_a = {"Standard":dict_std, "Zhou Qishen":dict_Z, "Qiu Yue":dict_Q, "Li Bowen":dict_L, "Xie Mu":dict_X}
dump(dict_a, jf_a, indent=4)
print("ok")

