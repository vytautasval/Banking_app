import sqlite3
import re
import bcrypt

"""con = sqlite3.connect("banking_database.db")
        cur = con.cursor()"""


class ProgramInit:
    def __init__(self):
        self.command_prompts = {
            "Type '1' to log in.": "1",
            "Type '2' to register.": "2",
            "Type 'quit' to quit the program.": "quit",
        }

    def start_up(self):
        print("Welcome, this is an interactive banking app.")
        for prompt, comm in self.command_prompts.items():
            print(prompt)

        user_choice = input().casefold().strip()
        while user_choice not in self.command_prompts.values():
            print(
                "Incorrect command. Please try again. If you wish to quit, type in 'quit'."
            )
            user_choice = input()
        else:
            return user_choice

    def main(self):
        banking_app = BankingApp()
        while True:
            user_choice = self.start_up()
            if user_choice == "1":
                if banking_app.login():
                    print("Logged in successfully.")
                    # Logs in and goes to next screen.
                else:
                    print("Incorrect credentials. Please try again or register a new account.")
                    continue
            elif user_choice == "2":
                banking_app.register()

            elif user_choice == "quit":
                raise (SystemExit("Program stopped."))


class DatabaseActions:
    def __init__(self):
        self.connection = sqlite3.connect("banking_database.db")
        self.cursor = self.connection.cursor()

    """def create_table(self):
        #cur.execute("CREATE TABLE customer_info(email VARCHAR(40) PRIMARY KEY, password VARCHAR(20))")"""

    def create_customer_profile(self, input_email: str, hashed_password: str):
        """Adds a new email and password into the customer_info database. Password is hashed using bcrypt"""
        self.cursor.execute(
            "INSERT INTO customer_info (email, password) VALUES(?, ?)",
            (input_email, hashed_password)
        )
        self.connection.commit()


# cur.execute("INSERT INTO customer_info VALUES('test_2@gmail.com', 'testerissimo2')")
# con.commit()


class BankingApp(DatabaseActions):
    """Using inheritence to make sure functions are able to utilize queries to SQLite"""

    def login(self) -> bool:
        """Asks for email and password and initializes validity checks through other functions."""
        email = input("Enter your email address: ")
        input_password = input("Enter your password: ")

        """If email in customer_info database, check if password valid"""
        if self.email_is_valid(email):
            return self.password_is_valid(email, input_password)
        else:
            return False

    def email_is_valid(self, input_email: str) -> bool:
        """Checking if email is in the database"""
        self.cursor.execute("SELECT COUNT(*) FROM customer_info WHERE email = ?", (input_email,))

        count = self.cursor.fetchone()[0]

        return count > 0

    def password_is_valid(self, input_email: str, input_password: str) -> bool | str:
        """Checking if password corresponds to email."""
        self.cursor.execute(
            "SELECT password FROM customer_info WHERE email = ?", (input_email,)
        )
        password_result_tuple = self.cursor.fetchone()
        (hashed_password,) = password_result_tuple #Tuple unpacking

        encoded_password = input_password.encode()
        if bcrypt.checkpw(encoded_password, hashed_password):
            return True
        else:
            return False

    def register(self):
        """Prompts the user for their desired email and password and sends them through validity checks.
        If all checks passed, the new user information is stored in the database."""

        while True:
            desired_email = input("Please enter an email you would like to use: ")

            if desired_email.lower() == "quit":
                return
            elif self.email_is_valid(desired_email):
                # Using previously defined function to check if email already in database.
                print("Email invalid. Please choose another one, or type 'quit' to return: ")
            elif self.email_format_is_valid(desired_email) != None:
                print("Email is valid.")
                break
            else:
                desired_email = input("Email invalid. Please choose another one, or type 'quit' to return: ")




        while True:
            desired_password = input(
                "Please enter a password you would like to use. It must be between 8 and 20 characters long: "
            )
            if desired_password.lower() == "quit":
                return
            elif self.password_format_is_valid(desired_password):
                print("Password is valid.")
                encoded_password = desired_password.encode()
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

                self.create_customer_profile(desired_email, hashed_password)
                print("You have successfully created an account. You may now log in.")
                return  # Exit the registration process
            else:
                print("Password invalid. Please choose another one, or type 'quit' to return: ")



    def email_format_is_valid(self, input_email: str) -> bool | str:
        """Checks if user inputted email is in a valid format using regex."""

        return re.search(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
            input_email
        )


    def password_format_is_valid(self, input_password: str) -> bool | str:
        return re.search(
            ".{8,20}$", input_password
        )

if __name__ == "__main__":
    program_init = ProgramInit()
    program_init.main()
