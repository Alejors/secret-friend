from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField


class ItemForm(FlaskForm):
  element = StringField('Idea de regalo')
  url = StringField('Imagen de Ejemplo')

class WishlistForm(FlaskForm):
  items = FieldList(FormField(ItemForm), min_entries=3, max_entries=3)
  submit = SubmitField('Actualizar Lista de Deseos')
