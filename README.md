# Banking_app
A simple console based banking application made to learn about databases.

In it the user is able to register, log in, withdraw, deposit, check their balance and download a full account of their withdrawals and deposits.

The key aspect of this exercise is integrating databases into actual code and making them usable. In this case I used sqlite3 to create and modify databases.
There are three databases: 
1. customer_info, which includes an email address and a hashed password using bcrypt;
2. customer_balance, which saves every users total withdrawals, deposits and remaining balance.
   It's purpose is to provide a simplified bank statement for the aforementioned information.
3. transactions, which displays the full list of all transactions conducted through the 'bank'. It saves an email, an operation amount (either a withdrawal or deposit),
   and a date of when the action was made.
