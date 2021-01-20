from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms import validators


class DeviceConfigureForm(FlaskForm):
    device_id = StringField(u"Device ID", validators=[validators.input_required()])
    source = StringField(u"Source", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class DeviceScanForm(FlaskForm):
    source = StringField(u"Source", validators=[validators.input_required()])
    submit = SubmitField("Submit")
