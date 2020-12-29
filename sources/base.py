class BaseReader(object):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, **kwargs):
        pass

    def read_config(self):
        pass

    def list_available_devices(self):
        pass

    def send_connect(self):
        pass

    def set_config(self):
        pass

    def read_data(self):
        pass
