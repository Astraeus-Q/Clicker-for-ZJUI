# connect the test backend to the database.
# add the database to the local files.

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
    def remote_db_init(self):
        self.cursor.execute("DROP TABLE IF EXISTS register")
        # careful not to call the function after data storage.
        # self.cursor.execute("DROP TABLE IF exists students,courses,register,teachers,teach,grades,weekly")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS students("
                       "hard_id CHAR(10) NOT NULL, "
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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS grades("
                       "hard_id CHAR(10) NOT NULL,"
                       "course CHAR(10) NOT NULL,"
                       "PRIMARY KEY (hard_id,course),"
                       "FOREIGN KEY (hard_id)"
                       "    REFERENCES students(hard_id)"
                       "    ON UPDATE CASCADE "
                       "    ON DELETE CASCADE,"
                       "FOREIGN KEY (course)"
                       "    REFERENCES courses(course)"
                       "    ON UPDATE CASCADE "
                       "    ON DELETE CASCADE)")

        # dense storage, clear per semester.
        self.cursor.execute("CREATE TABLE IF NOT EXISTS weekly("
                            "course CHAR(10) NOT NULL,"
                            "class INT(10) NOT NULL,"
                            "week INT(10) NOT NULL,"
                            "title CHAR(20),"
                            "total INT(10),"
                            "attend INT(10),"
                            "c_date DATE,"
                            "PRIMARY KEY (course,class,week),"
                            "FOREIGN KEY (course)"
                            "   REFERENCES courses(course)"
                            "   ON UPDATE CASCADE "
                            "   ON DELETE CASCADE )")
        # setting TRIGGER in the future updates.

        # ADD admin user info.
        self.cursor.execute("INSERT INTO teachers "
                       "VALUES (?,?,?)",("admin","admin","admin"))

        self.db.commit()

    # we will not care about the foreign student register, we would only focus on
    # collecting data from clickers.
    # Thus we only provide student information update API.
    def update_students(self,hardware_id:int, name:str, net_id:str):
        try :
            self.cursor.execute("UPDATE students "
                           "SET net_id = ?, name = ?"
                           "WHERE hard_id = ? ", (net_id, name, hardware_id))
        except:
            self.cursor.execute("INSERT INTO students "
                           "VALUES (?,?,?)",(hardware_id, net_id, name))

    def register_teacher(self,user_name:str, pwd:str, name:str):
        # register user into the database.
        try :
            self.cursor.execute("UPDATE teachers "
                                "SET password = ?, name = ?"
                                "WHERE user = ?", (pwd,name,user_name))
        except:
            self.cursor.execute("INSERT INTO teachers "
                                "VALUES (?,?,?)",(user_name,pwd,name))
    def change_pass(self,user_name:str,pwd:str):
        self.cursor.execute("UPDATE teachers "
                            "SET password = ? "
                            "WHERE user = ?",(pwd,user_name))
    def update_teach(self,user_name:str, courses:tuple,add = True):
        # allow multiple teacher teach same course.
        if add:
            for c in courses:
                self.cursor.execute("INSERT INTO teach "
                                    "VALUES (?,?)",(user_name,c))
        else:
            for c in courses:
                self.cursor.execute("DELETE FROM teach "
                                    "WHERE teacher = ?, course = ?",(user_name,c))
    def register_course(self,net_id:str, courses:tuple,class_num:int ,add = True):
        if add:
            for c in courses:
                self.cursor.execute("INSERT INTO register "
                                    "VALUES (?,?,?)",(c,net_id,class_num))
        else:
            for c in courses:
                self.cursor.execute("DELETE FROM register "
                                    "WHERE net_id = ?, code = ?",(net_id,c))
    def update_courses(self, course_number:str, course_name:str, semester:str):
        try :
            self.cursor.execute("UPDATE courses "
                                "SET name = ?, semester = ?"
                                "WHERE course = ?", (course_name, semester, course_number))
        except:
            self.cursor.execute("INSERT INTO courses "
                                "VALUES (?,?,?)", (course_number, course_name, semester))
    def local_update_course(self,user_name:str):
        course_list = {}
        try:
            courses = self.cursor.execute("SELECT course FROM teach "
                                              "WHERE user = ?",user_name)
            for c in courses:
                course_list[c] = {}
        except:
            print(" USER NOT EXISTS! ")

        dbm.writeDB(self.local_cou,course_list)

    def local_student_update(self):
        # read the local hardware id, pull the name and net_id into the local.
        student_list = dbm.read_DB(self.local_stu)
        info_tag = []
        for key,value in student_list.item():
            if value == "":
                try:
                    info_tag = self.cursor.execute("SELECT name FROM students "
                                                   "WHERE hard_id = ?", (key))
                    student_list[key] = info_tag[0]
                except:
                    pass
        dbm.writeDB(self.local_stu,student_list)
    def result_update(self, course_count:int):

        record = "./" + self.local_user + "/" + self.local_course + "/" + \
                 str(course_count) + ".json"
        try :
            dump_dict = dbm.read_DB(record)
            course_dict = dbm.read_DB(self.local_cou)
            student_dict = dmb.read_DB(self.local_stu)
        except:
            print("? QYNZGSM ?")
            return

        c_i = course_dict[self.local_course][str(course_count)]
        new_stu = False
        # first update the course record.
        self.cursor.execute("INSERT INTO weekly "
                            "VALUES (?,?,?,?,?,?,?)", (self.local_course,self.local_class,course_count,c_i[1],c_i[2],c_i[3],c_i[3]/c_i[2],c_i[0]))
        # then update the students.
        ans = dump_dict["Student"]
        qs= dump_dict["Question"]

        # TODO: find out how to detect new students with QY.
        # finally update the grades.
        # detect if the column exist.
        try:
            self.cursor.execute("SELECT ? FROM register "
                                "LIMIT 1", (course_count))
        except:
            sql_exec = "ALTER TABLE register ADD COLUMN " + str(course_count) + " REAL"
            self.cursor.execute(sql_exec)
        self.db.commit()    # important for consistency in transaction.
        # update student grades
        for key,values in answers.items():
            # key: student name, value, dict of answers.
            total_score = 0
            for num,ans in values.item():
                if (scores[num][0] == ans):
                    total_score += scores[num][4]
            # record the data into the grades.
            # sql_exec = "UPDATE register SET " + str(course_count) + " = "
            self.cursor.execute("UPDATE register "
                                "SET ? = ? "
                                "WHERE hard_id = ?, course = ? ", (str(course_count), total_score, key, self.local_course))

database = remote_db()
database.remote_db_init()