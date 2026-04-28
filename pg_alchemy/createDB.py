from sqlalchemy import create_engine

# import our models from the other file
from alchemyBase import Base

# to show the sql that is running
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

with open("pw.txt", "r") as f:
    passwd = f.read().strip()

# Create "engine" using connection string.
engine = create_engine(f'postgresql://neondb_owner:{passwd}@ep-weathered-cherry-antwpx5a-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
#engine = create_engine('sqlite:///airlineAlchemyExample.db')

# this will actually construct the tables from the objects
Base.metadata.create_all(engine)
