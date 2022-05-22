from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):    
  nilai_1=StringField('Value 1', validators=[DataRequired()])
  nilai_2=StringField('Value 2', validators=[DataRequired()])
  operatornya=SelectField("Operator",
              choices=[('',"Choose Operator"),('*','x'),('+','+'),('-','-'),('/','/')])
  submit=SubmitField("Save")
  