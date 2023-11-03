from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import hashlib
import sqlite3
import bcrypt
import time

#test

# Register a user
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

# User login
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

# Enter and store password onto database
def store_password(username):
  website = input("Enter the website: ")
  password = get_password()

  # Insert the password into the SQLite database along with the user_id
  user_id = get_user_id(username)
  if user_id is not None:
      cursor.execute("INSERT INTO passwords (user_id, website, password) VALUES (?, ?, ?)", (user_id, website, password))
      connection.commit()
      print("Password stored successfully.")
  else:
      print(f"User '{username}' not found. Password not stored.")

# Function to get the user ID based on the username
def get_user_id(username):
  cursor.execute("SELECT id FROM users WHERE username=?", (username,))
  user_id = cursor.fetchone()
  if user_id:
      return user_id[0]
  else:
      return None
    
# Retrieve the password from database using username, website
def retrieve_password(username):
  website = input("Enter the website name: ")

  passwordFound = False

  # Get the user_id based on the username
  user_id = get_user_id(username)

  if user_id is not None:
      # Query the database for passwords associated with the user_id and website
      cursor.execute("SELECT website, password FROM passwords WHERE user_id=? AND website=?", (user_id, website))
      password_data = cursor.fetchone()

      if password_data:
          website, password = password_data
          print(f"Retrieved password for {website}: {password}")
          passwordFound = True

  if not passwordFound:
      print("Password not found for the website.")
      
# Gets the password
# Takes no arguments and returns a password string
def get_password():
    password = input("Enter your password: ")
    
    while validate_password(password) == False:
        password = input("Enter your password: ")
    
    return password

# Validates if the password meets requirements
# Takes in the password as a string and returns T/F if its valid
def validate_password(password):
    lowerAlphas = "q w e r t y u i o p a s d f g h j k l z x c v b n m".split()
    upperAlphas = "Q W E R T Y U I O P A S D F G H J K L Z X C V B N M".split()
    nums = "1 2 3 4 5 6 7 8 9 0".split()
    specials = "! @ # $ % ^ & * ( ) _ + - = < > , . / ? ; :".split()
    
    validLower = False
    validUpper = False
    validNums = False
    validSpecials = False
    
    missingRequirements = []

    for char in password:
        if char in lowerAlphas:
            validLower = True
        if char in upperAlphas:
            validUpper = True
        if char in nums:
            validNums = True
        if char in specials:
            validSpecials = True
            
    if validLower and validUpper and validNums and validSpecials:
        return True
    else:
        if validLower is False:
            missingRequirements.append(1)
        if validUpper is False:
            missingRequirements.append(2)
        if validNums is False:
            missingRequirements.append(3)
        if validSpecials is False:
            missingRequirements.append(4)
        print("\nInvalid password")
        requirements_message(missingRequirements)
        return False
        
# Takes in the missing requirements as an array of characters that denote the missing requirements
# Prints the correct error message and does not return anything
def requirements_message(missingRequirements): 
    errorOutput    = "Password must contain"

    #appending requirements to the output
    if len(missingRequirements) > 1:
        for i in range(len(missingRequirements) - 1):
            errorOutput = construct_requirements_message(missingRequirements[i], errorOutput)
        errorOutput = errorOutput + " and"
    errorOutput = construct_requirements_message(missingRequirements[len(missingRequirements) - 1], errorOutput)
    print(errorOutput + '\n')
    
def construct_requirements_message(missingRequirement, errorOutput):
    invalidLower   = ", a lower case letter"
    invalidUpper   = ", an upper case letter"
    invalidNum     = ", a number"
    invalidSpecial = ", a special character"
    
    if missingRequirement == 1:
        message = errorOutput + invalidLower
    elif missingRequirement == 2:
        message = errorOutput + invalidUpper
    elif missingRequirement == 3:
        message = errorOutput + invalidNum
    elif missingRequirement == 4:
        message = errorOutput + invalidSpecial
    else:
        message = errorOutput + "error"
    
    return message

    
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
          username = login_user()

          while True:
              print("\n2------------ Password Menu ---------")
              print("1. Store password")
              print("2. Retrieve password")
              print("3. Back to main menu")

              userChoice1 = int(input("Enter your choice: "))

              if userChoice1 == 1:
                  store_password(username)
              elif userChoice1 == 2:
                  retrieve_password(username)
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
