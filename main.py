from Crypto.Cipher import AES
import hashlib
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64decode
from base64 import b64encode
import sqlite3
import bcrypt
import time

#register user
def user_register():
  print("\n ---------- User Registration ----------")
  
  while True:
    username = input("Enter a username: ")

    # Check if the username already exists in the database
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_username = cursor.fetchone()

    if existing_username:
        print("Username already taken. Please choose another username.")
        continue  # Continue the loop to allow the user to enter a new username
    else:
        password = input("Enter a password: ")
        # Hash the password using bcrypt and generate a salt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Store the username, hashed password, and salt in the database
        cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
        connection.commit()
        print("Registration successful!")
        break

#login a user
def login_user():
  max_attempts = 3
  attempts = 0

  print("\n -------- User Login ----------")
  while attempts < max_attempts:
      username = input("\nEnter your username: ")
      password = input("Enter your password: ")

      cursor.execute("SELECT salt, password FROM users WHERE username=?", (username,))
      user_data = cursor.fetchone()

      if user_data:
          stored_salt, stored_hashed_password = user_data

          """Debug prints
          print("Entered username:", username)
          print("Stored salt:", stored_salt)
          print("Stored hashed password:", stored_hashed_password)
          """
          # Hash the combined password and salt
          hashed_password_to_check = bcrypt.hashpw(password.encode('UTF-8'), stored_salt)
          """
          # Compare the hashed passwords
          # Debug print
          print("Computed hashed password to check:", hashed_password_to_check)
          """
          if hashed_password_to_check == stored_hashed_password:
              print("\nLogin successful!")
              break
          else:
              print("\nLogin failed. Incorrect username or password.")

      attempts += 1

  if attempts == max_attempts:
      print("Maximum login attempts reached. Account locked for 5 minutes.")
      time.sleep(300)
  return username

#salt the password in the password storage and encrypt it onto the database
def store_password(username):
  website = input("Enter the website: ")
  password = input("Enter your password: ")

  # Insert the password into the SQLite database along with the username
  cursor.execute("INSERT INTO passwords (username, website, password) VALUES (?, ?, ?)", (username, website, password))
  connection.commit()

  print("Password stored successfully.")

  print("------- Options --------")
  print("\n1. Store another password/Main Menu")
  print("2. Retrieve password")
  
  while True:
    choice = input("\nEnter your choice: ")

    if choice == "1":
        break  

    if choice == "2":
        retrieve_password()
        break
    
#retrieve password function
def retrieve_password(username):
  website = input("Enter the website name: ")

  passwordFound = False

  # Query the database for passwords associated with the logged-in user's username
  cursor.execute("SELECT website, password FROM passwords WHERE username=? AND website=?", (username, website))
  password_data = cursor.fetchone()

  if password_data:
      website, password = password_data
      print(f"Retrieved password for {website}: {password}")
      passwordFound = True

  if not passwordFound:
      print("Password not found for the website.")

def main():
  print("Welcome To Password Manager")

  while True:
      print("1. Register")
      print("2. Login")
      print("3. Exit")

      userChoice0 = int(input("\nEnter your choice: "))

      if userChoice0 == 1:
          user_register()
      elif userChoice0 == 2:
          login_user()

          while True:
              print("\n2------------ Password Menu ---------")
              print("1. Store password")
              print("2. Retrieve password")
              print("3. Back to main menu")

              userChoice1 = int(input("Enter your choice: "))

              if userChoice1 == 1:
                  store_password()
              elif userChoice1 == 2:
                  retrieve_password()
              elif userChoice1 == 3:
                  break

      elif userChoice0 == 3:
          break

  #close the connection
  cursor.close()
  connection.close()

if __name__ == "__main__":
  # Establish a connection to the SQLite database
  connection = sqlite3.connect("password_manager.db")
  cursor = connection.cursor()

  # Create a table for user registration with the "salt" column
  cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)")

  # Create a table for storing passwords
  cursor.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, user_id INTEGER, website TEXT, password TEXT)")

  connection.commit()
  main()
