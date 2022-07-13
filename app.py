from flask import Flask, redirect, render_template, url_for
from flask_restful import Api
from flask_cors import CORS
from flask_security import Security, login_required, current_user
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView


from models import db, ma, user_datastore, User, Role, BankAccount
from APIs.lab1 import Lab1Get
from APIs.db_api import BankWithoutID, BankWithID
from APIs.test_api import TestWithoutID, TestWithID


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/admin/'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/admin/'
app.config['SECURITY_POST_REGISTER_VIEW'] = '/admin/'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
if 'SECURITY_PASSWORD_SALT' not in app.config:
    app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

db.init_app(app)
ma.init_app(app)
# admin = Admin(app, name='Академічна різниця',
#               base_template='my_master.html', template_mode='bootstrap3')
admin = Admin(app, name='Академічна різниця', template_mode='bootstrap3')


class UserModelView(ModelView):
    can_create = False
    edit_modal = True
    create_modal = True
    column_display_pk = True
    column_filters = ('id', 'email', 'active', 'confirmed_at', 'roles')
    column_sortable_list = ('id', 'email', 'active', 'confirmed_at', 'roles')

    def is_accessible(self):
        roles = current_user.roles
        role_names = (role.name for role in roles)
        return (current_user.is_active and
                current_user.is_authenticated and 'admin' in role_names)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))


class RoleModelView(UserModelView):
    can_create = True
    column_filters = ('id', 'name', 'description')
    column_sortable_list = ('id', 'name', 'description')


class BankModelView(UserModelView):
    can_create = True
    column_filters = ('accountID', 'accountName', 'accountWallet')
    column_sortable_list = ('accountID', 'accountName', 'accountWallet')


admin.add_view(UserModelView(User, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(BankModelView(BankAccount, db.session))


admin.add_link(MenuLink(name='Login', category='', url="/login"))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

security = Security(app, user_datastore)

api.add_resource(Lab1Get, '/api/v1/hello-world-000')

api.add_resource(TestWithoutID, '/test-api/bank/')
api.add_resource(TestWithID, '/test-api/bank/<int:id>')

api.add_resource(BankWithoutID, '/api/bank/')
api.add_resource(BankWithID, '/api/bank/<int:id>')

api.init_app(app)


@app.before_first_request
def create_user():
    user = User.query.filter_by(email='admin').first()
    if user is None:
        user_datastore.create_user(email='admin', password='admin')
        db.session.commit()
    if Role.query.filter_by(name='admin').first() is None:
        user_datastore.create_role(name='admin')
        db.session.commit()
        role = Role.query.filter_by(name='admin').first()
        user = User.query.filter_by(email='admin').first()
        user_datastore.add_role_to_user(user, role)
        db.session.commit()


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for,
        h=admin_helpers
    )


@app.route('/')
@login_required
def index():
    return render_template('index.html')


if(__name__ == "__main__"):
    app.run(host='127.0.0.1', port=8080, debug=True)
