# connect the test backend to the database.
# add the database to the local files.

# Init local DB.
# Create and init the local SQLite 3 database. only for temp use.
# create student info, class into. this would store both online and offline.
# Will transmit to online db when network connection established.
# temp storage: each class would create an table to store stat for each question, temp table
# for student answers. After upload, both would be drop.
import sqlite3 as sql

rdb = sql.connect("remote.db")
ldb = sql.connect("Local.db")

def remote_db_init(db:sql.Connection):
    cursor = db.cursor()
    cursor.execute("CREATE TABLE students("
                   "net_id CHAR(10) NOT NULL, "
                   "hard_id INT(10) , "
                   "name CHAR(10),"
                   "PRIMARY KEY (net_id))")
    cursor.execute("CREATE TABLE classes("
                   "code CHAR(7) NOT NULL , "
                   "name CHAR(20), "
                   "PRIMARY KEY (code))")
    cursor.execute("CREATE TABLE register("
                   "code CHAR(7) NOT NULL, "
                   "net_id CHAR(10) NOT NULL, "
                   "score REAL, "
                   "PRIMARY KEY (code,id),"
                   "FOREIGN KEY (code)"
                   "    REFERENCES classes(code)"
                   "    ON UPDATE CASCADE "
                   "    ON DELETE CASCADE,"
                   "FOREIGN KEY (net_id)"
                   "    REFERENCES students(net_id)"
                   "    ON UPDATE CASCADE "
                   "    ON DELETE CASCADE,"
                   "CHECK (score >= 0 AND score <= 100) )")
    cursor.execute("CREATE TABLE auth("
                   "user CHAR(20) NOT NULL,"
                   "password CHAR(20)"
                   "PRIMARY KEY (user))")
    # setting TRIGGER in the future updates.

    # ADD admin user info. 
    cursor.execute("INSERT INTO auth "
                   "VALUES (?,?)",("admin","admin"))
    db.commit()

# we wont care about the foreign student register, we would only focus on
# collecting data from clickers.
# Thus we only provide student information update API.
def student_info_update(hardware_id:int, name:str, net_id:str):
    # query from the database.
    cursor = rdb.cursor()
    try :
        cursor.execute("UPDATE students "
                       "SET hard_id = ?, name = ?"
                       "WHERE net_id = ? ", (hardware_id,name,net_id))
    except:
        cursor.execute("INSERT INTO students"
                       "VALUES (?,?,?)",(net_id, hardware_id,name))


# init the local db that contends answers for this class. 
def local_db_init():
    cursor = ldb.cursor()
    cursor.execute("CREATE TABLE students"
                   "hard_id INT(10) NOT NULL"
                   "net_id CHAR(10)"
                   "name CHAR(10)"
                   "PRIMARY KEY (hard_id)")
    # answers would be create when class start. 
    ldb.commit()

def class_init(class_name:str):
    