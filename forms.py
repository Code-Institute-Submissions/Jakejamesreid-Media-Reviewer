from wtforms import StringField, IntegerField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange

class SubmitReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    rating = IntegerField('Rating', [DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Submit Review')