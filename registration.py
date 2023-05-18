import json

f_reg = open("stu_register.csv", "r")
f_js = open("JSON_Base/Rigel/ECE_110/student.json", "w+")
dict_map = {}
for line in f_reg.readlines():
    line = line.strip('\n')
    id = line[:7]
    name = line[8:]
    dict_map[id] = name
json.dump(dict_map, f_js, indent=4)
