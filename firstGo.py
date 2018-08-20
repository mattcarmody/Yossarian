import shelve

class User():
	def __init__(self, name):
		self.name = name
		self.languages = []
		
	def add_language(self, language):
		self.languages.append(language)
		
class Language():
	def __init__(self, name):
		self.name = name
		self.read = 0
		self.write = 0
		self.listen = 0
		self.speak = 0
	def legacy(self, read, write, listen, speak):
		self.read += read
		self.write += write
		self.listen += listen
		self.speak += speak
	def duolingo(self, score):
		self.read += int(score)
		self.write += int(score)
		self.listen += int(score/3)
		self.speak += int(score/3)
	def podcast(self, score):
		self.listen += score*3
		print("You earned {} xp in {} listening during that podcast session!".format(score*3, self.name))

def display_stats(matt):
	print("\n{}, here is your xp:\n".format(matt.name))
	for ii in range(len(matt.languages)):
		print(matt.languages[ii].name)
		print("Reading: {}".format(matt.languages[ii].read))
		print("Writing: {}".format(matt.languages[ii].write))
		print("Listening: {}".format(matt.languages[ii].listen))
		print("Speaking: {}".format(matt.languages[ii].speak))
		print("")

def main():
	matt = User("Matt")
	matt.add_language(Language("Portuguese"))
	for ii in range(len(matt.languages)):
		if matt.languages[ii].name == "Portuguese":
			matt.languages[ii].legacy(25,50,100,200)
			matt.languages[ii].duolingo(50)
			break
	matt.add_language(Language("Spanish"))
	for ii in range(len(matt.languages)):
		if matt.languages[ii].name == "Spanish":
			matt.languages[ii].legacy(10,20,30,40)
			matt.languages[ii].podcast(12)
			break
	matt.add_language(Language("Esperanto"))
	for ii in range(len(matt.languages)):
		if matt.languages[ii].name == "Esperanto":
			matt.languages[ii].legacy(10,20,30,40)
			matt.languages[ii].duolingo(90)
			break
	matt.add_language(Language("Italian"))
	for ii in range(len(matt.languages)):
		if matt.languages[ii].name == "Italian":
			matt.languages[ii].legacy(10,20,30,40)
			matt.languages[ii].podcast(12)
			break
	display_stats(matt)

if __name__=="__main__":
	main()
	
'''
def open_wb(filename):
	wb = openpyxl.load_workbook(filename)
	return wb

	
	wb = open_wb("Yossarian.xlsx")
	history_sheet = wb.get_sheet_by_name("History")
	for r in range(2, history_sheet.max_row+1):
		if history_sheet.cell(row=r, column=2).value == "Duolingo_Esperanto":
			matt.languages[2].duolingo(history_sheet.cell(row=r, column=3).value)
'''
