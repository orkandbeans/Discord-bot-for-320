import os
import sqlite3

DB_PATH = "C:\\Users\\Viscount\\Documents\\GitHub\\Discord-bot-for-320\\data\\db\\database.db"

cxn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()

def commit():
    cxn.commit()

def close():
    cxn.close()

def field(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()

def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()

def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]

def execute(command, *values):
    cur.execute(command, tuple(values))

def multiexec(command, valueset):
    cur.executemany(command, valueset)

def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())

def rowCount():
    return cur.rowcount
