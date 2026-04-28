## This file shows the "executemany" function
## and takes data from an array 

import sqlite3

con = sqlite3.connect("airlinev2.db")
cur = con.cursor()

# read the airline.sql DDL file 
with open("airline.sql", "r") as f:
    ddl = f.read()

# execute the DDL 
cur.executescript(ddl)

# planes
plane_data = [
    ('101', 'Boeing', '757', 200, 500),
    ('102', 'Boeing', '757', 200, 500),
    ('103', 'Boeing', '757', 200, 500),
    ('104', 'Boeing', '757', 200, 500),
    ('105', 'Airbus', 'A320', 150, 450),
    ('106', 'Airbus', 'A320', 150, 450),
    ('107', 'Airbus', 'A320', 150, 450),
]
cur.executemany("INSERT INTO plane VALUES (?, ?, ?, ?, ?)", plane_data)

# pax
passenger_data = [
    ('John', 'Doe', 'Smith', 123456789),
    ('Jane', 'Doe', 'Smith', 987654321),
    ('Alice', 'Wonderland', 'Smith', 123123123),
    ('Bob', 'Apples', 'Smith', 456456456),
]
cur.executemany("INSERT INTO passengers VALUES (?, ?, ?, ?)", passenger_data)

# flights
flight_data = [
    ('101', 'JFK', '10:00', 'LAX', '14:00', 101),
    ('102', 'MIA', '11:00', 'LAX', '15:00', 102),
    ('103', 'TPA', '12:00', 'LAX', '16:00', 103),
]
cur.executemany("INSERT INTO flight VALUES (?, ?, ?, ?, ?, ?)", flight_data)

# onboard
onboard_data = [
    (123456789, '101', '1A'),
    (987654321, '101', '1B'),
    (123123123, '102', '2A'),
    (456456456, '103', '3A'),
]
cur.executemany("INSERT INTO onboard VALUES (?, ?, ?)", onboard_data)

# commit the changes
con.commit()

con.close()
