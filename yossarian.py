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

def main():
	logging.debug("Start main.")
	
	languageNames = ["Portuguese", "Spanish", "Esperanto", "Italian"]
	languageSkills = ["read", "write", "listen", "speak"]
	
	Portuguese = Language(languageNames[0])
	Spanish = Language(languageNames[1])
	Esperanto = Language(languageNames[2])
	Italian = Language(languageNames[3])
	
	conn = sqlite3.connect("yossarian.db")
	with conn:
		cur = conn.cursor()
		if len(sys.argv) >= 2:
			if sys.argv[1]=="list":
				print("Available Languages:")
				for name in languageNames:
					print(name)
				sql = "SELECT Action FROM Actions"
				cur.execute(sql)
				raw_data = cur.fetchall()
				print("\nAvailable Actions:")
				for ii in range(len(raw_data)):
					print(raw_data[ii][0])
		else:
			now = str(datetime.datetime.now().timestamp())
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

if __name__=="__main__":
	main()
