from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, optional, NumberRange


class EventForm(FlaskForm):
  name = StringField('Name: ', validators=[DataRequired()], render_kw={"class": "form-control mb-2"})
  min_price = IntegerField('Minimum Price: ', validators=[optional(), NumberRange(min=0)], render_kw={"class": "form-control mb-2"})
  max_price = IntegerField('Maximum Price: ', validators=[optional(), NumberRange(min=0)], render_kw={"class": "form-control mb-2"})
  update = SubmitField("Update Event")
  create = SubmitField("Create Event")
  
  def validate(self):
    if not FlaskForm.validate(self):
      return False
    if self.min_price.data and self.max_price.data:
      if self.min_price.data > self.max_price.data:
        self.min_price.errors.append("Minimum Price Cannot Be Higher Than Maximum Price!")
        return False
    return True
