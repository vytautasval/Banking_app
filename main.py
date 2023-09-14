import sqlite3
import re
import bcrypt
import datetime

class ProgramInit:
    def __init__(self):
        self.command_prompts_1 = {
            "Type '1' to log in.": "1",
            "Type '2' to register.": "2",
            "Type 'quit' to quit the program.": "quit",
        }
        self.command_prompts_2 = {
            "Type '1' to deposit.": "1",
            "Type '2' to withdraw.": "2",
            "Type '3' to view balance.": "3",
            "Type '4' to send a full account to your email address.": "4",
            "Type '5' to log out.": "5",
            "Type 'quit' to quit the program.": "quit",
        }

    def start_up(self) -> str:
        """Prints out available options for user to take at the first screen and checks if choice valid."""
        print("Welcome, this is an interactive banking app.")
        for prompt, comm in self.command_prompts_1.items():
            print(prompt)

        user_choice = input().casefold().strip()
        while user_choice not in self.command_prompts_1.values():
            print(
                "Incorrect command. Please try again. If you wish to quit, type in 'quit'."
            )
            user_choice = input()
        else:
            return user_choice

    def account_actions_start_up(self) -> str:
        """Prints out available options for user to take at the second screen and checks if choice valid."""
        for prompt, comm in self.command_prompts_2.items():
            print(prompt)

        user_choice = input().casefold().strip()
        while user_choice not in self.command_prompts_2.values():
            print(
                "Incorrect command. Please try again. If you wish to quit, type in 'quit'."
            )
            user_choice = input()
        else:
            return user_choice

    def main(self):
        """Initializes the first screen to login or register based on user choice."""
        banking_app = BankingApp()
        while True:
            user_choice = self.start_up()
            if user_choice == "1":
                login_result = banking_app.login()
                if login_result != False:
                    email = login_result
                    print("Logged in successfully.")
                    banking_app.customer_info(email)
                    self.account_actions_main(email)
                    # Logs in and goes to next screen.
                else:
                    print(
                        "Incorrect credentials. Please try again or register a new account."
                    )
                    continue
            elif user_choice == "2":
                login_result = banking_app.register()
                if login_result != None:
                    email = login_result
                    print(
                        "You have successfully created an account. You have now been logged in."
                    )
                    banking_app.customer_info(email)
                    self.account_actions_main(email)
                    # Logs in and goes to next screen.

            elif user_choice == "quit":
                raise (SystemExit("Program stopped."))

    def account_actions_main(self, email: str):
        """Initializes the seconds screen based on user choice."""
        banking_app = BankingApp()
        while True:
            user_choice = self.account_actions_start_up()
            if user_choice == "1":
                banking_app.deposit(email)
            elif user_choice == "2":
                banking_app.withdraw(email)

