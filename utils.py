import json, hashlib
from qlks.models import User, UserRole, Rooms
from qlks import db


def read_data(path='data/room_type.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_rooms(rType_id=None, kw=None, from_price=None, to_price=None):
    rooms = Rooms.query

    if rType_id:
        rooms = rooms.filter(Rooms.room_type_id == rType_id)

    if kw:
        rooms = rooms.filter(Rooms.name.contains(kw))

    if from_price and to_price:
        rooms = rooms.filter(Rooms.price.__gt__(from_price),
                                   Rooms.price.__lt__(to_price))

    return rooms.all()


def get_room_by_id(room_id):
    return Rooms.query.get(room_id)



def check_login(username, password, role=UserRole.ADMIN):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    user = User.query.filter(User.username == username,
                             User.password == password,
                             User.user_role == role).first()

    return user

def get_user_by_id(user_id):
    return User.query.get(user_id)


def register_user(name, email, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             username=username,
             password=password,
             avatar=avatar,
             user_role=UserRole.USER)
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except:
        return False
