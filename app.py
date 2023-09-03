from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# define the database connection
DATABASE_URI = 'sqlite:///restaurants.db'# path to database
engine = create_engine(DATABASE_URI, echo=True)

# Base class for all the classes
Base = declarative_base()

class Customers(Base):
    __tablename__='customer'
    customer_id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class Restaurant(Base):
    __tablename__ = 'restaurant'
    restaurant_id = Column(Integer, Sequence('restaurant_id_seq'), primary_key=True)
    name = Column(String)

    
    

# creating all the tablesk
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

session.close()

