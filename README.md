# Password-Manager

This Python program is a simple command-line-based Password Manager that allows users to register, login, store, and retrieve passwords for various websites. It uses SQLite for data storage and bcrypt for password hashing.

## Features
User Registration: Users can register by providing a unique username and a password. The program checks for duplicate usernames to ensure uniqueness.

User Login: Registered users can log in with their username and password. The program securely compares the hashed password stored in the database with the entered password using bcrypt.

Password Storage: After login, users can store passwords for websites along with the website name. The passwords are securely stored in an SQLite database.

Password Retrieval: Users can retrieve stored passwords by providing the website name. The program fetches the password from the database if it exists.

## Getting Started
Clone or download the repository to your local machine.
Make sure you have Python installed (the code is compatible with Python 3).
Install the required packages using pip install pycryptodome and pip install bcrypt.
Run the program by executing the password_manager.py file in your terminal or IDE.

## Usage
Choose an option from the main menu:

Register (1): Register a new user.
Login (2): Log in as an existing user.
Exit (3): Exit the program.

If you choose to register, enter a unique username and password. The program will store your information securely in the database.
If you choose to log in, enter your username and password. After successful login, you can access the Password Menu, which allows you to:

Store password (1): Store a new password for a website.
Retrieve password (2): Retrieve a stored password for a website.
Back to main menu (3): Go back to the main menu.
Database
The program uses an SQLite database to store user information and passwords. The database schema includes two tables:

users: Stores user information (id, username, password, salt).
passwords: Stores stored passwords (id, user_id, website, password).
Important Notes
The program employs bcrypt for secure password hashing.
The AES encryption and decryption code is provided but commented out. You can uncomment it and use it to encrypt and decrypt passwords.
Author
This program is created by [Your Name]. Feel free to contact me at [Your Email] if you have any questions or suggestions.

License
This project is licensed under the [License Name] - see the LICENSE file for details.

Enjoy using the Password Manager!
