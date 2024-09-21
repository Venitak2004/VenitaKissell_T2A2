from flask import Blueprint, request
from models.user import User, user_schema
from init import bcrypt, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():

#get the user data from the body, check if user exists
    body_data = request.get_json()
#create the user model instance
    user = User(
        name = body_data.get("name"),
        email = body_data.get("email"),
        display_name = body_data.get("display_name")
    )
#has protect the user password
    password = body_data.get("password")
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")
#add and commit to the database
    db.session.add(user)
    db.session.commit()
#return confirmation
    return user_schema.dump(user), 201





