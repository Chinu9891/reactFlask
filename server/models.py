from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

follows = db.Table(
    'follows',
    db.Column('user_id', db.String(32), db.ForeignKey('user.id'), primary_key=True),
    db.Column('streamer_id', db.String(32), db.ForeignKey('streamer.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    followed_streamers = db.relationship(
        'Streamer',
        secondary=follows,
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

class Streamer(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=get_uuid, unique=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    img = db.Column(db.String(120), unique=False, nullable=False)
    isFeatured = db.Column(db.Boolean, unique=False, nullable=False)
    subscription_id = db.Column(db.String(120), unique=True, nullable=True)