from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.product import Product
from models.review import Review


#uses blueprints and calls db from the user.py
db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Your Tables have been created")

#Seed the tables with inserted data
@db_commands.cli.command("seed")
def seed_tables():
    users = [
       User(
           name = "Venita Kissell",
           email = "admin@gmail.com",
           password = bcrypt.generate_password_hash('abc123').decode("utf-8"),
           admin_user= True

       ), 
       User(
           name = "Mary Brown",
           email = "maryb@gmail.com",
           password = bcrypt.generate_password_hash("abc123").decode("utf-8"),
           display_name = "MaryB"
       ),
       User(
           name = "John Jones",
           email = "johnjones@gmail.com",
           password = bcrypt.generate_password_hash("abc123").decode("utf-8"),
           display_name = "JJJones"
       ), 
        User(
           name = "Suki Nakagawa",
           email = "nakagawas@gmail.com",
           password = bcrypt.generate_password_hash("abc123").decode("utf-8"),
           display_name = "Suki5"
       ),
       User(
           name = "Sarah Banan",
           email = "banwas@gmail.com",
           password = bcrypt.generate_password_hash("abc123").decode("utf-8"),
           display_name = "BanwaSS"
       ),  
    ]

    db.session.add_all(users)

    products = [
        Product(
            name = "Bike",
            description = "Mountain Bike",
            category = "Sport",
            user = users[0]
        ), 
        Product(
            title = "Freedom Lounge",
            description = "3 seater L shaped lounge, grey",
            category = "Furniture",
            user = users[0]            
        ), 
        Product(
            title = "Ikea Lamp",
            description = "Ikea desk lamp",
            category = "Electrical",
            user = users[0]
        ),
        Product(
            title = "MaxFactor Foundation",
            description = "Dewy and Smooth 24 hour foundation",
            category = "Beauty",
            user = users[0]
        ),
        Product(
            title = "Dr Beats HeadPhones",
            description = "Dr Beats over ear HeadPhones",
            category = "Technology",
            user = users[0]
        )
        ]
    db.session.add_all(reviews)

    reviews = [
        Review(
            date = date.today(),
            user = users[1],
            product = products[3],
            rating = "3",
            comment = "Didn't really like the texture on my skin"
        ),
        Review(
            date = date.today(),
            user = users[3],
            product = products[1],
            rating = "4",
            comment = "I really like this lamp, the quality is good for the price."
        ),
        Review(
            date = date.today(),
            user = users[4],
            product = products[1],
            rating = "5",
            comment = "I really like this mountain bike, quality is good, price is good, its comfortable and well constructed"
        )
    ]

    db.session.add_all(reviews)
    








    db.session.commit()
    print("Tables values have been seeded successfully.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Table has been dropped.")
    