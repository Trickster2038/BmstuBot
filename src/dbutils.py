import settings
import psycopg2
import datetime
import os.path
import os
import re
from django.contrib.auth.hashers import make_password

def validShortString(str):
    return (len(str) < 20) and (re.match( r'[a-яА-Я]', str, re.M|re.I))

def validLongString(str):
    return (len(str) < 400) 

def make_capital(str):
    return  str[0].upper() + str[1:].lower()

def connect():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
    db = settings.DB
    global conn
    conn = psycopg2.connect(dbname=db.name, user=db.user, 
                        password=db.password, host=db.host)
    conn.autocommit = True
    global cursor
    cursor = conn.cursor()

def get_info(id):
    cursor.execute(f"SELECT beta_persont.name, beta_persont.surname, beta_facultiest.name, \
    beta_persont.department, beta_persont.course, beta_persont.trusted, beta_persont.bio,  \
    beta_persont.username, beta_persont.is_moderator, beta_persont.is_curator \
    FROM beta_persont JOIN beta_facultiest ON beta_persont.faculty = beta_facultiest.id \
    WHERE  beta_persont.id = {id}")
    result = cursor.fetchone()
    return result

def pop_moderator_pool(id):
    cursor.execute(f"SELECT id from beta_persont where id <> {id} and trusted = 1 ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    if result != None:
        result = int(result[0])
    return result

def avatar_exists(id):
    return os.path.isfile("../media/avatars/" + str(id) + ".jpg")

def verify_exists(id):
    return os.path.isfile("../media/verify/" + str(id) + ".jpg")

# db test >>>
def write_name(id, str, nick):
    name = make_capital(str)
    cursor.execute(f"INSERT beta_persont values ({id}, '{name}', ' ', 0, \
     0,' ', false, 0, 0, '{nick}', \
     0, 0, false, false)")

def write_surname(id, str1):
    surname = make_capital(str1)
    cursor.execute(f"UPDATE beta_persont set surname = '{surname}' where id = {id}")

def write_faculty(id, code):
    cursor.execute(f"UPDATE beta_persont set faculty = {code} where id = {id}")

def write_department(id, code):
    cursor.execute(f"UPDATE beta_persont set department = {code} where id = {id}")

def write_course(id, code):
    cursor.execute(f"UPDATE beta_persont set  course = {code} where id = {id}")
# /db test

def write_curator(id, fl):
    cursor.execute(f"UPDATE beta_persont set is_curator = {fl} where id = {id}")

def write_bio(id, bio):
    cursor.execute(f"UPDATE beta_persont set bio = '{bio}' where id = {id}")
    bio = [bio]

def id_exists(id):
    cursor.execute(f"SELECT * FROM beta_persont where id = {id}")
    res = cursor.fetchone()
    return res != None

def is_filled(id):
    cursor.execute(f"SELECT is_filled from beta_persont where id = {id}")
    result = cursor.fetchone()
    if result == None:
        result = [False]
    return result[0]

def is_moderator(id):
    cursor.execute("SELECT is_moderator from beta_persont where id = {}".format(id))
    result = cursor.fetchone()
    if result == None:
        result = [False]
    return result[0]

def drop_trusted(id):
    cursor.execute("UPDATE beta_persont set trusted = 0 where id = {}"\
        .format(id))   

def grant_trusted(id):
    cursor.execute(f"UPDATE beta_persont set trusted = 2 where id = {id}")

def turn_moderate(id):
    cursor.execute(f"UPDATE beta_persont trusted = 1 where id = {id}")

# def get_faculty_id(id):
#     cursor.execute("SELECT faculty FROM public.users where id = {}".format(id))
#     res = cursor.fetchone()
#     return int(res[0])

# TODO: from all tables
def delete(id):
    cursor.execute(f"DELETE FROM beta_persont where id = {id}")

def finish_registration(id):
    cursor.execute(f"SELECT * from beta_persont where id = {id}")
    result = cursor.fetchone()
    fl = True
    for x in result:
        if x == None:
            fl = False
    if fl:
        cursor.execute(f"UPDATE beta_persont set is_filled = True where id = {id}")
    return fl

# =========================================

def pop_potential_friend_unsafe(id):
    data = get_info(id)
    req = """SELECT users.id from beta_persont, beta_friendst \
        where beta_persont.id <> {} and faculty = {}
        and department = {} and course > {} and is_curator and is_filled \
        and not(user1 = {} and user2 = beta_persont.id)
        and user1 = {}
        ORDER BY RANDOM() LIMIT 1""".format(id, data[2], data[3], data[4], id, id)
    cursor.execute(req)
    # print(req)
    result = cursor.fetchone()
    if result != None:
        result = int(result[0])
    return result

def pop_potential_friend_safe(id):
    data = get_info(id)
    req = """SELECT users.id from beta_persont, beta_friendst \
            where beta_persont.id <> {} and faculty = {}
            and department = {} and course > {} and is_curator and is_filled \
            and trusted = 2 \
            and not(user1 = {} and user2 = beta_persont.id)
            and user1 = {}
            ORDER BY RANDOM() LIMIT 1""".format(id, data[2], data[3], data[4], id, id)
    cursor.execute(req)
    result = cursor.fetchone()
    if result != None:
        result = int(result[0])
    return result

# db edit >>>

def request_friendship(id_from, id_to):
    cursor.execute("SELECT count(*) from beta_friendst where user1 = {} and user2 = {}".format(id_from, id_to))
    result = cursor.fetchone()
    new_request = (int(result[0]) == 0)
    if new_request:
        cursor.execute("INSERT into beta_friendst values (default, {}, {}, false)".format(id_from, id_to))
    return new_request

def get_incoming(id, n):
    cursor.execute("SELECT user1  from beta_friendst where user2 =  {} and not applied ORDER BY RANDOM() LIMIT {}"\
        .format(id, n))
    result = cursor.fetchall()
    data = []
    for x in result:
        data.append(int(x[0]))
    return data

def discard_friend(id1, id2):
    cursor.execute("DELETE from beta_friendst where (user1 = {} and user2 = {}) or (user1 = {} and user2 = {})"\
        .format(id1, id2, id2, id1))

def apply_friend(apply_id, id):
    cursor.execute("SELECT count(*) from beta_friendst where user1 = {} and user2 = {} and not applied".format(apply_id, id))
    result = cursor.fetchone()
    request_exists = (int(result[0]) == 1)
    if request_exists:
        cursor.execute("UPDATE beta_friendst set applied = True where user1 = {} and user2 = {}"\
        .format(apply_id, id))
    return request_exists

def get_outcoming(id, n):
    print("> get outcoming")
    req = "SELECT user2 from beta_friendst where user1 = {} and not applied ORDER BY RANDOM() LIMIT {}"\
        .format(id, n)
    cursor.execute(req)
    result = cursor.fetchall()
    data = []
    for x in result:
        data.append(int(x[0]))
    return data

def get_curators(id, n):
    req = "SELECT user2 from beta_friendst where user1 = {} and applied ORDER BY RANDOM() LIMIT {}"\
        .format(id, n)
    cursor.execute(req)
    result = cursor.fetchall()
    data = []
    for x in result:
        data.append(int(x[0]))
    return data

def get_mypeople(id, n):
    cursor.execute("SELECT user1  from beta_friendst where user2 =  {} and applied ORDER BY RANDOM() LIMIT {}"\
        .format(id, n))
    result = cursor.fetchall()
    data = []
    for x in result:
        data.append(int(x[0]))
    return data

# ==========================================

def set_password(id, password):
    id = str(id)
    password_hash = make_password(password)

    query = "SELECT count(*) from auth_user where username='{}'".format(id)
    cursor.execute(query)
    result = cursor.fetchone()
    is_new = (int(result[0]) == 0)

    if is_new:
        ts = datetime.datetime.now()
        ts = str(ts).split(".")[0]
        query = "INSERT into auth_user values (default, '{}', TIMESTAMP '{}', false, '{}',\
        '', '', '', false , true, TIMESTAMP '{}')".format(password_hash, ts, id, ts)
    else:
        query = "UPDATE auth_user set password='{}' where username='{}'".format(password_hash, id)
    cursor.execute(query)