class DatabaseActions:
    def __init__(self):
        self.connection = sqlite3.connect("banking_database.db")
        self.cursor = self.connection.cursor()

    def create_customer_profile(self, email: str, hashed_password: str):
        """Adds a new email and password into the customer_info database. Password is hashed using bcrypt.
        Also adds email to customer_balance database."""
        self.cursor.execute(
            "INSERT INTO customer_info (email, password) VALUES(?, ?)",
            (email, hashed_password),
        )
        self.cursor.execute(
            "INSERT INTO customer_balance (email, deposit, withdrawal, balance) VALUES(?, 0, 0, 0)",
            (email,)
        )
        self.connection.commit()

    def get_email(self, email: str) -> str:
        """Enters customer_info database and returns selected email."""
        self.cursor.execute("SELECT email FROM customer_info WHERE email = ?", (email,))
        email_result_tuple = self.cursor.fetchone()
        (unpacked_email,) = email_result_tuple  # Tuple unpacking

        return unpacked_email

    def get_balance(self, email: str) -> int:
        """Enters customer_balance database and returns balance based on email."""
        self.cursor.execute("SELECT balance FROM customer_balance WHERE email = ?", (email,))
        balance_result_tuple = self.cursor.fetchone()
        (unpacked_balance,) = balance_result_tuple

        return unpacked_balance

    def balance_update(self, email: str, operation: float) -> float:
        """Takes user input and posts a new number for user balance to the database accordingly."""
        total_balance = self.get_balance(email)
        new_value = total_balance + operation

        self.cursor.execute(
            "UPDATE customer_balance SET balance = ? WHERE email = ?",
            (new_value, email,)
        )
        self.connection.commit()

    def get_deposit(self, email: str) -> int:
        """Enters customer_balance database and returns total deposit amount based on email."""
        self.cursor.execute("SELECT deposit FROM customer_balance WHERE email = ?", (email,))
        deposit_result_tuple = self.cursor.fetchone()
        (unpacked_deposit,) = deposit_result_tuple

        return unpacked_deposit

    def make_deposit(self, email: str, total_amount: float):
        """Updates the customer_balance database with a new total amount for deposits."""
        self.cursor.execute(
            "UPDATE customer_balance SET deposit = ? WHERE email = ?",
            (total_amount, email,)
        )
        self.connection.commit()

    def get_withdrawal(self, email: str) -> int:
        """Enters customer_balance database and returns total withdrawal amount based on email."""
        self.cursor.execute("SELECT withdrawal FROM customer_balance WHERE email = ?", (email,))
        withdrawal_result_tuple = self.cursor.fetchone()
        (unpacked_withdrawal,) = withdrawal_result_tuple

        return unpacked_withdrawal

    def make_withdrawal(self, email: str, total_amount: float):
        """Updates the customer_balance database with a new total amount for withdrawals."""
        self.cursor.execute(
            "UPDATE customer_balance SET withdrawal = ? WHERE email = ?",
            (total_amount, email,)
        )
        self.connection.commit()

    def post_transaction(self, email: str, operation: float):
        """Posts the transaction to the total transactions database."""
        current_time = datetime.datetime.now()
        self.cursor.execute("INSERT INTO transactions (email, operation, date) VALUES(?, ?, ?)",
                            (email, operation, current_time))
        self.connection.commit()

