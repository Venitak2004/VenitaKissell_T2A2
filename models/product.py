from init import db, ma
from marshmallow import fields

class Product (db.Model):
    #create the Product table
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable= False)
    description = db.Column(db.String)
    
    #define the foreign key for the Products table, foreign key User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #attached the relationships for the foreign key tables connection
    user = db.relationship('User', back_populates='products')

    #define the foreign key for the Products table, foreign key Category
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    #attached the relationships for the foreign key tables connection
    category = db.relationship('Category', back_populates='products')


class ProductSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    class Meta:
        fields = ("id", "name", "description","user")

#call a single card
product_schema = ProductSchema()
#call a list of cards
products_schema = ProductSchema(many=True)