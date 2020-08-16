from wtforms import StringField, SelectField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea

class SubmitReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[i for i in range(1, 11)], default=1, validators=[DataRequired()])
    comment = StringField('Comment', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit Review')