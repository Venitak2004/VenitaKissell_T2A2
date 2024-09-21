from init import db, ma
from marshmallow import fields

class Category (db.Model):
    #create the Category table
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable= False)


class CategorySchema(ma.Schema):

    products = fields.Nested('ProductSchema', only=["id", "name", "description"])
    class Meta:
        fields = ("id", "name")

#call a single category
category_schema = CategorySchema()
#call a list of cards
category_schemas = CategorySchema(many=True)