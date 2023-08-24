from dataclasses import dataclass
from main import db

@dataclass
class Users(db.Model):
    __tablename__ = "Users"
    UserID :int = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    Username :str = db.Column(db.String,nullable=False,unique=True)
    Password :str = db.Column(db.String, nullable=False)

@dataclass
class Boards(db.Model):
    __tablename__ = "Boards"
    BoardID :int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    BoardName :str = db.Column(db.String, nullable=False)
    CreatedBy :int = db.Column(db.Integer, db.ForeignKey("Users.UserID"), nullable=False)

@dataclass
class Lists(db.Model):
    __tablename__ = "Lists"
    ListID :int = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    BoardID :int = db.Column(db.Integer, db.ForeignKey("Boards.BoardID"), nullable=False)
    ListName :str = db.Column(db.String,nullable=False)

@dataclass
class Tasks(db.Model):
    __tablename__ = "Tasks"
    TaskID :int = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    ListID :int = db.Column(db.Integer, db.ForeignKey("Lists.ListID"), nullable=False)
    TaskName :str = db.Column(db.String, nullable=False)
    Description :str = db.Column(db.String)
    Deadline :str = db.Column(db.String, nullable=False)
    Status :int = db.Column(db.Integer, nullable=False)
    CreatedBy :int = db.Column(db.Integer, db.ForeignKey("Users.UserID"), nullable=False)

@dataclass
class BoardMembership(db.Model):
    __tablename__ = "BoardMembership"
    UserID :int = db.Column(db.Integer, db.ForeignKey("Users.UserID"), nullable=False, primary_key=True)
    BoardID :int = db.Column(db.Integer, db.ForeignKey("Lists.ListID"), nullable=False, primary_key=True)
    Status :int = db.Column(db.Integer, nullable=False)