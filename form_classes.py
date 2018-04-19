from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, \
DecimalField, DateField, BooleanField, FileField, SubmitField
from wtforms.validators import Email, Length, DataRequired, Regexp, NumberRange

class buy_form(FlaskForm):
		quantity = IntegerField('Quantity to buy', validators=[
														NumberRange(min=0.01, message="Must buy more than 0.")])
		submit = SubmitField('Make Purchase')


class add_listing_form(FlaskForm):
		title = StringField('Title', validators=[Length(
				min=1, message="A title is required.")])
		photo = FileField('Picture')
		description = StringField('Description', validators=[
															Length(min=1, message="A description is required.")])
		original_quantity = IntegerField(
				'Quantity', validators=[NumberRange(min=1, message="A quantity is required.")])
		unit_type = StringField('Measurement', validators=[
														Length(min=1, message="A measurement is required.")])
		price_per_unit = DecimalField('Price Per Unit', places=2,
																	validators=[NumberRange(min=1, message="A price is required.")])
		listing_category = SelectField('Category',
																	 choices=[('vegetable', 'Vegetable'), ('fruit', 'Fruit'), ('other', 'Other')])
		is_tradeable = BooleanField('Tradeable')
		date_harvested = DateField('Date Harvested', format="%Y-%m-%d")
		submit = SubmitField('Add')