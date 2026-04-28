# Let's look at some code to access a database.

# first, import the sqlite3 module which gives us functions to use SQL
# sqlite3 should be built-in - should not need to pip install it
import sqlite3

# create a connection to the database (again, a SQLite DB is just a file)
# you can also do this connection in a "with" statement to auto-close when done
conn = sqlite3.connect("airline.db")

# if the database doesn't exist, a new db will be created

# now let's read in the DDL file
with open("airline.sql", "r") as f:
    ddl = f.read()

# execute the DDL on the db
# executescript can run multiple SQL statements at once
conn.executescript(ddl)

# let's look at the database in sqlitestudio right now
# PAUSE
########

# The tables are there, great!

# close the connection
conn.close()

# In other files we will insert data

