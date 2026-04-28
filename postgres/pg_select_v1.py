import psycopg

# read password from a file (pw.txt)
with open("pw.txt", "r") as f:
    password = f.read().strip()

# connect to the database
conn = psycopg.connect(f"postgresql://neondb_owner:{password}@ep-frosty-field-amqo58jo.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require")


cur = conn.cursor()

# query all planes from the plane table
cur.execute("SELECT * FROM plane")
planes = cur.fetchall()  # fetch all rows as a list of tuples
print("Planes:", planes)

# query all passengers from the passengers table
cur.execute("SELECT * FROM passengers")
passengers = cur.fetchall()
print("Passengers:", passengers)

# query all flights from the flight table
cur.execute("SELECT * FROM flight")
flights = cur.fetchall()
print("Flights:", flights)

# query all onboard data from the onboard table
cur.execute("SELECT * FROM onboard")
onboard = cur.fetchall()
print("Onboard:", onboard)

# query a specific flight by flight_no and create a dictionary from it
flight_no = '101'
cur.execute("SELECT * FROM flight WHERE flight_no = %s", (flight_no,))
specific_flight = cur.fetchone()  # fetch one row
if specific_flight:
    flight_dict = {
        "flight_no": specific_flight[0],
        "dep_loc": specific_flight[1],
        "dep_time": specific_flight[2],
        "arr_loc": specific_flight[3],
        "arr_time": specific_flight[4],
        "tail_no": specific_flight[5]
    }
    print("Specific Flight:", flight_dict)

# also look into row_factory to automatically convert rows to dictionaries
# https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory

# close the connection
conn.close()
