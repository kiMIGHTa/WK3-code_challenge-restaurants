from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# define the database connection
DATABASE_URI = 'sqlite:///restaurants.db'# path to database
engine = create_engine(DATABASE_URI, echo=True)

# Base class for all the classes
Base = declarative_base()

class Customer(Base):
    __tablename__='customer'
    customer_id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    review = relationship('Review', back_populates='customers')

class Restaurant(Base):
    __tablename__ = 'restaurant'
    restaurant_id = Column(Integer, Sequence('restaurant_id_seq'), primary_key=True)
    name = Column(String)

    rest_review = relationship('Review', back_populates='restaurants')

class Review(Base):
    __tablename__ = 'review'
    review_id = Column(Integer, Sequence('review_id_seq'), primary_key=True)  
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
    star_rating = Column(Integer)  

    customers = relationship('Customer', back_populates='review')
    restaurants = relationship('Restaurant', back_populates='rest_review')
    

# creating all the tablesk
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# insert data
# --- customers
cust1 = Customer(first_name='Dennis',last_name='Kimaita')
cust2 = Customer(first_name='Michael',last_name='Jackson')
cust3 = Customer(first_name='Shay',last_name='Lia')
cust4 = Customer(first_name='Frank',last_name='Ocean')
cust5 = Customer(first_name='Earl',last_name='Sweatshirt')

session.add_all([cust1,cust2,cust3,cust4,cust5])
session.commit()


# --- restaurants
rest1 = Restaurant(name='Shawarma')
rest2 = Restaurant(name='Chinese')
rest3 = Restaurant(name='Hidden Gem')

session.add_all([rest1,rest2,rest3])
session.commit()


# --- reviews
rev1 = Review(customer_id=cust1.customer_id, restaurant_id=rest1.restaurant_id, star_rating=4)
rev2 = Review(customer_id=cust2.customer_id, restaurant_id=rest2.restaurant_id, star_rating=7)
rev3 = Review(customer_id=cust3.customer_id, restaurant_id=rest2.restaurant_id, star_rating=6)
rev4 = Review(customer_id=cust4.customer_id, restaurant_id=rest3.restaurant_id, star_rating=3)
rev5 = Review(customer_id=cust2.customer_id, restaurant_id=rest3.restaurant_id, star_rating=7)

session.add_all([rev1,rev2,rev3,rev4,rev5])
session.commit()



# # Saving data to database
# session.commit()

session.close()

