from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms import validators


class SerialPortForm(FlaskForm):
    serial_port = StringField(u"Serial Port", validators=[validators.input_required()])
    submit = SubmitField("Submit")


class BLEDeviceListForm(FlaskForm):
    ble_device_id = StringField(u"BLE Device ID", validators=[validators.input_required()])
    submit = SubmitField("Submit")