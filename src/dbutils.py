import settings
import psycopg2
import os.path
import re

def validShortString(str):
    return (len(str) < 20) and (re.match( r'[a-яА-Я]', str, re.M|re.I))

def validLongString(str):
    return (len(str) < 400) 

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

def get_info(id):
    cursor.execute("SELECT name, surname, faculty, department, course, trusted, bio, username  from public.users where id = {}".format(id))
    result = cursor.fetchone()
    return result

def pop_moderator_pool(id):
    cursor.execute("SELECT id  from public.users where id <> {} and trusted = 1 ORDER BY RANDOM() LIMIT 1".format(id))
    result = cursor.fetchone()
    if result != None:
        result = int(result[0])
    return result

def avatar_exists(id):
    return os.path.isfile("avatars/" + str(id) + ".jpg")

def verify_exists(id):
    return os.path.isfile("verify/" + str(id) + ".jpg")

def write_name(id, str, nick):
    name = make_capital(str)
    cursor.execute("INSERT into public.\"users\" values ({}, '{{{}}}', null, null, null, null, default, default, default, '{{{}}}', null, default, default)"\
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

def write_bio(id, bio):
    bio = [bio]
    cursor.execute("""
            Update
                public.users
            set
                bio = %(bio)s
            WHERE
                id = %(id)s
        """, {
            'bio': bio,
            'id': id
        })

def id_exists(id):
    cursor.execute("SELECT * FROM public.users where id = {}".format(id))
    res = cursor.fetchone()
    return res != None

def is_filled(id):
    cursor.execute("SELECT is_filled from public.users where id = {}".format(id))
    result = cursor.fetchone()
    if result == None:
        result = [False]
    return result[0]

def is_moderator(id):
    cursor.execute("SELECT is_moderator from public.users where id = {}".format(id))
    result = cursor.fetchone()
    if result == None:
        result = [False]
    return result[0]

def drop_trusted(id):
    cursor.execute("UPDATE public.\"users\" set \"trusted\" = 0 where id = {}"\
        .format(id))   

def grant_trusted(id):
    cursor.execute("UPDATE public.\"users\" set \"trusted\" = 2 where id = {}"\
        .format(id))

def turn_moderate(id):
    cursor.execute("UPDATE public.\"users\" set \"trusted\" = 1 where id = {}"\
        .format(id))   

def get_faculty_id(id):
    cursor.execute("SELECT faculty FROM public.users where id = {}".format(id))
    res = cursor.fetchone()
    return int(res[0])

def delete(id):
    cursor.execute("DELETE FROM public.users where id = {}".format(id))

def finish_registration(id):
    cursor.execute("SELECT * from public.users where id = {}".format(id))
    result = cursor.fetchone()
    fl = True
    for x in result:
        if x == None:
            fl = False
    if fl:
        cursor.execute("UPDATE public.\"users\" set \"is_filled\" = True where id = {}"\
            .format(id))
    return fl