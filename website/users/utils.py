import secrets, os
from flask import url_for, current_app, redirect, abort
from flask_mail import Message, Mail
from PIL import Image
from functools import wraps


mail = Mail()


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
    
    
def sendEmail(recipients=[], title='', email_type='', user=None):
    msg = Message(
        title,
        sender='noreply@kjg.lt',
        recipients=recipients
    )   
    if email_type == 'Password_reset':
        token = user.get_reset_token()
        msg.body=message_body.password_reset(token)
        print('Sent '+email_type+' email to '+str(recipients))
    elif email_type == 'Notify_admin_about_new_user':
        msg.body=message_body.notify_admin_about_new_user(user)
        print('Sent '+email_type+' email to '+str(recipients))
    elif email_type == 'User_registered':
        msg.body=message_body.userRegistered(user)
        print('Sent '+email_type+' email to '+ str(recipients))
    else:
        abort(500)
    mail.send(msg)

class message_body:
    @staticmethod
    def password_reset(token):
        return f'''To reset your password, visit the following link:\n
{url_for('users.reset_token', token=token, _external=True)}\n
If you did not make this request then simply ignore this email and no changes will be made.'''
    
    @staticmethod
    def notify_admin_about_new_user(user):
        return f'''A new user just registered it's details:\n
Full name: {user.name} {user.surname}\n
Email: {user.email}\n
Phone:{user.phone}\n

Please register new users when you come back online.'''
    
    @staticmethod
    def userRegistered(user):
        return f'''Welcome {user.name} {user.surname}!\n
    Our administrators approved your request to join. You can now login  using this link:\n
    {url_for('users.login', _external=True)}\n
    And start using our platform.
    '''