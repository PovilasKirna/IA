from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
import datetime


class NullableDateTimeField(DateTimeField):
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))


class ProposalForm(FlaskForm):
    name = StringField('Name', validators=[
            DataRequired()
        ]
    )
    description = TextAreaField('Description', validators=[
            DataRequired()
        ]
    )
    starting_date = NullableDateTimeField('Starting Date', format='%Y-%m-%d %H:%M')
    ending_date = NullableDateTimeField('Ending Date', format='%Y-%m-%d %H:%M')
    submit = SubmitField('Send')

