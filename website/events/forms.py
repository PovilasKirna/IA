from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectMultipleField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_login import current_user
from flask_wtf import FlaskForm
from ..models import ClassEvent, User




class ClassEventForm(FlaskForm):
    name = StringField('Name', validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    starting_date = DateTimeField('Starting Date', format='%Y-%m-%d %H:%M:%S', validators=[
            DataRequired()
        ]
    )
    ending_date = DateTimeField('Ending Date', format='%Y-%m-%d %H:%M:%S', validators=[
            DataRequired()
        ]
    )
    
    starting_location = StringField('Starting location', validators=[
                DataRequired(),
                Length(max=50)
        ]
    )
    
    ending_location = StringField('Ending location', validators=[
                DataRequired(),
                Length(max=50)
        ]
    )
    route = TextAreaField('Route', validators=[
                DataRequired(),
                Length(max=500)
        ]
    )
    
    goal = TextAreaField('Goal', validators=[
                DataRequired(),
                Length(max=500)
        ]
    )
    
    event_content = TextAreaField('Event content', validators=[
                DataRequired(),
                Length(max=1000)
        ]
    )
    
    teacher = SelectField(u'Teacher', validators=[
                DataRequired()
        ]
    )
    
    assistant = StringField('Assistant', validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    
    destination = StringField('Destination', validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    
    attending_class = SelectField('Attending class', validators=[
                DataRequired()
        ]
    )    
    
    submit = SubmitField('Send')


    
    
    
    

