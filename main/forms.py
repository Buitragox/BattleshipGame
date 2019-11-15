from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Required


# Formulario usado para que el usuario ingrese su nombre
class FormularioNombre(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired(), Length(max=15)])
    submit = SubmitField('Empezar')


# Formulario usado para que el usuario indique las coordenadas donde va a ubicar el barco y la
# dirección
class FormularioUbicar(FlaskForm):
    x = SelectField('Direccion', validators=[InputRequired()],
                choices=[("0", "a"), ("1", 'b'), ("2", 'c'), ("3", 'd'), ("4", 'e')
                , ("5", 'f'), ("6", 'g'), ("7", 'h'), ("8", 'i'), ("9", 'j')])
    y = SelectField('Direccion', validators=[InputRequired()],
                choices=[("0", "1"), ("1", '2'), ("2", '3'), ("3", '4'), ("4", '5')
                , ("5", '6'), ("6", '7'), ("7", '8'), ("8", '9'), ("9", '10')])
    direccion = SelectField('Direccion', validators=[InputRequired()],
                choices=[('1', 'Vertical'), ('2', 'Horizontal')])
    submit = SubmitField('Ubicar')


# Formulario usado para que el jugador indique las coordenadas donde va a disparar
class FormularioDisparo(FlaskForm):
    x = SelectField('Direccion', validators=[InputRequired()],
                choices=[("0", "a"), ("1", 'b'), ("2", 'c'), ("3", 'd'), ("4", 'e')
                , ("5", 'f'), ("6", 'g'), ("7", 'h'), ("8", 'i'), ("9", 'j')])
    y = SelectField('Direccion', validators=[InputRequired()],
                choices=[("0", "1"), ("1", '2'), ("2", '3'), ("3", '4'), ("4", '5')
                , ("5", '6'), ("6", '7'), ("7", '8'), ("8", '9'), ("9", '10')])
    submit = SubmitField('Disparar')
