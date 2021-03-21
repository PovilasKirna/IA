import secrets, os
from flask import url_for, current_app, redirect, abort
from .. import mail
from flask_mail import Message
from PIL import Image
from functools import wraps


def Qson(proposals):
    json = "{'data':["
    d = {}
    for row in proposals:
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
            i= str(d)
        json=json+i+','
    json+="]}"
    coma = json.find(',', len(json)-5)
    first_part = json[:coma] 
    last_part = json[coma+1:]
    json =first_part + last_part
    return json.replace("'", '"')

def elligible(curr_user):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not curr_user.registered:
                return redirect(url_for('users.registered'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

def roleRequired(curr_user, role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not curr_user.role == role:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request', 
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    
    msg.body =f'''To reset your password, visit the following link:\n
{url_for('users.reset_token', token=token, _external=True)}\n
If you did not make this request then simply ignore this email and no changes will be made.
    '''
    
    mail.send(msg)
    

def notify_admin_about_new_user(user, admin):
    msg = Message(
        'New User Registered', 
        sender='noreply@demo.com',
        recipients=[admin.email]
    )
    msg.body =f'''A new user just registered it's details:\n
Full name: {user.name} {user.surname}\n
Email: {user.email}\n
Phone:{user.phone}\n

Please register new users when you come back online.'''
    
    mail.send(msg)