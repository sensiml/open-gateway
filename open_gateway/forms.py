from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators


class DeviceConfigureForm(FlaskForm):
    device_id = StringField("Device ID", validators=[validators.input_required()])
    source = StringField("Source", validators=[validators.input_required()])
    mode = StringField("MODE", validators=[validators.input_required()])
    baud_rate = IntegerField("Baud Rate", validators=[validators.Optional()])
    sample_rate = IntegerField("Sample Rate", validators=[validators.Optional()])
    submit = SubmitField("Submit")


class DeviceScanForm(FlaskForm):
    source = StringField("Source", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class DeviceRecordForm(FlaskForm):
    filename = StringField("File Name", validators=[validators.Optional()])
    event_type = StringField("Event Type", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class CameraForm(FlaskForm):
    event_type = StringField("Event Type", validators=[validators.input_required()])
    camera_index = IntegerField("Camera Index", validators=[validators.Optional()])
    submit = SubmitField("Submit")
