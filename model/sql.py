import sqlite3

def conn():
    conn = sqlite3.connect('user.db',check_same_thread=False)
    print('Open successfully')
    c = conn.cursor()
    conn.commit()
    conn.close()

def addUser(name,password):
    conn = sqlite3.connect('user.db',check_same_thread=False)
    c = conn.cursor()
    c.execute("insert into user (name, password) values ('%s','%s');"%(name,password))
    conn.commit()
    conn.close()

def findName(name):
    conn = sqlite3.connect('user.db',check_same_thread=False)
    c = conn.cursor()
    c.execute("select name from user where name = '%s'"%name)
    print("select name from user where name = '%s'"%name)
    conn.commit()
    a = c.fetchall()
    conn.close()
    return a

def findPassword(name):
    conn = sqlite3.connect('user.db',check_same_thread=False)
    c = conn.cursor()
    c.execute("select password from user where name = '%s'"%name)
    conn.commit()
    a = c.fetchall()
    conn.close()
    return a

def findAll():
    conn = sqlite3.connect('user.db',check_same_thread=False)
    c = conn.cursor()
    c.execute("select * from user")
    conn.commit()
    a = c.fetchall()
    conn.close()
    return a

