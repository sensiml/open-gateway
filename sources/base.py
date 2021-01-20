SHORT = 2


class BaseReader(object):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, **kwargs):
        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.sample_rate = config["CONFIG_SAMPLE_RATE"]
        self.config_columns = config.get("CONFIG_COLUMNS")
        self.data_width = len(config.get("CONFIG_COLUMNS", []))
        self.streaming = False

    @property
    def packet_buffer_size(self):
        return self.samples_per_packet * self.data_width * SHORT

    def read_config(self):
        pass

    def list_available_devices(self):
        pass

    def send_connect(self):
        pass

    def set_config(self, config):
        pass

    def read_data(self):
        pass

    def disconnect(self):
        self.streaming = False
