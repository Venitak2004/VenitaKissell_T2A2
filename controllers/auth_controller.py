from flask import Blueprint, request
from models.user import User, user_schema, UserSchema
from init import bcrypt, db
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator

auth_blue = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blue.route("/register", methods=["POST"])
def register_user():

#get the user data from the body, check if user exists
    body_data = request.get_json()
#create the user model instance
    user = User(
        name = body_data.get("name"),
        email = body_data.get("email"),
        display_name = body_data.get("display_name")
    )
#hash protect the user password
    password = body_data.get("password")
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")
#add and commit to the database
    db.session.add(user)
    db.session.commit()
#return confirmation
    return user_schema.dump(user), 201

#search for existing user in the database and match it to the criteria
@auth_blue.route("/login", methods=["POST"])
def login_user():
    # Get the user data from the body of the request
    body_data = request.get_json()
    # Find the user in DB with the matching email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # If user exists in the database and password matches
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create JWT token for access
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=15))
        # Reply to user 
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    # Else
    else:
        # Respond back with an error message
        return {"error": "Invalid email or password, email or password is not in the database."}, 400

#Find the user in the database and update with user changes
# /auth/users/user_id
@auth_blue.route("/users", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    # get the user fields from the body of the request
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # get the user from the db
    # SELECT * FROM user WHERE id= get_jwt_identity()
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # if the user exists:
    if user:
        # then update the updated fields as required
        user.name = body_data.get("name") or user.name
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        # commit to the DB
        db.session.commit()
        # return a response
        return user_schema.dump(user)
    # else:
    else:
        # return an error response
        return {"error": "The User does not exist."},
    
# Authorising Admin to delete a user
@auth_blue.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@auth_as_admin_decorator
def delete_user(user_id):
    # find the user with the id from the db
    # SELECT * FROM users WHERE id==user_id;
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # if exists:
    if user:
        # delete the user
        db.session.delete(user)
        db.session.commit()
        # return an acknowledgement message
        return {"message": f"User with id {user_id} is deleted."}
    else:
        # return error message
        return {"message": f"User with id {user_id} could not be found."}, 404
