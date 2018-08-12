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
	for i in range(len(matt.languages)):
		print(matt.languages[i].name)
		print("Reading: {}".format(matt.languages[i].read))
		print("Writing: {}".format(matt.languages[i].write))
		print("Listening: {}".format(matt.languages[i].listen))
		print("Speaking: {}".format(matt.languages[i].speak))
		print("")

def main():
	matt = User("Matt")
	matt.add_language(Language("Portuguese"))
	for i in range(len(matt.languages)):
		if matt.languages[i].name == "Portuguese":
			#matt.languages[i].legacy(25,50,100,200)
			#matt.languages[i].duolingo(50)
			break
	matt.add_language(Language("Spanish"))
	for i in range(len(matt.languages)):
		if matt.languages[i].name == "Spanish":
			#matt.languages[1].legacy(10,20,30,40)
			#matt.languages[i].podcast(12)
			break
	matt.add_language(Language("Esperanto"))
	for i in range(len(matt.languages)):
		if matt.languages[i].name == "Esperanto":
			#matt.languages[1].legacy(10,20,30,40)
			matt.languages[i].duolingo(90)
			break
	matt.add_language(Language("Italian"))
	for i in range(len(matt.languages)):
		if matt.languages[i].name == "Italian":
			#matt.languages[1].legacy(10,20,30,40)
			#matt.languages[i].podcast(12)
			break
	display_stats(matt)

if __name__=="__main__":
	main()
