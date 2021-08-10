import settings
import psycopg2
import re

def validShortString(str):
    return (len(str) < 20) and (re.match( r'[a-яА-Я]', str, re.M|re.I))

def make_capital(str):
    return  str[0].upper() + str[1:].lower()

def connect():
    db = settings.DB
    global conn
    conn = psycopg2.connect(dbname=db.name, user=db.user, 
                        password=db.password, host=db.host)
    conn.autocommit = True
    global cursor
    cursor = conn.cursor()

def write_name(id, str, nick):
    name = make_capital(str)
    cursor.execute("INSERT into public.\"users\" values ({}, '{{{}}}', null, null, null, null, null, default, default, default, default, '{{{}}}', null)"\
        .format(id, name, nick))

def write_surname(id, str):
    surname = make_capital(str)
    cursor.execute("UPDATE public.\"users\" set \"surname\" = '{{{}}}' where id = {}"\
        .format(surname, id))

def write_faculty(id, code):
    cursor.execute("UPDATE public.\"users\" set \"faculty\" = {} where id = {}"\
        .format(code, id))

def write_department(id, code):
    cursor.execute("UPDATE public.\"users\" set \"department\" = {} where id = {}"\
        .format(code, id))

def write_course(id, code):
    cursor.execute("UPDATE public.\"users\" set \"course\" = {} where id = {}"\
        .format(code, id))

def id_exists(id):
    cursor.execute("SELECT * FROM public.users where id = {}".format(id))
    res = cursor.fetchone()
    return res != None

def get_faculty_id(id):
    cursor.execute("SELECT faculty FROM public.users where id = {}".format(id))
    res = cursor.fetchone()
    return int(res[0])

def delete(id):
    cursor.execute("DELETE FROM public.users where id = {}".format(id))