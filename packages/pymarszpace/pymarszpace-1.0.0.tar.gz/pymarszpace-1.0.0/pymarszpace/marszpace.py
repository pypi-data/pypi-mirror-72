# สื่อก่ารสอน OOP Python โดย CCSleep

import random
import time
from threading import Thread

class Marszpace:
	"""Marszpace, the most sensitive human ever created."""
	def __init__(self):
		"""Initialize his habits."""
		self.name = "Marszpace"
		self.alias = ["Hikari","Tiaritsu","Rem"]
		self.addict = ["osu!","Arcaea","Hypixel Skyblock","Rem","Astroneer","Minecraft","Bedwars"] # there's more that i forgot
		self.hate = ["Classical Music","AlgyCuber","AtomThum","CCSleep","TinnerKung"]
		self.flex = ["osu! pp", "PP", "Fracture Ray","Skyblock Coins","Arcaea","Wishing"]
		self.emotions = ["Sad","Mental Breakdown","A little bit sad","Very sad","Depression","Regretting being born","wants to die","Turn to Rem","**** Rem"]
		self.time = 13

	def ThreadRunner(self,func):
		"""Thread Run so I can run time in background"""
		thread = Thread(target=func)
		thread.start()

	def ignore(self, name="CCSleep", action="going to toilet",game=None):
		"""This is the most common thing that Marszpace do"""
		emotion = random.choice(self.emotions)
		if game == None:
			game = random.choice(self.addict)
		print(f"""Marszpace: No one wants to play {game} with me TwT.
{name}: Calm down bro, I'm just {action}.
Marszpace: So you don't want to play with me?
{name}: No...
Marszpace: NOW YOU'RE NOT MY FRIEND ANYMORE, STAY AWAY FROM MY LIFE
----Marszpace Blocked Your Discord----
Marszpace right now: {emotion}""")
		for i in range(1,random.randint(4,8)):
			print(f"{i} minute(s) passed")
			time.sleep(1)

		print("----Marszpace Joined Back----")
		print("Marszpace: Ummm... Let's pretend that didn't happened.")
		
	def flexing(self):
		"""It's just Marszpace flexing his rhythm games performance, and etc."""
		flex = random.choice(self.flex)
		if flex == "osu! pp": print(f"Marszpace: I have got {random.randint(100,200)} osu! pps today")
		elif flex == "PP": print(f"Marszpace: I have a 12 inch penis")
		elif flex == "Fracture Ray": print("Marszpace: I have beaten Fracture Ray max combo/perfect")
		elif flex == "Skyblock Coins": print(f"Marszpace: I have gained {random.randint(10,30)/10}m skyblock coins today.")
		elif flex == "Arcaea": print(f"Developers: I forgot how did he go when he is flexing Arcaea.")
		elif flex == "Wishing": print(f"Marszpace: Wishing Version {random.randint(1, 999)} is soooooo beautiful, like Rem.")

	def timego(self):
		"""Time Count for _playGames function"""
		while self.time <= 23.5:
			self.time += 0.5
			time.sleep(1)
	
	def _playGames(self,game,name="CCSleep",action="going to bed"):
		"""Base function for playing games with Marszpace, using in Marszpace.Friend()"""
		if game in self.addict:
			print(f"Marszpace: Sure!")
			
			self.ThreadRunner(self.timego)
			input("Press Enter to stop playing games")
			if self.time < 23.5:
				self.ignore(name,action)
			else:
				print("Marszpace: bye i'm going to sleep\n----Marszpace Left the Channel----")
			self.time = 13
		else:
			game = random.choice(self.addict)
			print(f"Marszpace: I don't have that game, do you want to play {game}?\n{name}: Sorry, I don't have that game.")
			self.ignore(name,action,game=game)

class Friend(Marszpace):
	"""A generic Marszpace's friend"""
	def __init__(self,name):
		"""Initialize friend's name"""
		super().__init__()
		self.name = name

	def playGames(self,game,action="play this game"):
		"""Main playing games function."""
		super()._playGames(game,self.name,action)

class Algy(Friend):
	"""AlgyCuber, one of the Marszpace's friend"""
	def __init__(self):
		"""Initialize Algy's name from Marszpace.Friend.__init__"""
		super().__init__("AlgyCuber")

	def astronautTest(self,action):
		"""Marszpace wants to be an astronaut, but he needs to pass Algy's astronaut test."""
		super().ignore(self.name,action)
		print(f"{self.name}: You have failed the astronaut test. Please try again.")

class Atom(Friend):
	"""AtomThum, one of the Marszpace's best friend"""
	def __init__(self):
		"""Initialize Atom's name from Marszpace.Friend.__init__"""
		super().__init__("AtomThum")

	def classicalMusic(self,name):
		"""AtomThum like classical music, but it makes him not online with Marszpace 24/7"""
		print(f"{self.name}: I like {name}.")
		a = random.randint(1,2)
		if a == 1:
			super().ignore(self.name,f"listening to {name}")
		elif a == 2:
			super().flexing()

if __name__ == '__main__':
	thum = Atom()
	algy = Algy()
	thum.classicalMusic("Tchaikovsky Violin Concerto")
	algy.astronautTest("composing a symphony")