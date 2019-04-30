import os
from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from datetime import datetime
from functools import wraps
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
visitation_db = os.path.join(BASE_DIR, "visit.db")



app = Flask(__name__)



def insert_into_database(fname, lname, kerberos, student_id, dorm):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    c.execute('''INSERT into students(fname, lname, kerberos, student_id, dorm) VALUES (?,?,?,?,?);''', (fname, lname, kerberos, student_id, dorm))
    conn.commit()
    conn.close()

def insert_into_connections(student1, student2):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    c.execute('''INSERT into connections(friend1, friend2) VALUES (?, ?);''', (student1, student2))
    conn.commit()
    conn.close()



def lookup_database(arr):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    things = c.execute('''SELECT * FROM students''').fetchall()
    for row in things:
        arr.append(row)
    conn.commit()
    conn.close()

def lookup_connections(arr):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    things = c.execute('''SELECT * FROM connections''').fetchall()
    for row in things:
        arr.append(row)
    conn.commit()
    conn.close()

def check_login(kerb):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    user = c.execute('''SELECT * FROM students WHERE kerberos = ?''', (kerb, )).fetchone()
    conn.commit()
    conn.close()
    return user
def fetch_user(studentID):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    user = c.execute('''SELECT * FROM students WHERE student_id = ?''', (studentID, )).fetchone()
    conn.commit()
    conn.close()
    return user
def fetch_user_by_id(id):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    user = c.execute('''SELECT * FROM students WHERE id = ?''', (id, )).fetchone()
    conn.commit()
    conn.close()
    return user
def get_conns_of_user(id, conn_list):
    conn = sqlite3.connect(visitation_db)
    c = conn.cursor()
    conns = c.execute('''SELECT * FROM connections WHERE friend2 = ?''', (id, )).fetchall()
    for c in conns:
        conn_list.append(c)
    conn.commit()
    conn.close()




def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return render_template('login.html')
    return wrap


import visit.views
