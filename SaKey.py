import hashlib, os, random, struct, time, sys, secrets, string
from Crypto.Cipher import AES

from getpass import getpass
from secure_delete import secure_delete

secure_delete.secure_random_seed_init()

sake = '1'

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):

    if not out_filename:
        out_filename = in_filename + '.db'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:

        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    return out_filename

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
    return out_filename

os.system('clear')

sys.stdout.write("\x1b]2;| SaKey AuthSystem |"'\x07')


print('Please insert your USB key\n')

while True:
    if os.path.isdir('/Volumes/SaKey'):
        print('USB Key found!\n')
        time.sleep(1)
        break
    else:
        continue

while True:
	if os.path.exists('/Volumes/SaKey/auth.key'):
		print('Loading auth file...\n')
		time.sleep(1)
		os.system('clear')
		break
	else:
		continue

password = getpass('Please enter your password: ')
os.system('clear')
password = password.encode('utf-8')

hash_object = hashlib.sha512(password)
hex_dig = hash_object.hexdigest()


key = hashlib.sha256(password).digest()


for x in range(3):
	print('Authenticating...')
	time.sleep(0.5)
	os.system('clear')


f = open("/Volumes/SaKey/auth.key", "r")
f = f.read()
if f == hex_dig:
    print('Authenticated')
    sys.stdout.write("\x1b]2;| SaKey |"'\x07')
    time.sleep(2)
    os.system('clear')

else:
    print('Incorrect password')
    os.system('exit')


while sake == '1':
    os.system('clear')

    print("""
███████╗ █████╗ ██╗  ██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██║ ██╔╝██╔════╝╚██╗ ██╔╝
███████╗███████║█████╔╝ █████╗   ╚████╔╝ 
╚════██║██╔══██║██╔═██╗ ██╔══╝    ╚██╔╝  
███████║██║  ██║██║  ██╗███████╗   ██║   
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   
        """)
    print('=========================================')
    print('          Welcome to your SaKey')
    print('=========================================')



    print('\n1 :: View your database')
    print('2 :: Add to your database')
    print('3 :: Clear your database')
    print('4 :: Generate a password')
    print('99 :: Exit')


    choice = input('\nChoice: ')
    if choice == '1':
        os.system('clear')
        try:
            decrypt_file(key, '/Volumes/SaKey/SaKey.db')
        except:
            print('ERROR: Could not decrypt database')
            continue
        try:
            contents = open("/Volumes/SaKey/SaKey", "r")
            contents = contents.read()

            print(contents)
        except:
            print('ERROR: Could not open database')
            continue


        secure_delete.secure_delete('/Volumes/SaKey/SaKey')

        gone = input('\nPress return to continue')
        os.system('clear')

    elif choice == '2':
        os.system('clear')

        addToDB = input('Line to add to database: ')

        decrypt_file(key, '/Volumes/SaKey/SaKey.db')

        file_out = open("/Volumes/SaKey/SaKey", "a")
        file_out.write('\n\n')
        file_out.write(addToDB)
        file_out.close()

        encrypt_file(key, '/Volumes/SaKey/SaKey')

        secure_delete.secure_delete('/Volumes/SaKey/SaKey')


        os.system('clear')
    elif choice == '3':
        os.system('clear')


        secure_delete.secure_delete('/Volumes/SaKey/SaKey.db')

        file_out = open("/Volumes/SaKey/SaKey", "a")
        file_out.write('Sake DB:')
        file_out.write('\n')
        file_out.write('\n')
        file_out.close()


        encrypt_file(key, '/Volumes/SaKey/SaKey')


        secure_delete.secure_delete('/Volumes/SaKey/SaKey')

        print('Database has been cleared')


        gone = input('\nPress return to continue')
        os.system('clear')
    elif choice == '4':
        os.system('clear')

        pass_label = input('Label for the password: ')
        pass_length = int(input('Length of the password: '))

        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(pass_length))



        decrypt_file(key, '/Volumes/SaKey/SaKey.db')

        file_out = open("/Volumes/SaKey/SaKey", "a")
        file_out.write('\n\n')
        file_out.write(f'{pass_label} : {password}')
        file_out.close()

        encrypt_file(key, '/Volumes/SaKey/SaKey')
        secure_delete.secure_delete('/Volumes/SaKey/SaKey')



        
        gone = input('\nPress return to continue')
        os.system('clear')
        
    elif choice == '99':
        os.system('clear')
        sake = 'sake'
        os.system('exit')
    else:
        print('Please enter a valid option')
        












