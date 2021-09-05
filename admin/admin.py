import psycopg2
import settings

def connect(db):
    global conn
    conn = psycopg2.connect(dbname=db.name, user=db.user, 
                        password=db.password, host=db.host)
    conn.autocommit = True
    global cursor
    cursor = conn.cursor()
    return cursor

db = settings.DB
cursor = connect(db)

actions = ["очистить БД", "заполнить БД тестовыми данными", "Назначить модератора", "Удалить модератора"]

def confirm(s):
	print("Подтвердите действие ({}) [введите y]:".format(s))
	decision = input()
	return decision == "y"

while True:
	print("Введите номер команды:")
	for i in range(len(actions)):
		print("({}) {}".format(i, actions[i]))
	print("\n")
	cmd = int(input())
	if cmd == 0:
		if confirm(a[1]):
		else:
			print("отмена")
	elif cmd == 1:
		if confirm(a[1]):
		else:
			print("отмена")
	elif cmd == 2:
		print("Введите его id:")
		id = input()
	elif cmd == 3:
		print("Введите его id:")
		id = input()
	else:
		print("Неизвестная команда")
	print("Команда выполнена")