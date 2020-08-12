from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class SubmitReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit Review')