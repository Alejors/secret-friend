from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, optional, NumberRange


class EventForm(FlaskForm):
  name = StringField('Nombre: ', validators=[DataRequired()])
  min_price = IntegerField('Precio Mínimo: ', validators=[optional(), NumberRange(min=0)])
  max_price = IntegerField('Precio Máximo: ', validators=[optional(), NumberRange(min=0)])
  update = SubmitField("Actualizar Evento")
  create = SubmitField("Crear Evento")
  
  def validate(self):
    if not FlaskForm.validate(self):
      return False
    if self.min_price.data and self.max_price.data:
      if self.min_price.data > self.max_price.data:
        self.min_price.errors.append("El precio mínimo no puede ser mayor que el precio máximo!")
        return False
    return True
