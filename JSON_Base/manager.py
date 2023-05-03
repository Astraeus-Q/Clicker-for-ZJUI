from json import *

jf = open("JSON_Base/account.json", "w+")
dict = {"admin":"e10adc3949ba59abbe56e057f20f883e", "Rigel":"e10adc3949ba59abbe56e057f20f883e"} # Md5 encoding  ：  123456
dump(dict, jf, indent=4)
print("ok")