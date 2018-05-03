from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, IntegerField, SelectField, \
DecimalField, DateField, BooleanField, FileField, SubmitField, TextAreaField
from wtforms.validators import Email, Length, DataRequired, Regexp, \
NumberRange

class buy_form(FlaskForm):
		quantity = IntegerField('Quantity to buy', validators=[NumberRange(min=1, message="Must buy more than 0.")])
		submit = SubmitField('Pay')


class add_listing_form(FlaskForm):
		#c = []
		#for category in FlaskForm['categories']:
			#c.append((category['category_id'], category['name']))
		title = StringField('Title', validators=[Length(min=1, message="A title is required.")])
		photo = FileField('Product Photo', validators=[FileRequired(message="Please choose an image to upload.")])
		description = TextAreaField('Description', validators=[Length(min=1, message="A description is required.")])
		original_quantity = IntegerField('Quantity For Sale', validators=[NumberRange(min=1, message="A quantity is required.")])
		unit_type = StringField('Measurement', validators=[Length(min=1, message="A measurement is required.")])
		price_per_unit = DecimalField('Price Per Unit', validators=[NumberRange(min=0.01, message="A price is required.")])
		category_id = SelectField('Category', choices=[(1, 'Vegetable'),(2, 'Fruit'),(3, 'Meat'),(4, 'Cheese')], coerce=int)
		is_tradeable = BooleanField('Should this product be tradeable?')
		date_harvested = DateField('Date Harvested', format="%Y-%m-%d")
		submit = SubmitField('Add')