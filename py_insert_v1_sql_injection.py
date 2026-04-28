# in this file we will use the most basic (and potentially unsafe)
# way to insert data into a db

import sqlite3

# open the db we just created
con = sqlite3.connect("airline.db")
cur = con.cursor()

# let's add a new passenger! 
fname = input("Please enter your first name:")
mname = input("Please enter your middle name:")
lname = input("Please enter your last name:")
ssn = input("Please enter your ssn:")

cur.executescript("INSERT INTO passengers VALUES ('" + fname + "', '" + mname + "', '" + lname + "', " + ssn + ")")

# commit the changes
con.commit()

# close the connection
con.close()