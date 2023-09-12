import sqlite3
import re
'''con = sqlite3.connect("banking_database.db")
        cur = con.cursor()'''
class DatabaseActions:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect("banking_database.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        ...
        #cur.execute("CREATE TABLE customer_info(email VARCHAR(40) PRIMARY KEY, password VARCHAR(20))")
    def drop_table(self):
        ...
        #cur.execute("DROP TABLE customer_info")

#cur.execute("INSERT INTO customer_info VALUES('test_2@gmail.com', 'testerissimo2')")
#con.commit()

'''Using inheritence to make sure functions are able to utilize queries to SQLite'''
class BankingApp(DatabaseActions):

    def login(self):
        email = input("Enter your email address: ")
        password = input("Enter your pasword: ")

        '''If email in customer_info database, check if password valid'''
        if self.email_is_valid(email):
            return self.password_is_valid(email, password)



    def email_is_valid(self, input_email: str) -> bool:
        '''Checking if email is in the database'''
        cur.execute("SELECT email FROM customer_info")
        email_result = cur.fetchall()
        print(email_result)
        for registered_email_tuple in email_result:

            (registered_email,) = registered_email_tuple #Tuple unpacking here
            if registered_email != input_email:
                continue
            elif registered_email == input_email:
                return True

        print("Account not found. Please try again or register.")
        return False

    def password_is_valid(self, input_email: str, input_password: str):
        '''Checking if password corresponds to email.'''
        cur.execute(f"SELECT password FROM customer_info WHERE email = {input_email}")

def main():

    initial_response = input("Welcome, this is an interactive banking app.\n"
          "Type 1 to log in.\n"
          "Type 2 to register.\n"
          "Type quit to exit the program.\n").strip()
    banking_app = BankingApp()
    if initial_response == "1":
        while not banking_app.login():
            continue
        else:
            print("Logged in successfully.")
    if banking_app.login():
        ...
    else:
        ...
if __name__ == "__main__":
    main()



