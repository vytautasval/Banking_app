import sqlite3

con = sqlite3.connect("banking_database.db")
cur = con.cursor()

#cur.execute("CREATE TABLE customer_info(email VARCHAR(40) PRIMARY KEY, password VARCHAR(20))")
#cur.execute("DROP TABLE customer_info")

#cur.execute("INSERT INTO customer_info VALUES('test_1@gmail.com', 'testerissimo')")
#con.commit()

res = cur.execute("SELECT email FROM customer_info")
res.fetchall()
