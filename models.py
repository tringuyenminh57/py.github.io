from sqlalchemy import Column, Integer, Float, String, \
    Boolean, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from qlks import db
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from enum import Enum as UserEnum

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    def __str__(self):
        return self.name



class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(Base, UserMixin):
    __tablename__ = 'user'

    email = Column(String(100))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class Guest_Type(Base):
    __tablename__= "guest_type"
    guest = relationship("Guest", backref="guest_type",lazy=True)


class Guest(Base):
    __tablename__="guest"
    #CM thu
    identity_num=Column(String(50),nullable=False)
    address=Column(String(50),nullable=False)
    guest_type_id = Column(Integer,ForeignKey(Guest_Type.id),nullable=False)
    reservation = relationship('Reservation', backref='guest', lazy=True)
    payment= relationship('Payment',backref='guest',lazy=True)
    #user_id= Column(Integer, ForeignKey(User.id),nullable=False)




class Room_Type(Base):
    __tablename__= "room_type"
    rooms= relationship('Rooms',backref= 'room_type',lazy=True)


class Room_Status(Base):
    __tablename__= "room_status"
    rooms= relationship('Rooms',backref='room_status',lazy=True)


class Rooms(Base):
    __tablename__ = "rooms"
    price = Column(Float, default=0)
    description=Column(String(200),nullable=True)
    room_type_id = Column(Integer,ForeignKey(Room_Type.id),nullable=False)
    room_status_id=Column(Integer,ForeignKey(Room_Status.id),nullable=False)
    reservation = relationship('Reservation', backref='rooms', lazy=True)


class Reservation(Base):
    __tablename__="reservation"
    # ngay thue
    checkin = Column(Date,nullable=False)
    #ngay tra
    checkout=Column(Date,nullable=False)
    #so luong nguoi o = guest number
    guest_num= Column(Integer,nullable=False)
    room_id= Column(Integer,ForeignKey(Rooms.id),nullable=False)
    guest_id= Column(Integer,ForeignKey(Guest.id),nullable=False)
    payment= relationship('Payment',backref='reservation',lazy=True)


class Payment(Base):
    __tablename__= "payment"
    reservation_id= Column(Integer,ForeignKey(Reservation.id),nullable=False)
    guest_id= Column(Integer,ForeignKey(Guest.id),nullable=False)



class RoomModelView(ModelView):
    column_display_pk = True
    can_create = True
    can_export = True
    form_columns = ('name', )



if __name__== '__main__':
    db.create_all()