from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FormField, FieldList, SubmitField
from wtforms.validators import DataRequired, optional, NumberRange


class ParticipantForm(FlaskForm):
  name = StringField('Nombre', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  
class EventSelector(FlaskForm):
  events = SelectField('Mis Eventos:')
  
class EventForm(FlaskForm):
  name = StringField('Nombre: ', validators=[DataRequired()])
  min_price = IntegerField('Precio Mínimo: ', validators=[optional(), NumberRange(min=0)])
  max_price = IntegerField('Precio Máximo: ', validators=[optional(), NumberRange(min=0)])
  submit = SubmitField("Actualizar Evento")
  
  def validate(self):
    if not FlaskForm.validate(self):
      return False
    if self.min_price and self.max_price:
      if self.min_price.data > self.max_price.data:
        return False
    return True
