
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Customer
from app import Restaurant
from app import Review
from app import session



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
rest1 = Restaurant(name='Shawarma',price=2000)
rest2 = Restaurant(name='Chinese',price=5620)
rest3 = Restaurant(name='Hidden Gem', price=2344)

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
print(rev1.full_review())
print(rest2.all_reviews())

session.close()

# formatted_review = rev1.full_review()
# print(formatted_review)

