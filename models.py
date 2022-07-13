from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_security import RoleMixin, UserMixin
from flask_security import SQLAlchemyUserDatastore


db = SQLAlchemy()
ma = Marshmallow()

parser = reqparse.RequestParser()
parser.add_argument('accountName', type=str)
parser.add_argument('accountWallet', type=float)


class BankAccount(db.Model):
    __tablename__ = 'bank'

    accountID = db.Column(db.Integer, primary_key=True)
    accountName = db.Column(db.String(100), nullable=False)
    accountWallet = db.Column(db.Float)

    def __repr__(self):
        return f"Bank Account (name = {self.accountName}, available funds = {self.accountWallet}$)."

# db.create_all()


class BASchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BankAccount


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"{self.name}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"{self.email}"


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
