from json import *

# ------------JSON Database------------
def read_DB(db_path):
    jf = open(db_path, "r+")
    dict_out = load(jf)
    jf.close()
    return dict_out

def write_DB(db_path, dict_in):
    jf = open(db_path, "w+")
    dump(dict_in, jf, indent=4)
    jf.close()
    return