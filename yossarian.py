#yossarian.py

import datetime
import json
import logging
import requests
import sqlite3
import sys

import personal

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
levels = [0,83,174,276,388,512,650,801,969,1154,1358,1584,1833,2107,\
2411,2746,3115,3523,3973,4470,5018,5624,6291,7028,7842,8740,9730,10824,\
12031,13363,14833,16456,18247,20224,22406,24815,27473,30408,33648,37224,\
41171,45529,50339,55649]

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
			xp = getattr(eval(lang), "{}".format(skill))
			ii = 0
			level = 0
			while xp > levels[ii]:
				level += 1
				ii += 1
			print("{} {}: {}    Level {}".format(lang, skill, int(xp), level))
			
def add_training(cur, language, action, quantity):
	now = str(datetime.datetime.now().timestamp())	
	cur.execute("INSERT INTO History (Language, Action, Quantity, Datetime) VALUES (?, ?, ?, ?);", (language, action, quantity, now))

def help_menu():
	print("The following run commands are supported:")
	print("status  // View statistics")
	print("list    // See the supported languages and activities")
	print("add     // Add training to history. Must be followed by Language Action Quantity")
	
def add_duolingo(cur):    
	duo_url = "https://www.duolingo.com/users/{}".format(personal.data["duoUsername"])
	duo_response = requests.get(duo_url)
	duo_response.raise_for_status()
	duo_data = json.loads(duo_response.text)
	
	cur.execute("UPDATE History SET Quantity=? WHERE Language='Esperanto' AND Action='Duolingo' LIMIT 1", (duo_data["languages"][1]["points"] / 10, ))
	cur.execute("UPDATE History SET Quantity=? WHERE Language='Italian' AND Action='Duolingo' LIMIT 1", (duo_data["languages"][3]["points"] / 10, ))
	cur.execute("UPDATE History SET Quantity=? WHERE Language='Spanish' AND Action='Duolingo' LIMIT 1", (duo_data["languages"][8]["points"] / 10, ))
	cur.execute("UPDATE History SET Quantity=? WHERE Language='Portuguese' AND Action='Duolingo' LIMIT 1", (duo_data["languages"][11]["points"] / 10, ))


def main():
	logging.debug("Start main.")
	conn = sqlite3.connect("yossarian.db")
	with conn:
		cur = conn.cursor()
		if len(sys.argv) >= 2:
			if sys.argv[1]=="list":
				list_options(cur)
			elif sys.argv[1]=="status":
				add_duolingo(cur)
				view_progress(cur)
			elif sys.argv[1]=="duolingo":
				add_duolingo(cur)
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
