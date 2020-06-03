import sqlite3

def initDB():
    conn = sqlite3.connect('bilistat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE user(
        MID     TEXT PRIMARY KEY    NOT NULL,
        NAME    TEXT                NOT NULL,
        SEX     TEXT                NOT NULL,
        FANS    LONG,
        ATTENTION   TEXT,
        LEVEL   TEXT,
        FACE    TEXT,
        SIGN    TEXT);''')
    conn.commit()


    conn.close()

# initDB()

def gettop2up(conn):
    c = conn.cursor()
    result = c.execute("SELECT NAME, FANS, FACE, MID FROM USER ORDER BY FANS DESC;")
    r = []
    for row in result:
        r.append((row[0], row[1], row[2], row[3]))
    return r

def gettop10up(conn):
    c = conn.cursor()
    result = c.execute("SELECT NAME, FANS, FACE, SIGN, MID FROM USER ORDER BY FANS DESC;")
    r = []
    for row in result:
        r.append([row[0], row[1], row[2], row[3], row[4]])
    return r

def getdayrank10(conn):
    c = conn.cursor()
    result = c.execute("SELECT AUTHOR, PLAY, PIC, TITLE, BVID FROM DAYRANK LIMIT 10;")
    r = []
    for row in result:
        r.append(row)
    return r

def getmonthrank10(conn):
    c = conn.cursor()
    result = c.execute("SELECT AUTHOR, PLAY, PIC, TITLE, BVID FROM MONTHRANK LIMIT 10;")
    r = []
    for row in result:
        r.append(row)
    return r
