import sqlite3
import re

con = sqlite3.connect("banking_database.db")
cur = con.cursor()

#cur.execute("CREATE TABLE customer_info(email VARCHAR(40) PRIMARY KEY, password VARCHAR(20))")
#cur.execute("DROP TABLE customer_info")

#cur.execute("INSERT INTO customer_info VALUES('test_1@gmail.com', 'testerissimo')")
#con.commit()

class BankingApp:

    def login(self):
        email = input("Enter your email address: ")
        password = input("Enter your pasword: ")

        '''If email in login database, check if password valid'''
        return self.login_is_valid(email, password)


    def login_is_valid(self, input_email, input_password):
        '''Checking if email is in the database'''
        cur.execute("SELECT email FROM customer_info")
        email_result = cur.fetchall()
        for registered_email_tuple in email_result:
            #Tuple unpacking here
            (registered_email,) = registered_email_tuple

            if registered_email != input_email:
                continue
            elif registered_email == input_email:
                print("well done")
        return print("Account not found. Please register.")

def main():
    print("Welcome, this is an interactive banking app. Please login to begin.")
    banking_app = BankingApp()
    banking_app.login()

main()



