import settings
import psycopg2
import datetime
import os.path
import os
import re
import pandas as pd
# from django.contrib.auth.hashers import make_password

pd.options.display.width = 0
SELECT_COLUMNS = 'beta_persont.id, beta_persont.name, beta_persont.surname, \
beta_facultiest.name as faculty, beta_persont.department as dept, beta_persont.course, \
beta_persont.is_moderator as moderator'

def connect():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'
    db = settings.DB
    global conn
    conn = psycopg2.connect(dbname=db.name, user=db.user, 
                        password=db.password, host=db.host)
    conn.autocommit = True
    global cursor
    cursor = conn.cursor()
    return cursor

def get_settings():
    return settings.DB

def set_columns(cols):
    global SELECT_COLUMNS 
    SELECT_COLUMNS = cols
    return cols

def request(req):
    result = pd.read_sql(req, conn)
    return result

def show_by_id(id):
    result = pd.read_sql(f'select {SELECT_COLUMNS} from beta_persont\
    JOIN beta_facultiest ON beta_persont.faculty = beta_facultiest.id\
    where beta_persont.id = {id}', conn)
    return result

def show_by_nickname(nick):
    result = pd.read_sql(f"select {SELECT_COLUMNS} from beta_persont\
    JOIN beta_facultiest ON beta_persont.faculty = beta_facultiest.id\
    where beta_persont.username = '{nick}'", conn)
    return result

def grant_moderator_by_id(id):
    cursor.execute(f"update beta_persont set is_moderator = True where id = {id}")
    return show_by_id(id)

def rm_moderator_by_id(id):
    cursor.execute(f"update beta_persont set is_moderator = False where id = {id}")
    return show_by_id(id)

def grant_moderator_by_nickname(nick):
    cursor.execute(f"update beta_persont set is_moderator = True where username = '{nick}'")
    return show_by_nickname(nick)

def rm_moderator_by_nickname(nick):
    cursor.execute(f"update beta_persont set is_moderator = False where username = '{nick}'")
    return show_by_nickname(nick)

def moderators_list():
    result = pd.read_sql(f'select {SELECT_COLUMNS} from beta_persont\
    JOIN beta_facultiest ON beta_persont.faculty = beta_facultiest.id\
    where beta_persont.is_moderator = True', conn)
    return result

def tables_list():
    result = pd.read_sql("select tablename from pg_catalog.pg_tables \
    where schemaname = 'public'", conn)
    return result

# def pop_moderator_pool(id):
#     cursor.execute("SELECT id  from public.users where id <> {} and trusted = 1 ORDER BY RANDOM() LIMIT 1".format(id))
#     result = cursor.fetchone()
#     if result != None:
#         result = int(result[0])
#     return result

