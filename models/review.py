from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")

class ReviewSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    product = fields.Nested("ProductSchema", exclude=["comments"])
    
    class Meta:
        fields = ("id", "message", "date", "user", "card")

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)