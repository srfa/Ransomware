import socket, sys, os
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('192.168.170.128', 44389))
serv.listen(1)

while True:
	conn, addr = serv.accept()
	while True:
		print conn
		print addr
		from_client = ''
		data = conn.recv(4096)
		if not data: 
			break
		from_client += data
		
		print 'recieved'+from_client
		conn.send('thanks for sending me '+from_client)
		
		#if from_client == 'exit':
		#serv.close()
		#sys.exit()
		#if from_client == 'write file':
		#	f=open('scarlet', 'w')
		#	f.write('hannan')
#	print 'file written
