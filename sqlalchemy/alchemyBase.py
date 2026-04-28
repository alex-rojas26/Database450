"""Provides base classes for airline db"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Create a base class for declarative class definitions
# this keeps track of all the subclasses created from it. So it basically represents our schema.
Base = declarative_base()


class Plane(Base):
    """this represents a single table in the database. Notice - no SQL! Wow!"""
    __tablename__ = 'plane'
    tailno = Column(String, primary_key=True)
    make = Column(String)
    model = Column(String)
    capacity = Column(Integer)
    mph = Column(Integer)

    # This is an odd thing. Relationships have nothing to do with DDL,
    # but rather are about relationships between classes (in the application)
    # The relationships can be defined "both ways"
    # it's kind of like a "reverse foreign key." 
    # this allows me to easily filter for all of a plane's flights, for example
    # by accessing the "flights" attribute of this class
    flights = relationship("Flight", back_populates="plane")

class Passenger(Base):
    """Passengers table"""
    __tablename__ = 'passengers'
    ssn = Column(Integer, primary_key=True)
    first = Column(String)
    middle = Column(String)
    last = Column(String)

    # Again, same "reverse" foreign key relationship
    onboard_records = relationship("Onboard", back_populates="passenger")


class Flight(Base):
    """Flights"""
    __tablename__ = 'flight'
    flight_no = Column(String, primary_key=True)
    dep_loc = Column(String)
    dep_time = Column(String)  # Using String for simplicity
    arr_loc = Column(String)
    arr_time = Column(String)

    # now this defines a column that is a foreign key. 
    # in this case, the tail_number of the plane for the flight
    tail_no = Column(String, ForeignKey('plane.tailno'))

    # Normal relationship, the same "info" as the tail_no foreign key
    # but it's defining the relationship between the classes
    plane = relationship("Plane", back_populates="flights")

    # same "reverse" foreign key for the onboard table
    onboard_records = relationship("Onboard", back_populates="flight")


class Onboard(Base):
    """Tickets/onboard"""
    __tablename__ = 'onboard'
    id = Column(Integer, primary_key=True)
    ssn = Column(Integer, ForeignKey('passengers.ssn'))
    flight_no = Column(String, ForeignKey('flight.flight_no'))
    seat = Column(String)

    # Relationships
    passenger = relationship("Passenger", back_populates="onboard_records")
    flight = relationship("Flight", back_populates="onboard_records")