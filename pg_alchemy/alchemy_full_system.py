# Import necessary modules and models
from alchemyBase import Base, Plane, Passenger, Flight, Onboard
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# To show the SQL that is running (optional)
import logging
#logging.basicConfig()
#logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# This is our "connection" to the database
with open("pw.txt", "r") as f:
    passwd = f.read().strip()

# Create "engine" using connection string.
engine = create_engine(f'postgresql://neondb_owner:{passwd}@ep-weathered-cherry-antwpx5a-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

Session = sessionmaker(bind=engine)
session = Session()

# Basic command line main menu
def main_menu():
    while True: 
        print("\n~~~ Airline Database System ~~~")
        print("1. Search for flights")
        print("2. View passenger itinerary")
        print("3. Purchase a ticket")
        print("4. Create a new plane")
        print("5. Create a new flight")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            search_flights()
        elif choice == '2':
            view_itinerary()  
        elif choice == '3':
            purchase_ticket()
        elif choice == '4':
            create_plane()
        elif choice == '5':
            create_flight()
        elif choice == '6':
            print("Exiting")
            break
        else:
            print("Invalid option. Try again.")

def search_flights():
    city = input("Enter the city to search flights for (departure or arrival): ").strip()
    flights = session.query(Flight).filter(
        (Flight.dep_loc == city) | (Flight.arr_loc == city)
    ).all()
    
    if flights:
        print(f"\nFlights to/from {city}:")
        for flight in flights:
            print(f"Flight No: {flight.flight_no}, From: {flight.dep_loc}, To: {flight.arr_loc}, Departs at: {flight.dep_time}, Arrives at: {flight.arr_time}")
    else:
        print(f"No flights found involving {city}.")

def view_itinerary():
    ssn_input = input("Enter the SSN of the passenger: ").strip()
    try:
        ssn = int(ssn_input)
    except ValueError:
        print("Invalid SSN. Please enter numbers only.")
        return
    
    passenger = session.query(Passenger).filter_by(ssn=ssn).first()
    if not passenger:
        print("Passenger not found.")
        return
    
    print(f"\nItinerary for {passenger.first} {passenger.middle} {passenger.last} (SSN: {passenger.ssn}):")
    
    # Get the onboard records for the passenger
    onboard_records = passenger.onboard_records
    if not onboard_records:
        print("No flights booked for this passenger.")
        return
    
    for onboard in onboard_records:
        flight = onboard.flight
        print(f"Flight No: {flight.flight_no}, From: {flight.dep_loc}, To: {flight.arr_loc}, Departs at: {flight.dep_time}, Arrives at: {flight.arr_time}, Seat: {onboard.seat}")
    
def purchase_ticket():
    ssn_input = input("Enter your SSN (numbers only): ").strip()
    try:
        ssn = int(ssn_input)
    except ValueError:
        print("Invalid SSN. Please enter numbers only.")
        return
    
    passenger = session.query(Passenger).filter_by(ssn=ssn).first()
    
    if not passenger:
        print("Passenger not found. Let's create a new passenger profile.")
        first = input("First Name: ").strip()
        middle = input("Middle Name: ").strip()
        last = input("Last Name: ").strip()
        passenger = Passenger(ssn=ssn, first=first, middle=middle, last=last)
        session.add(passenger)
        session.commit()
        print("Passenger profile created.")
    else:
        print(f"Welcome back, {passenger.first} {passenger.last}!")
    
    flight_no = input("Enter the flight number you wish to book: ").strip()
    flight = session.query(Flight).filter_by(flight_no=flight_no).first()
    if not flight:
        print("Flight not found.")
        return
    
    seat = input("Enter desired seat number: ").strip()
    
    # Check if the seat is already taken on this flight
    existing_seat = session.query(Onboard).filter_by(flight_no=flight_no, seat=seat).first()
    if existing_seat:
        print("Seat is already taken. Please choose a different seat.")
        return
    
    # Check if the flight is at capacity
    passenger_count = session.query(Onboard).filter_by(flight_no=flight_no).count()
    if passenger_count >= flight.plane.capacity:
        print("Flight is at full capacity. Cannot purchase ticket.")
        return
    
    # Add the onboard record
    onboard_record = Onboard(ssn=passenger.ssn, flight_no=flight.flight_no, seat=seat)
    session.add(onboard_record)
    session.commit()
    print(f"Ticket purchased! You are booked on flight {flight.flight_no} in seat {seat}.")

def create_plane():
    tailno = input("Enter the tail number of the plane: ").strip()
    existing_plane = session.query(Plane).filter_by(tailno=tailno).first()
    if existing_plane:
        print("A plane with this tail number already exists.")
        return
    
    make = input("Enter the make of the plane: ").strip()
    model = input("Enter the model of the plane: ").strip()
    
    capacity_input = input("Enter the capacity of the plane: ").strip()
    try:
        capacity = int(capacity_input)
    except ValueError:
        print("Invalid capacity. Please enter a number.")
        return
    
    mph_input = input("Enter the speed (mph) of the plane: ").strip()
    try:
        mph = int(mph_input)
    except ValueError:
        print("Invalid speed. Please enter a number.")
        return
    
    plane = Plane(tailno=tailno, make=make, model=model, capacity=capacity, mph=mph)
    session.add(plane)
    session.commit()
    print(f"Plane {tailno} added successfully.")

def create_flight():
    flight_no = input("Enter the flight number: ").strip()
    existing_flight = session.query(Flight).filter_by(flight_no=flight_no).first()
    if existing_flight:
        print("A flight with this flight number already exists.")
        return
    
    dep_loc = input("Enter the departure location: ").strip()
    dep_time = input("Enter the departure time (e.g., 10:00): ").strip()
    arr_loc = input("Enter the arrival location: ").strip()
    arr_time = input("Enter the arrival time (e.g., 14:00): ").strip()
    tail_no = input("Enter the tail number of the plane for this flight: ").strip()
    
    plane = session.query(Plane).filter_by(tailno=tail_no).first()
    if not plane:
        print("Plane not found. Please create the plane first.")
        return
    
    flight = Flight(flight_no=flight_no, dep_loc=dep_loc, dep_time=dep_time, arr_loc=arr_loc, arr_time=arr_time, tail_no=tail_no)
    session.add(flight)
    session.commit()
    print(f"Flight {flight_no} added successfully.")

# Run the main menu
if __name__ == "__main__":
    main_menu()
