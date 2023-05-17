# connect the test backend to the database.
# add the database to the local files.
import sqlite3
import os
# Init local DB.
# Create and init the local SQLite 3 database. only for temp use.
# create student info, class into. this would store both online and offline.
# Will transmit to online db when network connection established.
# temp storage: each class would create an table to store stat for each question, temp table
# for student answers. After upload, both would be drop.
import sqlite3 as sql

import Clicker_DB_manager as dbm
class remote_db():
    def __init__(self):
        self.db = sql.connect("remote.db")
        self.cursor = self.db.cursor()
        # store some local variables.
        self.local_user = "admin"
        self.local_class = 0
        self.local_course = ""
        self.local_cou = "./JSON_Base/" + self.local_user+ "/course.json"
        self.local_stu = "./JSON_Base/" + self.local_user+ "/" + self.local_course + "/student.json"

    def change_user(self,user_name:str):
        self.local_user = user_name
        self.local_cou = "./JSON_Base/" + self.local_user + "/course.json"
        self.local_stu = "./JSON_Base/" + self.local_user + "/" + self.local_course + "/student.json"

    def change_course(self,course_code:str, class_num:int = 0):
        self.local_class = class_num
        self.local_course = course_code
        self.local_stu = "./JSON_Base/" + self.local_user + "/" + self.local_course + "/student.json"

    def remote_db_init(self):
        # self.cursor.execute("DROP TABLE IF EXISTS questions")
        # careful not to call the function after data storage.
        # self.cursor.execute("DROP TABLE IF exists students,courses,register,teachers,teach,grades,weekly")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS students("
                       "hard_id CHAR(7) NOT NULL, "
                       "net_id INT(10) , "
                       "name CHAR(10),"
                       "PRIMARY KEY (hard_id))")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS courses("
                       "course CHAR(10) NOT NULL, "
                       "name CHAR(20),"
                       "semester CHAR(10),"
                       "attend_rate REAL, "
                       "PRIMARY KEY (course))")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS register("
                       "course CHAR(7) NOT NULL, "
                       "hard_id CHAR(10) NOT NULL,"
                       "class INT(10),"
                       "PRIMARY KEY (course,hard_id),"
                       "FOREIGN KEY (course)"
                       "    REFERENCES courses(course)"
                       "    ON UPDATE CASCADE "
                       "    ON DELETE CASCADE,"
                       "FOREIGN KEY (hard_id)"
                       "    REFERENCES students(hard_id)"
                       "    ON UPDATE CASCADE "
                       "    ON DELETE CASCADE)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS teachers("
                       "user CHAR(10) NOT NULL,"
                       "password CHAR(20) NOT NULL,"
                       "name CHAR(10),"
                       "pass_md5 CHAR(40),"
                       "PRIMARY KEY (user))")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS teach("
                       "user CHAR(10) NOT NULL,"
                       "course CHAR(10) NOT NULL ,"
                       "PRIMARY KEY (user,course),"
                       "FOREIGN KEY (user)"
                       "    REFERENCES teachers(user)"
                       "    ON UPDATE CASCADE "
                       "    ON DELETE CASCADE,"
                       "FOREIGN KEY (course)"
                       "    REFERENCES courses(course)"
                       "    ON UPDATE CASCADE "
                       "    ON DELETE CASCADE)")

        # appendable table here, we can add list for each week.
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS grades("
        #                "hard_id CHAR(10) NOT NULL,"
        #                "course CHAR(10) NOT NULL,"
        #                "PRIMARY KEY (hard_id,course),"
        #                "FOREIGN KEY (hard_id)"
        #                "    REFERENCES students(hard_id)"
        #                "    ON UPDATE CASCADE "
        #                "    ON DELETE CASCADE,"
        #                "FOREIGN KEY (course)"
        #                "    REFERENCES courses(course)"
        #                "    ON UPDATE CASCADE "
        #                "    ON DELETE CASCADE)")

        # dense storage, clear per semester.
        self.cursor.execute("CREATE TABLE IF NOT EXISTS weekly("
                            "course CHAR(10) NOT NULL,"
                            "class INT(10) NOT NULL,"
                            "week INT(10) NOT NULL,"
                            "title CHAR(20),"
                            "total INT(10),"
                            "attend INT(10),"
                            "scores INT(10),"
                            "c_date DATE,"
                            "PRIMARY KEY (course,class,week),"
                            "FOREIGN KEY (course)"
                            "   REFERENCES courses(course)"
                            "   ON UPDATE CASCADE "
                            "   ON DELETE CASCADE )")
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS questions("
                            "course CHAR(10) NOT NULL,"
                            "class INT(10) NOT NULL,"
                            "week INT(10) NOT NULL,"
                            "question INT(10),"
                            "ans INT(10),"
                            "total INT(10),"
                            "counts INT(10),"
                            "score  INT(10),"
                            "PRIMARY KEY (course,class,week,question),"
                            "FOREIGN KEY (course)"
                            "   REFERENCES courses(course)"
                            "   ON UPDATE CASCADE"
                            "   ON DELETE CASCADE)")

        
        # setting TRIGGER in the future updates.

        # ADD admin user info.
        # self.cursor.execute("INSERT INTO teachers "
        #                "VALUES (?,?,?,?)",("admin","admin","admin","admin"))

        self.db.commit()

    # we will not care about the foreign student register, we would only focus on
    # collecting data from clickers.
    # Thus we only provide student information update API.
    def update_students(self,hardware_id:int, name:str, net_id:str):
        try :
            self.cursor.execute("INSERT INTO students "
                           "VALUES (?,?,?)",(hardware_id, net_id, name))
        except:
            self.cursor.execute("UPDATE students "
                                "SET net_id = ?, name = ?"
                                "WHERE hard_id = ? ", (net_id, name, hardware_id))

        self.db.commit()
    def register_teacher(self,user_name:str, pwd:str, name:str, pwd_md5:str):
        # register user into the database.
        try :
            self.cursor.execute("INSERT INTO teachers "
                                "VALUES (?,?,?,?)",(user_name,pwd,name,pwd_md5))
        except:
            self.cursor.execute("UPDATE teachers "
                                "SET password = :pwd, name = :name, pass_md5 = :pwd_md "
                                "WHERE user = :user", ({"pwd":pwd,"name":name,"pwd_md":pwd_md5,"user":user_name}))
        self.db.commit()
    def sync_local_account(self):
        account_list = dbm.read_DB("./JSON_Base/account.json")
        for row in self.cursor.execute("SELECT user, pass_md5 FROM teachers ORDER BY user"):
            account_list[row[0]] = row[1]
        # write to local cache.
        dbm.write_DB("./JSON_Base/account.json",account_list)

    def change_pass(self,user_name:str,pwd:str, pwd_md5:str):
        self.cursor.execute("UPDATE teachers "
                            "SET password = ?, pass_md5 = ?"
                            "WHERE user = ?",(pwd, pwd_md5, user_name))
        self.db.commit()
    def update_teach(self,user_name:str, courses:tuple,add = True):
        # allow multiple teacher teach same course.
        if add:
            try:
                for c in courses:
                    self.cursor.execute("INSERT INTO teach "
                                        "VALUES (?,?)",(user_name,c))
                self.db.commit()
            except sqlite3.IntegrityError:
                print(" course already added. ")
        else:
            for c in courses:
                try:
                    self.cursor.execute("DELETE FROM teach "
                                        "WHERE teacher = ?, course = ?",(user_name,c))
                    self.db.commit()
                except sqlite3.IntegrityError:
                    print(" course already deleted. ")

    def register_course(self,hard_id:str, courses:tuple,class_num:tuple ,add = True):
        if add:
            try:
                for i in range(len(courses)):
                    self.cursor.execute("INSERT INTO register (course,hard_id,class)"
                                        "VALUES (?,?,?)",(courses[i],hard_id,class_num[i]))
                self.db.commit()
            except sqlite3.IntegrityError:
                print(" some course has registered! ")
        else:
            try:
                for i in range(len(courses)):
                    self.cursor.execute("DELETE FROM register (course,hard_id,class)"
                                        "WHERE hard_id = ?, course = ?",(hard_id,courses[i]))
                self.db.commit()
            except sqlite3.IntegrityError:
                print(" Some course not exits! ")

    def update_courses(self, course_number:str, course_name:str, semester:str):
        try :
            self.cursor.execute("INSERT INTO courses "
                                "VALUES (?,?,?,?)", (course_number, course_name, semester,0))
        except:
            self.cursor.execute("UPDATE courses "
                                "SET name = ?, semester = ?"
                                "WHERE course = ?", (course_name, semester, course_number))

        self.db.commit()
    def local_update_course(self):
        if not os.path.exists(self.local_cou):
            course_list = {}
            for row in self.cursor.execute("SELECT course FROM teach "
                                           "WHERE user = ?",(self.local_user,)):
                course_list[row[0]] = {}

            self.cursor.execute("SELECT week FROM weekly "
                                    "WHERE course = ? "
                                    "ORDER BY week DESC "
                                    "LIMIT 1",(self.local_course,))
            result = self.cursor.fetchall()
            if len(result) == 0:
                pass
            else:
            
                hist = result[0][0]
                # find if any local cache

                for i in range(hist):
                    # update course information from database.
                    if str(i+1) not in course_list[self.local_course].keys():
                        try:
                            self.cursor.execute("SELECT c_date, title FROM weekly "
                                            "WHERE course = :c AND week = :w ", ({"c":self.local_course,"w":int(i+1)}))
                            result = self.cursor.fetchall()
                            list_to_w = list(result[0])
                            course_list[self.local_course][str(i+1)] = list_to_w
                            dbm.write_DB(self.local_cou,course_list)
                        except sqlite3.IntegrityError:
                            pass
            if os.path.exists("./JSON_Base/"+self.local_user+"/"):
                pass
            else:
                os.mkdir("./JSON_Base/"+self.local_user+"/")

            dbm.write_DB(self.local_cou,course_list)

    def local_student_update(self):
        if not os.path.exists(self.local_stu):
            student_list = {}
            # read the local hardware id, pull the name and net_id into the local.
            for row in self.cursor.execute("SELECT R.hard_id, S.name from register R LEFT OUTER JOIN students S ON R.hard_id = S.hard_id "
                                           "WHERE course = ? ORDER BY R.hard_id", (self.local_course,)):
                student_list[row[0]] = row[1]

            # create folder if not exist.
            if os.path.exists("./JSON_Base/"+self.local_user+"/"+self.local_course+"/"):
                pass
            else:
                os.mkdir("./JSON_Base/"+self.local_user+"/"+self.local_course+"/")
            dbm.write_DB(self.local_stu,student_list)

    def result_update(self, course_count:int):

        record = "./JSON_Base/" + self.local_user + "/" + self.local_course + "/" + \
                 str(course_count) + ".json"

        try :
            dump_dict = dbm.read_DB(record)

        except:
            print("? QYNZGSM ?")
            return

        course_dict = dbm.read_DB(self.local_cou)
        student_dict = dbm.read_DB(self.local_stu)

        ans = dump_dict["Student"]
        qs= dump_dict["Question"]

        c_i = course_dict[self.local_course][str(course_count)]
        # first update the course record.
        total_score = 0
        try:
            for key,values in qs.items():
                total_score += int(values[3])
                self.cursor.execute("INSERT INTO questions "
                                    "VALUES (?,?,?,?,?,?,?,?)",
                                    (self.local_course,self.local_class,course_count,key,values[0],int(values[1]),int(values[2]),int(values[3])))

            self.cursor.execute("INSERT INTO weekly "
                                "VALUES (?,?,?,?,?,?,?,?)",
                                (self.local_course,self.local_class,course_count,c_i[1],0,0,total_score,c_i[0]))
            # then update the students.
            self.db.commit()
        except sqlite3.IntegrityError:
            print(" Record Alrerady added! ")

        # TODO: find out how to detect new students with QY.
        # finally update the grades.
        # detect if the column exist.
        week_name = "week_" + str(course_count)
        ans_name = "ans_" + str(course_count)

        for key,values in ans.items():
            # key: student name, value, dict of answers.
            total_score = 0
            answer_char = ""
            hid = ""
            for k,v in student_dict.items():
                if v == key :
                    hid = k

            for num,ans in values.items():
                answer_char += ans
                answer_char += ","
                if (qs[num][0] == ans):
                    total_score += int(qs[num][3])

            # record the data into the grades.
            try :
                self.cursor.execute("UPDATE register "
                                    "SET " + week_name + " = :set "
                                    "WHERE hard_id = :hid AND course = :c ",
                                    ({"set":total_score,"hid":hid,"c":self.local_course}))
                self.cursor.execute("UPDATE register "
                                    "SET " + ans_name +" = ? "
                                    "WHERE hard_id = ? AND course = ? ",
                                    (answer_char, hid, self.local_course))
            except:
                sql_exec = ["ALTER TABLE register ADD " + week_name + " REAL DEFAULT 0",
                            "ALTER TABLE register ADD " + ans_name + " CHAR(10) DEFAULT " + "_"]
                self.cursor.execute(sql_exec[0])
                self.cursor.execute(sql_exec[1])
                self.cursor.execute("UPDATE register "
                                    "SET " + week_name + " = :set "
                                    "WHERE hard_id = :hid AND course = :c ",
                                    ({"set":total_score,"hid":hid,"c":self.local_course}))
                self.cursor.execute("UPDATE register "
                                    "SET " + ans_name + " = ? "
                                    "WHERE hard_id = ? AND course = ? ",
                                    (answer_char, hid, self.local_course))
        self.db.commit()

    def history_update(self):
        # would pull nearly all the history information.
        # first pull the max week info.
        self.cursor.execute("SELECT week FROM weekly "
                                   "WHERE course = ? "
                                   "ORDER BY week DESC "
                                   "LIMIT 1",(self.local_course,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            return
        
        hist = result[0][0]
        # find if any local cache
        course_dict = dbm.read_DB(self.local_cou)

        for i in range(hist):
            # update course information from database.
            if str(i+1) not in course_dict[self.local_course].keys():
                try:
                    self.cursor.execute("SELECT c_date, title FROM weekly "
                                        "WHERE course = :c AND week = :w ", ({"c":self.local_course,"w":int(i+1)}))
                    result = self.cursor.fetchall()
                    list_to_w = list(result[0])
                    course_dict[self.local_course][str(i+1)] = list_to_w
                    dbm.write_DB(self.local_cou,course_dict)
                except sqlite3.IntegrityError:
                    pass
                    # record deleted by admin.
            # update course answers from database.
            target = "./JSON_Base/"+self.local_user+"/"+self.local_course+"/"+str(i+1)+".json"
            if os.path.exists(target):
                pass 
            else: 
                qs = {}
                ans = {}
                try:
                    self.cursor.execute("SELECT question, ans, total, counts, score "
                                        "FROM questions "
                                        "WHERE course = ? AND week = ?"
                                        "ORDER BY question", (self.local_course,str(i+1)))
                    result = self.cursor.fetchall()
                    for q_num in range(len(result)):
                        q_list = list(result[q_num])
                        q_list.pop(0)
                        q_list.append(0)
                        qs[str(q_num+1)] = q_list
                    sql_exec = "SELECT S.name, ans_"+str(i+1)+" FROM register R LEFT OUTER JOIN students S ON R.hard_id = S.hard_id WHERE course = ? ORDER BY R.hard_id"
                    # print(sql_exec)
                    self.cursor.execute(sql_exec, (self.local_course,))
                    result = self.cursor.fetchall()
                    # print(result)
                    for s in result:
                        ad = {}
                        splits = str(s[1]).split(",")
                        splits.pop(-1)
                        for count in range(len(splits)):
                            ad[str(count+1)] = splits[count]
                        ans[s[0]] = ad
                    dict_to_w ={}
                    dict_to_w["Question"] = qs
                    dict_to_w["Student"] = ans
                    dbm.write_DB(target,dict_to_w)
                except sqlite3.IntegrityError:
                    pass
                    # record delete by admin.


def main():
    database = remote_db()
    database.remote_db_init()

    database.change_user("admin")

    course_list = dbm.read_DB(database.local_cou)

    acc = dbm.read_DB("./JSON_Base/account.json")
    for key,values in acc.items():
        if key == "*":
            pass
        else:
            database.register_teacher(key,"123456",key,values)

    for key,values in course_list.items():
        database.update_teach(database.local_user,(key,))
        database.update_courses(key,"some course","Fall 2019")

    database.change_course("ME_200",1)
    stu_list = dbm.read_DB(database.local_stu)
    for key,values in stu_list.items():
        database.update_students(key,values,"some_id")
        database.register_course(key,(database.local_course,),(database.local_class,))

    database.change_course("Test_Clicker",1)
    stu_list = dbm.read_DB(database.local_stu)
    for key,values in stu_list.items():
        database.update_students(key,values,"some_id")
        database.register_course(key,(database.local_course,),(database.local_class,))

    database.change_user("Rigel")
    course_list = dbm.read_DB(database.local_cou)
    for key,values in course_list.items():
        database.update_teach(database.local_user,(key,))
        database.update_courses(key,"some course","Fall 2019")

    database.change_course("CS_240",1)
    stu_list = dbm.read_DB(database.local_stu)
    for key,values in stu_list.items():
        database.update_students(key,values,"some_id")
        database.register_course(key,(database.local_course,),(database.local_class,))

    database.change_course("ECE_110",1)
    stu_list = dbm.read_DB(database.local_stu)
    for key,values in stu_list.items():
        database.update_students(key,values,"some_id")
        database.register_course(key,(database.local_course,),(database.local_class,))

    database.change_course("Test_Clicker_R")
    stu_list = dbm.read_DB(database.local_stu)
    for key,values in stu_list.items():
        database.update_students(key,values,"some_id")
        database.register_course(key,(database.local_course,),(database.local_class,))
    #______________________test 1: local updates ____________________________
    database.change_course("ECE_110",1)
    #  teacher
    # acc_dict = dbm.read_DB("./JSON_Base/account.json")
    # for key, values in acc_dict.items():
    #     print(key,values)
    #     print(type(values))
    #     database.register_teacher(key,"A123456",key,values)
    #
    # database.register_teacher("Jordan","Aa123456","Akizuki","qwerrtyasdfghzxcvbn")
    # database.sync_local_account()
    # courses----------------
    # course_list = dbm.read_DB(database.local_cou)
    # for key,values in course_list.items():
    #     database.update_courses(key,"some course","Fall 2019")


    # database.update_students(1233445,"dummy","dummy")
    # database.register_course(1233445,("CS_240",),(1,))
    # database.change_course("CS_240",1)
    #
    # database.local_student_update()
    database.result_update(1)
    database.result_update(2)
    database.result_update(3)



if __name__ == "__main__":
    main()