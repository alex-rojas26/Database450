import sqlite3

con = sqlite3.connect("airline.db")
cur = con.cursor()

# read the airline.sql DDL file
with open("airline.sql", "r") as f:
    ddl = f.read()


# add another user
fname = input("Please enter your first name:")
mname = input("Please enter your middle name:")
lname = input("Please enter your last name:")
ssn = input("Please enter your ssn:")

# this time we'll use parameter binding
cur.execute("INSERT INTO passengers VALUES (?, ?, ?, ?)", (fname, mname, lname, ssn))

# commit the changes
con.commit()

# close the connection
con.close()
