import socket,os               # Import socket module

s = socket.socket()         # Create a socket object

s.connect(('192.168.170.128', 50000))

print 'Sending...'

command = raw_input('Enter Command:')

s.send(command)

print "Done Sending command\n"
   
print s.recv(1024)
s.shutdown(socket.SHUT_WR)
s.close 
