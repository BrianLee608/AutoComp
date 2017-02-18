from config import twitch_cfg
import socket
from twitch import Twitch

def read_join_greeting(s):
	readbuffer = ""
	loading = True
	while loading:
		readbuffer += str(s.recv(1024), 'utf-8')
		temp = readbuffer.split("\n")
		readbuffer = temp.pop()

		for line in temp:
			print(line)
			# twitch irc's last msg on initial login is the one specified below
			loading = "End of /NAMES list" in line

def send_msg(s, message, channel):
	msg = "PRIVMSG #" + channel + " :" + message
	s.send((msg + "\r\n").encode())

# example socket respose
# :user123!user123@user123.tmi.twitch.tv PRIVMSG #somechannel_tv :nice shot!
def get_user(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def get_msg(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message

class ChatListener:
	def __init__(self, channel):
		self.channel = channel

	def execute(self):
		"""
		This function will eventually call a chron to go on twitch and
		create/dl clips when the 'time is right'
		"""

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((twitch_cfg['HOST'], twitch_cfg['PORT']))
			s.send(("PASS " + twitch_cfg['PASS'] + "\r\n").encode())
			s.send(("NICK " + twitch_cfg['IDENT'] + "\r\n").encode())
			s.send(("JOIN " + '#adren_tv' + "\r\n").encode())

			read_join_greeting(s)
			readbuffer = ""

			t = Twitch()
			num_viewers = t.get_viewers('adren_tv')

			while True:
				readbuffer += str(s.recv(1024), 'utf-8')
				temp = readbuffer.split("\n")
				readbuffer = temp.pop()

				for line in temp:
					print(line)
					if "PING" in line:
						s.send(line.replace("PING", "PONG").encode('utf-8'))
						break

# todo: look into greasemonkey augmented browsing library
# tampermonkey for chrome
c = ChatListener('#adren_tv')
c.execute()
