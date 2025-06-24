import random
from datetime import datetime
from cryptography.fernet import Fernet
import os
import smtplib


def MY_First_Project():
    def write_key():
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    if not os.path.exists('key.key'):
        write_key()

    def load_key():
        with open('key.key', 'rb') as file_k:
            return file_k.read()

    key = load_key()
    fer = Fernet(key)

    def end_ask():
        ask = input('Do You Want TO Exist (Y/N):')
        if ask.upper() == 'Y':
            return "Exited"
        else:
            MY_First_Project()

    def read_all_decrypted_lines():
        decrypted_lines = []
        if os.path.exists('Password_generate.txt'):
            with open('Password_generate.txt', 'r') as file:
                for line in file:
                    decrypted_lines.append(fer.decrypt(line.encode()).decode())
          
        return decrypted_lines

    def get_user_input(mode):
        if mode == 1:
            while True:
                try:
                    length = int(input('Enter password length (e.g., 12): '))
                    if length <= 0:
                        print("Length must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
        website = input('Enter the website name (e.g., github.com): ').replace(' ', '')
        email = input('Enter the email used for login: ').replace(' ', '')
        if mode == 1:
            return [length, website, email]
        elif mode == 2:
            return [website, email]

    def check_existing_data(website, email):
        combined_key = f"{website} login from {email}"
        decrypted_data = read_all_decrypted_lines()
        for line in decrypted_data:
            if combined_key in line:
                return [combined_key, decrypted_data, line.split()]
        return [combined_key, decrypted_data, None]

    def only_pass(length):
        list_list = []
        if input('Include alphabets in password? (yes/no): ').strip().lower() == 'yes':
            list_list.append(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        if input('Include numbers in password? (yes/no): ').strip().lower() == 'yes':
            list_list.append(list('1234567890'))
        if input('Include special characters? (yes/no): ').strip().lower() == 'yes':
            list_list.append(list('!@#$%^&*'))

        if not list_list:
            print("No character types selected. Defaulting to alphabets.")
            list_list.append(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))

        password = ''
        for _ in range(length):
            group = random.choice(list_list)
            password += random.choice(group)
        return password

    def change_password(website, email, length):
        ask = input(f'Do you want to create a new password for {website} login from {email}? (yes/no): ').strip().lower()
        if ask == 'yes':
            new_password = only_pass(length)
            print(f'Your new password is: {new_password}')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('Password_generate.txt', 'a') as f:
                f.write(fer.encrypt(
                    f'Password for {website} login from {email} is {new_password} generated on {now}'.encode()
                ).decode() + '\n')
            os.system('attrib +h Password_generate.txt')

    def create_password(mode):
        print('Let\'s generate a new password!')
        user_data = get_user_input(mode)
        length, website, email = user_data
        existing = check_existing_data(website, email)

        if existing[0] not in existing[1]:
            password = only_pass(length)
            print(f'Your new password is: {password}')
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('Password_generate.txt', 'a') as f:
                f.write(fer.encrypt(
                    f'Password for {website} login from {email} is {password} generated on {now}'.encode()
                ).decode() + '\n')
            os.system('attrib +h Password_generate.txt')
        else:
            print(f'You already have a password for {website} with email {email}. It is -----> {existing[2][7]}')
            change_password(website, email, length)

    def main(master_input):
        master_check = 'Master Password Is'
        master_found = None
        for line in read_all_decrypted_lines():
            if master_check in line:
                master_found = line.split()
                break
        if master_found and master_input == master_found[3]:
            choice = input('Choose an option - Generate(1), Search(2), Store(3): ')
            if choice == '1':
                create_password(1)
            elif choice == '2':
                data = get_user_input(2)
                result = check_existing_data(data[0], data[1])[2]
                if result:
                    print(f'Your password for {data[0]} with email {data[1]} is -----> {result[7]}')
                else:
                    print('No password found for the provided details.')
            elif choice == '3':
                password = input('Enter the password: ')
                website = input('Enter the website: ')
                email = input('Enter the email: ')
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('Password_generate.txt', 'a') as f:
                    f.write(fer.encrypt(
                        f'Password for {website} login from {email} is {password} generated on {now}'.encode()
                    ).decode() + '\n')
                os.system('attrib +h Password_generate.txt')
                print('Your password has been safely stored.')
            else:
                print("Invalid choice.")
        else:
            print('Wrong Master Password!')
            exist_ask = input("Do You Want To Reset Your password (Y/N)  :")
            if exist_ask.upper() == 'Y':
                otp_temp = otp(master_found[7])
                otp_check = input(f'Enter otp Send to {master_found[7]}:')
                if otp_check == otp_temp:
                    new_master_password = input('New master password: ')
                    with open('Password_generate.txt', 'r') as f:
                        lines = f.readlines()
            
                    # Filter out the unwanted master password line
                    filtered_lines = []
                    for line in lines:
                        try:
                            decrypted_con = fer.decrypt(line.encode()).decode()
                            if "Master Password Is" not in decrypted_con:  # keep all lines except this
                                filtered_lines.append(line)
                        except:
                            pass  # skip any line that fails decryption

                    # Rewrite the file with only the filtered lines
                    with open('Password_generate.txt', 'w') as f:
                        f.writelines(filtered_lines)
                    
                    with open('Password_generate.txt', 'a') as f:
                        f.write(fer.encrypt(f'Master Password Is {new_master_password} for the mail {master_found[7]}'.encode()).decode() + '\n')
                    print("Your Password Has Been updated")
                    os.system('attrib +h Password_generate.txt')
                    
                else:
                    print('wrong otp')
                    end_ask()
                                        
    def otp(re_mail):
        otp = str(random.randint(100000, 999999))
       

        sender_email = "darshitvarshney1928@gmail.com"
        sender_password = "ntbq nolh ryqv xnyk"   
        receiver_email = re_mail

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, f"Subject: Your OTP\n\nYour OTP is {otp}")
        server.quit()
        return otp

    def project():
        print('Welcome to My Password Manager')
        if os.path.exists('Password_generate.txt'):
            master = input('Enter Master Password: ')
            main(master)
        else:
            re_mail = input('Enter Your email---')
            otp_temp = otp(re_mail)
            otp_check = input(f'Enter otp Send to {re_mail}:')
            if otp_check == otp_temp:
                master = input('Create a Master Password: ')

                with open('Password_generate.txt', 'a') as f:
                    f.write(fer.encrypt(f'Master Password Is {master} for the mail {re_mail}'.encode()).decode() + '\n')
                os.system('attrib +h Password_generate.txt')
                main(master)


    project()

MY_First_Project()
