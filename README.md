This Vaultify allows users to generate, store, and retrieve passwords in an encrypted manner for various websites. The application is safeguarded by a Master Password, and the stored data is encrypted using Fernet (symmetrical encryption) to bolster security. For increased privacy, once mysteriously going into hiding, the password file is kept hidden from the file system on Windows after every small modification.

✅ Key Features:

Master Password Authentication: One master password to access all stored data.

OTP-Based Password Reset: Reset the master password via OTP sent to registered email.

Strong Password Generator: Allowing letters, numbers, and special characters.

Encrypted Storage: Has encryption on all passwords and other crucial data using cryptography’s library.

Hidden Password File: Hiding the main storage file (Password_generate.txt) for a bit of added discretion using Windows attrib command.

Password Lookup and Modification: Quickly search or update credentials for a specific website and e-mails.

🛠 Technologies Used: Python standard libraries (os, datetime, random, smtplib)

cryptography for encryption

smtplib for OTP email transmission (Gmail SMTP)
