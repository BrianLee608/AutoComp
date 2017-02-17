from config import twitch_cfg
import socket

# chat_login is the scope needed for oauth


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# 	s.connect((HOST, PORT))
# 	s.send(("PASS " + PASS + "\r\n").encode())
# 	s.send(("NICK " + IDENT + "\r\n").encode())
# 	s.send(("JOIN #" + CHANNEL + "\r\n").encode())
# 	data = s.recv(1024)


# print('received', repr(data.decode()))

class ChatListener:
	def __init__(channel):
		self.channel = channel

	def listen():
		pass

def openSocket():
	s = socket.socket()
	s.connect((twitch_cfg['HOST'], twitch_cfg['PORT']))
	s.send(("PASS " + PASS + "\r\n").encode('utf-8'))
	s.send(("NICK " + IDENT + "\r\n").encode('utf-8'))
	s.send(("JOIN " + CHANNEL + "\r\n").encode('utf-8'))
	return s

def sendMessage(s, message):
	messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
	s.send((messageTemp + "\r\n").encode())
	print("Sent: " + messageTemp)

def joinRoom(s):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + str(s.recv(1024), 'utf-8')
		temp = readbuffer.split("\n")
		readbuffer = temp.pop()

		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	sendMessage(s, "Successfully joined chat")

def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True

def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user
def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message

s = openSocket()
joinRoom(s)
readbuffer = ""

while True:
		readbuffer = readbuffer + str(s.recv(1024), 'utf-8')
		temp = readbuffer.split("\n")
		readbuffer = temp.pop()

		for line in temp:
			print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG").encode('utf-8'))
				break
			user = getUser(line)
			message = getMessage(line)
			print(user + " typed :" + message)
			if "You Suck" in message:
				sendMessage(s, "No, you suck!")
				break
