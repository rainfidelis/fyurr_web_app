#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

Show = db.Table('shows',
                 db.Column('show_id', db.Integer, primary_key=True),
                 db.Column('artists_id', db.Integer, db.ForeignKey('artists.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, nullable=False),
                 db.Column('venues_id', db.Integer, db.ForeignKey('venues.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True, nullable=False),
                 db.Column('start_time', db.DateTime, nullable=False, default=datetime.utcnow())
                 )


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(100))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    artists = db.relationship('Artist', secondary=Show,
                              backref=db.backref('venues', lazy=True))

    def __repr__(self) -> str:
        return f'<Venue {self.id, self.name, self.address}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    website = db.Column(db.String(100))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())
    

    def __repr__(self) -> str:
        return f'<Artist {self.id, self.name}>'


