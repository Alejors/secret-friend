from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField, IntegerField


class ItemForm(FlaskForm):
  element = StringField('Gift Idea:')
  price = IntegerField('Price:')
  url = StringField('Example URL: ')
  submit = SubmitField('Update Item')

class WishlistForm(FlaskForm):
  items = FieldList(FormField(ItemForm), min_entries=1)
  submit = SubmitField('Update Wishlist')
