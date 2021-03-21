from flask import Flask, redirect, url_for, flash, abort,request, Response
from flask_admin import Admin, AdminIndexView, babel
from flask_login import LoginManager, current_user
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_admin.menu import MenuLink
from flask_mail import Mail, Message
from .config import Config


mail = Mail()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'users.login'

from .models import User, Proposal, Pupil, Parent, Class, ClassEvent

def expose(url='/', methods=('GET',)):
    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f
    return wrap

class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and (current_user.role == 'Admin' or current_user.role == 'Manager'):
            return current_user.is_authenticated
        else:
            flash('You cannot access that page!', category='error')
            self.inaccessible_callback(name='')
    
    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class MyAdminIndexView(AdminIndexView):
    def __init__(self, name=None, category=None,
                 endpoint=None, url=None,
                 template='admin/index.html',
                 menu_class_name=None,
                 menu_icon_type=None,
                 menu_icon_value=None):
        super(AdminIndexView, self).__init__(name or babel.lazy_gettext('Home'),
                                             category,
                                             endpoint or 'admin',
                                             '/admin' if url is None else url,
                                             'static',
                                             menu_class_name=menu_class_name,
                                             menu_icon_type=menu_icon_type,
                                             menu_icon_value=menu_icon_value)
        self._template = template

    @expose()
    def index(self):
        unregistered_users = User.query.filter_by(registered=False).all()
        return self.render(self._template, users=unregistered_users, curr_user=current_user)
    
    def is_accessible(self):
        if current_user.is_authenticated and (current_user.role == 'Admin' or current_user.role == 'Manager'):#manageris neturetu tureti galimybiu                                                                                                             #  editinti userius tik prieiga prie useri                                                                                                #  sukurtu files
            return current_user.is_authenticated
        else:
            flash('You cannot access that page!', category='error')
            self.inaccessible_callback(name='')
    
    def inaccessible_callback(self, name, **kwargs):
        abort(403)

admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap4')
admin.add_view(AdminModelView(User, db.session, category='People'))
admin.add_view(AdminModelView(Pupil, db.session, category='People'))
admin.add_view(AdminModelView(Parent, db.session, category='People'))
admin.add_view(AdminModelView(Proposal, db.session))
admin.add_view(AdminModelView(ClassEvent, db.session))
admin.add_view(AdminModelView(Class, db.session))
admin.add_link(MenuLink(name='Logout', category='', url='/logout'))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    
    from website.users.routes import users
    from website.proposals.routes import proposals
    from website.main.routes import main
    from website.errors.handlers import errors
    from website.events.routes import events

    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(proposals, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')
    app.register_blueprint(events, url_prefix='/')
    
    create_database(app)
    
    return app

def create_database(app):
    db.create_all(app=app)
    print('Created Database!')
    

