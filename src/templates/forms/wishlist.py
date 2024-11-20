from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField, FileField


class ItemForm(FlaskForm):
  element = StringField('Idea de regalo')
  image = FileField('Carga una imagen: ')
  url = StringField('Pega la URL de una: ')

class WishlistForm(FlaskForm):
  items = FieldList(FormField(ItemForm), min_entries=3)
  submit = SubmitField('Actualizar Lista de Deseos')
