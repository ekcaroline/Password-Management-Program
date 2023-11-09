# Password Manager
# Overview
This Python-based command-line Password Manager provides a secure and efficient solution for users to manage and store their passwords. Key features include user registration, login, password storage, and retrieval. The program utilizes SQLite for data storage and bcrypt for robust password hashing.

## Features
**User Registration:** Users can register by supplying a unique username and a password. Duplicate username prevention ensures uniqueness.

**User Login:** Registered users can securely log in using their username and password. Bcrypt is employed to compare the hashed password in the database with the entered password.

**Password Storage:** After login, users can store passwords for various websites, associating them with website names. Passwords are securely stored in an SQLite database.

**Password Retrieval:** Users can retrieve stored passwords by providing the website name. The program fetches the password from the database if it exists.

## Getting Started
- Clone or download the repository to your local machine.
- Ensure you have Python installed (compatible with Python 3).
- Install required packages using pip install pycryptodome and pip install bcrypt.
- Run the program by executing the main.py file in your terminal or IDE.
## Usage
Choose an option from the main menu:

- **Register (1):** Register a new user.
- **Login (2):** Log in as an existing user.
- **Exit (3):** Exit the program.
  
If registering, enter a unique username and password. The program securely stores this information in the database. For login, provide your username and password. After a successful login, access the Password Menu, allowing you to:

- **Store Password (1):** Save a new password for a website.

- **Retrieve Password (2):** Fetch a stored password for a website.

- **Update Password (3):** Update an existing password for a website.

- **Logout (4):** Log out and return to the main menu.

## Database
The program utilizes an SQLite database to store user information and passwords. The database schema includes two tables:

**users:** Stores user information (id, username, password, salt).
**passwords:** Stores stored passwords (id, user_id, website, password).

## Important Notes
The program employs bcrypt for secure password hashing.

## Authors
This Password Manager is created by Caroline Ek and Alexander Au. Feel free to reach out for any questions or suggestions.
