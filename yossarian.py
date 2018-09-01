#yossarian.py

import datetime
import logging
import sqlite3
import sys

logging.basicConfig(filename='yossarian_log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

class Language():
	def __init__(self, name):
		self.name = name
		self.read = 0
		self.write = 0
		self.listen = 0
		self.speak = 0

languageNames = ["Portuguese", "Spanish", "Esperanto", "Italian"]
languageSkills = ["read", "write", "listen", "speak"]
Portuguese = Language(languageNames[0])
Spanish = Language(languageNames[1])
Esperanto = Language(languageNames[2])
Italian = Language(languageNames[3])

def list_options(cur):
	print("Available Languages:")
	for name in languageNames:
		print(name)
	sql = "SELECT Action FROM Actions"
	cur.execute(sql)
	results = cur.fetchall()
	print("\nAvailable Actions:")
	for ii in range(len(results)):
		print(results[ii][0])

def view_progress(cur):
	sql = "SELECT PK, Language, Action, Quantity, Datetime FROM History"
	cur.execute(sql)
	raw_data = cur.fetchall()
	for ii in range(len(raw_data)):
		cur.execute("SELECT * FROM Actions WHERE Action=?", (raw_data[ii][2],))
		weights = cur.fetchone()
		quantity = raw_data[ii][3]
		eval(raw_data[ii][1]).read += weights[2] * quantity
		eval(raw_data[ii][1]).write += weights[3] * quantity
		eval(raw_data[ii][1]).listen += weights[4] * quantity
		eval(raw_data[ii][1]).speak += weights[5] * quantity
	
	for lang in languageNames:
		for skill in languageSkills:
			print("{} {}: {}".format(lang, skill, getattr(eval(lang), "{}".format(skill))))
			
def add_training(cur, language, action, quantity):
	now = str(datetime.datetime.now().timestamp())	
	cur.execute("INSERT INTO History (Language, Action, Quantity, Datetime) VALUES (?, ?, ?, ?);", (language, action, quantity, now))

def help_menu():
	print("The following run commands are supported:")
	print("status  // View statistics")
	print("list    // See the supported languages and activities")
	print("add     // Add training to history. Must be followed by Language Action Quantity")

def main():
	logging.debug("Start main.")
	conn = sqlite3.connect("yossarian.db")
	with conn:
		cur = conn.cursor()
		if len(sys.argv) >= 2:
			if sys.argv[1]=="list":
				list_options(cur)
			elif sys.argv[1]=="status":
				view_progress(cur)
			elif sys.argv[1]=="add":
				if len(sys.argv)==5:
					add_training(cur, sys.argv[2], sys.argv[3], sys.argv[4])
				else:
					print("When adding there need to be three additional arguments: Language, Action and Quantity.")
			else:
				help_menu()
		else:
			help_menu()

if __name__=="__main__":
	main()
