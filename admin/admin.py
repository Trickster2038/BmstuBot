import psycopg2
import settings
import dbutils
from colorlog import bcolors

COMMANDS = ['help', 'moderator-list', 'tables-list', 'sql', 'show-by-id',\
		'show-by-nick', 'grant-moderator-id', 'rm-moderator-id', 'grant-moderator-nick',\
		'rm-moderator-nick', 'set-columns']

dbutils.connect()
db_params = dbutils.get_settings()
print(bcolors.OKGREEN + 'Database:\n' + \
f'name: {db_params.name}\n' + \
f'user: {db_params.user}\n' + \
f'host: {db_params.host}\n' + bcolors.ENDC)

print("Input 'help' to see comands list\n")

while True:
	print(bcolors.OKCYAN + f'\n{db_params.host}:{db_params.user}' + bcolors.ENDC + '$ ', end='')
	cmd = input()

	if cmd == 'help':
		print('Commands:')
		for x in COMMANDS:
			print(f" {x}")
	elif cmd == "moderators-list":
		print(dbutils.moderators_list()) 
	elif cmd == "tables-list":
		print(dbutils.tables_list())
	else:
			if cmd in COMMANDS:
				try:
					arg = input("> ")
					if cmd == 'sql':
						print(dbutils.request(arg))
					elif cmd == 'show-by-id':
						print(dbutils.show_by_id(arg))
					elif cmd == 'show-by-nick':
						print(dbutils.show_by_nickname(arg))
					elif cmd == 'grant-moderator-id':
						print(dbutils.grant_moderator_by_id(arg))
						print(bcolors.OKGREEN + 'SUCCESS\n' + bcolors.ENDC)
					elif cmd == 'rm-moderator-id':
						print(dbutils.rm_moderator_by_id(arg))
						print(bcolors.OKGREEN + 'SUCCESS\n' + bcolors.ENDC)
					elif cmd == 'grant-moderator-nick':
						print(dbutils.grant_moderator_by_nickname(arg))
						print(bcolors.OKGREEN + 'SUCCESS\n' + bcolors.ENDC)
					elif cmd == 'rm-moderator-nick':
						print(dbutils.rm_moderator_by_nickname(arg))
						print(bcolors.OKGREEN + 'SUCCESS\n' + bcolors.ENDC)
					elif cmd == 'set-columns':
						print(dbutils.set_columns(arg))
						print(bcolors.OKGREEN + 'SUCCESS\n' + bcolors.ENDC)
					else:
						print(bcolors.FAIL + f'Commandline failure: {cmd}' + bcolors.ENDC)
				except Exception as e:
					print(bcolors.FAIL + str(e) + bcolors.ENDC)
			else:
				print(bcolors.FAIL + f'Unkonown command: {cmd}' + bcolors.ENDC)
				