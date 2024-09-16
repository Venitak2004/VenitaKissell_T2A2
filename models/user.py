from init import db, ma

class User(db.Model):
    #Create the users table
    __tablename__ = "users"

    #table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin_user = db.Column(db.Boolean, default=False)
    display_name = db.Column(db.String)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "admin_user", "display_name")

#call a single user 
user_schema = UserSchema(exclude=["password"])

#call a list of users
user_schema = UserSchema(many=True, exclude=["password"])


