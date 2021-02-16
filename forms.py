from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField
from wtforms import validators


class DeviceConfigureForm(FlaskForm):
    device_id = StringField(u"Device ID", validators=[validators.input_required()])
    source = StringField(u"Source", validators=[validators.input_required()])
    mode = StringField(u"MODE", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class DeviceScanForm(FlaskForm):
    source = StringField(u"Source", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class DeviceRecordForm(FlaskForm):
    filename = StringField(u"File Name", validators=[validators.Optional()])
    event_type = StringField(u"Event Type", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class CameraForm(FlaskForm):
    event_type = StringField(u"Event Type", validators=[validators.input_required()])
    camera_index = IntegerField(u"Camera Index", validators=[validators.Optional()])
    submit = SubmitField("Submit")
