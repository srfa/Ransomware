import socket,os               # Import socket module

while True:
	try:
		s = socket.socket()         # Create a socket object
		s.connect(('192.168.170.128', 50005))
		command = raw_input('Enter Command:')
		print 'Sending...'
		s.send(command)
		print "Success"
   
		print s.recv(1024)
		s.shutdown(socket.SHUT_WR)
		s.close 
	except:
		print 'Host is offline'
		break
