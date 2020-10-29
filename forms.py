from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms import validators


class SerialPortForm(FlaskForm):
    serial_port = StringField(u"SerialPort", validators=[validators.input_required()])
    submit = SubmitField("Submit")
