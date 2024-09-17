from flask import Blueprint
from init import db, bcrypt
from models.user import User


#uses blueprints and calls db from the user.py
db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables have been created")

#create the list of user instances
@db_commands.cli.command("seed")
def seed_tables():
    users = [
       User(
           email = "admin@email.com",
           password = bcrypt.generate_password_hash('123456').decode("utf-8"),
           admin_user= True

       ), 
       User(
           name = "User 1",
           email = "user1@email.com",
           password = bcrypt.generate_password_hash("123456").decode("utf-8"),
           display_name = "user_display1"
       )
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Tables have been seeded successfully.")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Table has been dropped.")
    