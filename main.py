from flask import render_template, request, redirect
from qlks import app, utils, login
from qlks.admin import *
from flask_login import login_user
import os


@app.route("/")
def index():
    room_type = utils.read_data()
    return render_template('index1.html',
                           roomtype=room_type)


@app.route("/rooms")
def room_list():
    rType_id = request.args.get('room_type_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    rooms = utils.read_rooms(rType_id=rType_id,
                                   kw = kw,
                                   from_price=from_price,
                                   to_price=to_price)

    return render_template('room-list.html',
                           rooms=rooms)


@app.route("/rooms/<int:room_id>")
def room_detail(room_id):
    room = utils.get_room_by_id(room_id=room_id)

    return render_template('room-detail.html',
                           room=room)


@app.route('/login', methods=['post'])
def login_usr():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm-password')
        if password == confirm:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            f = request.files["avatar"]
            avatar_path = 'images/upload/%s' % f.filename
            f.save(os.path.join(app.root_path, 'static/', avatar_path))
            if utils.register_user(name=name, username=username, password=password,
                                   email=email, avatar=avatar_path):
                return redirect('/')
            else:
                err_msg = "System error , Try again!"
        else:
            err_msg = "Password not match !!"

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def get_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
