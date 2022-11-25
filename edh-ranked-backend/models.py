from datetime import datetime
from app import db, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)
    name = db.Column(db.String(36), index=True, unique=True)
    play_stars = db.Column(db.Float, index=True, unique=False, default=0)
    enemy_stars = db.Column(db.Float, index=True, unique=False, default=0)
    play_review_num = db.Column(db.Integer, index=True, unique=False, default=0)
    enemy_review_num = db.Column(db.Integer, index=True, unique=False, default=0)
    play_star_total = db.Column(db.Integer, index=True, unique=False,default=0)
    enemy_star_total = db.Column(db.Integer, index=True, unique=False, default=0)
    

class PlayRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(280), index=True, unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_username = db.Column(db.String(64), index=True, unique=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    author = db.relationship("User",backref="playRating")
    listing = db.relationship("Listing", backref="playRating")
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)

class EnemyRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(280), index=True, unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_username = db.Column(db.String(64), index=True, unique=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    author = db.relationship("User", backref="enemyRating")
    listing = db.relationship("Listing", backref="enemyRating")
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(280), index=True, unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_username = db.Column(db.String(64), index=True, unique=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    author = db.relationship("User", backref="comment")
    listing = db.relationship("Listing", backref="comment")
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)
    name = db.Column(db.String(36), index=True, unique=True)
    play_review_num = db.Column(db.Integer, index=True, unique=False)
    play_star_total = db.Column(db.Integer, index=True, unique=False)
class CardRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    author = db.relationship("User",backref="cardRating")
    card = db.relationship("Cards", backref="cardRating")
class CardListMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    listing_id = db.Column(db.Integer,db.ForeignKey('listing.id'))
if __name__ == "__main__":
    with app.app_context():
        db.drop_all() 
        db.create_all()
        



