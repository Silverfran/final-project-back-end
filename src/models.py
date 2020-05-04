from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Roles %r>' % self.rolename

    def serialize(self):
        return {
            "rolename": self.rolename
        }

class Packages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    tracking = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Packages %r>' % self.tracking

    def serialize(self):
        return {
            "length": self.length,
            "height": self.height,
            "width": self.width,
            "weight": self.weight,
            "tracking": self.tracking
        }