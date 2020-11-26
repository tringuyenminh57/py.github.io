from qlks import admin, db
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from qlks.models import Rooms, Room_Type,User,Guest,Guest_Type,Reservation,Room_Status,Payment


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated



admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Guest_Type,db.session))
admin.add_view(ModelView(Guest,db.session()))
admin.add_view(ModelView(Room_Status,db.session))
admin.add_view(ModelView(Reservation,db.session))
admin.add_view(ModelView(Payment,db.session))
admin.add_view(AuthenticatedView(Room_Type, db.session))
admin.add_view(AuthenticatedView(Rooms, db.session))

admin.add_view(ContactView(name='Contact'))
admin.add_view(LogoutView(name='Logout'))