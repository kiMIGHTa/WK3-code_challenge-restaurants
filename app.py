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

    def reviews(self, session):
        # Return a collection of all the reviews left by the Customer
        return [review for review in session.query(Review).filter(Review.customer_id == self.customer_id)]

    def restaurants(self, session):
        # Return a collection of all the restaurants reviewed by the Customer
        return [review.restaurants.name for review in session.query(Review).filter(Review.customer_id == self.customer_id)]
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def favorite_restaurants(self):
        customer_reviews = self.reviews(session)

        favorite_restaurant = None
        highest_rating = -1

        for review in customer_reviews:
            if review.star_rating > highest_rating:
                highest_rating=review.star_rating
                favorite_restaurant = review.restaurant()
        return favorite_restaurant  

    def add_review(self, restaurant, rating, session):
        # Create a new review and associate it with the restaurant and customer
        new_review = Review(customer_id=self.customer_id, restaurant_id=restaurant.restaurant_id, star_rating=rating)

        # Add the new review to the session and commit it to the database
        session.add(new_review)
        session.commit()

        return new_review 

    def delete_reviews(self,restaurant):
        reviews_to_delete = session.query(Review).filter(
            Review.customer_id == self.customer_id,
            Review.restaurant_id == restaurant.restaurant_id
        ).all()

        for review in reviews_to_delete:
            session.delete(review)

        session.commit()    
     
class Restaurant(Base):
    __tablename__ = 'restaurant'
    restaurant_id = Column(Integer, Sequence('restaurant_id_seq'), primary_key=True)
    name = Column(String)
    price = Column(Integer)

    rest_review = relationship('Review', back_populates='restaurants')

    def reviews(self, session):
        # Return a collection of all the reviews for the Restaurant
        return [review for review in self.rest_review]

    def customers(self, session):
        # Return a collection of all the customers who reviewed the Restaurant
        return [review.customers.first_name for review in self.rest_review]

class Review(Base):
    __tablename__ = 'review'
    review_id = Column(Integer, Sequence('review_id_seq'), primary_key=True)  
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
    star_rating = Column(Integer)  

    customers = relationship('Customer', back_populates='review')
    restaurants = relationship('Restaurant', back_populates='rest_review')
    
    def customer(self):
        return self.customers
    
    def restaurant(self):
        return self.restaurants
    
    #
    #  def full_review(self):
    #     restaurant = self.restaurants 
    #     customer = self.customers 

    #     review_str = f"Review for {restaurant.name} by {customer.full_name()}: {self.star_rating} stars."
    #     return review_str

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

# session.add_all([cust1,cust2,cust3,cust4,cust5])
# session.commit()


# --- restaurants
rest1 = Restaurant(name='Shawarma')
rest2 = Restaurant(name='Chinese')
rest3 = Restaurant(name='Hidden Gem')

# session.add_all([rest1,rest2,rest3])
# session.commit()


# --- reviews
rev1 = Review(customer_id=cust1.customer_id, restaurant_id=rest1.restaurant_id, star_rating=4)
rev2 = Review(customer_id=cust2.customer_id, restaurant_id=rest2.restaurant_id, star_rating=7)
rev3 = Review(customer_id=cust3.customer_id, restaurant_id=rest2.restaurant_id, star_rating=6)
rev4 = Review(customer_id=cust4.customer_id, restaurant_id=rest3.restaurant_id, star_rating=3)
rev5 = Review(customer_id=cust2.customer_id, restaurant_id=rest3.restaurant_id, star_rating=7)

# session.add_all([rev1,rev2,rev3,rev4,rev5])
# session.commit()



# print(session.query(Customer).first().restaurants(session))
# reviews = cust1.reviews(session)
# print(reviews)

# new_review = cust5.add_review(rest3, 5, session)

# if new_review:
#     print(f"Review ID: {new_review.review_id}, Star Rating: {new_review.star_rating}")
#     print(f"Review added for Restaurant: {rest3.name}")
# else:
#     print("Failed to add a new review.")



# favorite = cust2.favorite_restaurants()

# if favorite:
#     print(f"Customer's Favorite Restaurant: {favorite.name}, Star Rating: {favorite.star_rating}")
# else:
#     print("The customer has not reviewed any restaurants.")
# # Saving data to database
# session.commit()

session.close()

formatted_review = rev1.full_review()
print(formatted_review)

