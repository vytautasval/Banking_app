import sqlite3
import re

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
                    break  # Logs in and goes to next screen.
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

    def create_customer_profile(self, input_email: str, input_password: str):
        """Adds a new email and password into the customer_info database"""

        self.cursor.execute(
            "INSERT INTO customer_info (email, password) VALUES(?, ?)",
            (input_email, input_password)
        )


# cur.execute("INSERT INTO customer_info VALUES('test_2@gmail.com', 'testerissimo2')")
# con.commit()


class BankingApp(DatabaseActions):
    """Using inheritence to make sure functions are able to utilize queries to SQLite"""

    def login(self) -> bool:
        """Asks for email and password and initializes validity checks through other functions."""
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        """If email in customer_info database, check if password valid"""
        if self.email_is_valid(email):
            return self.password_is_valid(email, password)
        else:
            print("Incorrect credentials. Please try again or register a new account.")

    def email_is_valid(self, input_email: str) -> bool:
        """Checking if email is in the database"""
        self.cursor.execute("SELECT email FROM customer_info")
        email_result = self.cursor.fetchall()

        for registered_email_tuple in email_result:
            (registered_email,) = registered_email_tuple  # Tuple unpacking here
            if registered_email != input_email:
                continue
            elif registered_email == input_email:
                return True

        return False

    def password_is_valid(self, input_email: str, input_password: str) -> bool:
        """Checking if password corresponds to email."""

        self.cursor.execute(
            "SELECT password FROM customer_info WHERE email = ?", (input_email,)
        )
        password_result_tuple = self.cursor.fetchone()

        (password_result,) = password_result_tuple  # Tuple unpacking again
        if password_result == input_password:
            return True
        else:
            return False

    def register(self):
        desired_email = input("Please enter an email you would like to use: ")
        while True:
            if not self.email_is_valid(desired_email):
                # Using previously defined function to check if email already in database.
                if self.email_format_is_valid(desired_email) != None:
                    print("Email is valid.")
                    break
                else:
                    desired_email = input("Email invalid. Please choose another one: ")
            desired_email = input("Email invalid. Please choose another one: ")

        desired_password = print(
                        "Please enter a password you would like to use. It must be between 8 and 20 characters long."
                    )


    def email_format_is_valid(self, input_email: str) -> bool | str:
        """Checks if user inputted email is in a valid format using regex."""

        return re.search(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
            input_email
        )

    def password_format_is_valid(self, input_password: str) -> bool | str:
        return re.search(
            ""
        )

if __name__ == "__main__":
    program_init = ProgramInit()
    program_init.main()