class BankingApp(DatabaseActions):
    """Using inheritence to make sure functions are able to utilize queries to SQLite"""

    def login(self) -> bool | str:
        """Asks for email and password and initializes validity checks through other functions."""
        email = input("Enter your email address: ")
        password = input("Enter your password: ")

        """If email in customer_info database, check if password valid"""
        if self.email_is_valid(email):
            if self.password_is_valid(email, password):
                return email
            else:
                return False
        else:
            return False

    def email_is_valid(self, input_email: str) -> bool:
        """Checking if email is in the database"""
        self.cursor.execute(
            "SELECT COUNT(*) FROM customer_info WHERE email = ?", (input_email,)
        )

        count = self.cursor.fetchone()[0]

        return count > 0

    def password_is_valid(self, input_email: str, input_password: str) -> bool | str:
        """Checking if password corresponds to email."""
        self.cursor.execute(
            "SELECT password FROM customer_info WHERE email = ?", (input_email,)
        )
        password_result_tuple = self.cursor.fetchone()
        (hashed_password,) = password_result_tuple  # Tuple unpacking

        encoded_password = input_password.encode()
        if bcrypt.checkpw(encoded_password, hashed_password):
            return True
        else:
            return False

    def register(self) -> str | None:
        """Prompts the user for their desired email and password and sends them through validity checks.
        If all checks passed, the new user information is stored in the database."""

        while True:
            desired_email = input("Please enter an email you would like to use: ")

            if desired_email.lower() == "quit":
                return
            elif not self.email_is_valid(desired_email):
                # Using previously defined function to check if email already in database.
                print(
                    "Email invalid. Choose another one, or type 'quit' to return. "
                )
            elif self.email_format_is_valid(desired_email) != None:
                print("Email is valid.")
                break


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
                return desired_email  # Exit the registration process
            else:
                print(
                    "Password invalid. Please choose another one, or type 'quit' to return: "
                )

    def email_format_is_valid(self, input_email: str) -> bool | str:
        """Checks if user inputted email is in a valid format using regex."""
        return re.search(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
            input_email,
        )

    def password_format_is_valid(self, input_password: str) -> bool | str:
        """Makes a simple check if password is valid using regex."""
        return re.search(".{8,20}$", input_password)

    def customer_info(self, email: str) -> print:
        """Prints out the balance, deposit and withdrawal amounts of an account."""
        e = self.get_email(email)
        email_list = e.split("@")
        name = email_list[0]

        balance = self.get_balance(email)
        deposit = self.get_deposit(email)
        withdrawal = self.get_withdrawal(email)

        print(f"Hello, {name}.\n"
                f"Your balance is: €{balance}\n"
                f"Split into deposits: €{deposit}, and withdrawals: €{withdrawal}")

    def number_is_valid(self, input_number: str) -> bool:
        """Checks if given number is a valid float."""
        try:
            float_number = float(input_number)
            return True
        except ValueError:
            return False

    def deposit(self, email: str):
        """Takes an email, checks if user input valid and calls make_deposit database function."""
        print("In order to make a deposit, please enter the number only.")
        total_deposits = self.get_deposit(email)
        while True:
            user_deposit = input("Deposit: ")
            if user_deposit == "quit":
                return
            elif self.number_is_valid(user_deposit):
                new_value = float(user_deposit) + total_deposits
                self.make_deposit(email, new_value)
                self.post_transaction(email, float(user_deposit))
                self.balance_update(email, float(user_deposit))
                print("Deposit made successfully.")
                break
            else:
                print("Invalid number provided.")

    def withdraw(self, email: str):
        """Takes an email, checks if user input is valid, if selected amount not bigger than available balance
        and calls make_withdrawal function if conditons met."""
        print("In order to make a withdrawal, please enter the number only.")
        total_withdrawal = self.get_withdrawal(email)
        available_balance = self.get_balance(email)
        while True:
            user_withdrawal = input("Withdrawal: ")
            if user_withdrawal == "quit":
                return
            elif self.number_is_valid(user_withdrawal):
                if float(user_withdrawal) > available_balance:
                    print(f"Not enough funds available. You currently have €{available_balance}.")
                    continue
                else:
                    new_value = total_withdrawal - float(user_withdrawal)
                    self.make_withdrawal(email, new_value)
                    self.post_transaction(email, -abs(float(user_withdrawal)))
                    self.balance_update(email, -abs(float(user_withdrawal)))
                    print("Withdrawal made successfully.")
                    break
            else:
                print("Invalid number provided.")



def sql_queries():
    con = sqlite3.connect("banking_database.db")
    cur = con.cursor()
    '''cur.execute("ALTER TABLE customer_actions RENAME TO customer_balance")
    cur.execute("DROP TABLE transactions")
    cur.execute(
        "CREATE TABLE customer_info(email VARCHAR(40) PRIMARY KEY, password VARCHAR(20))"
    )
    cur.execute(
        "CREATE TABLE customer_actions(email VARCHAR(40), deposit DECIMAL(18,2), withdrawal DECIMAL(18,2), balance DECIMAL(18,2), FOREIGN KEY (email) REFERENCES customer_info (email))"
    )
    cur.execute(
        "CREATE TABLE transactions(email VARCHAR(40), deposit DECIMAL(18,2), withdrawal DECIMAL(18,2), date DATE, FOREIGN KEY (email) REFERENCES customer_info (email))"
    )
    con.commit()'''
    '''cur.execute("UPDATE customer_balance SET deposit = 0, withdrawal = 0, balance = 0")'''

    '''cur.execute("DELETE FROM transactions")'''




if __name__ == "__main__":
    program_init = ProgramInit()
    program_init.main()


