import json

SHORT = 2


class BaseReader(object):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, **kwargs):
        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.sample_rate = config["CONFIG_SAMPLE_RATE"]
        self.config_columns = config.get("CONFIG_COLUMNS")
        self.data_width = len(config.get("CONFIG_COLUMNS", []))
        self.streaming = False
        self._thread = None
        self.class_map = config.get("CLASS_MAP", None)

    @property
    def packet_buffer_size(self):
        return self.samples_per_packet * self.data_width * SHORT

    def _validate_config(self, config):

        if not isinstance(config, dict):
            raise Exception("Invalid Configuration")

        if config.get("column_location", None) is None:
            raise Exception("Invalid Configuration: no column_location")
        if config.get("sample_rate", None) is None:
            raise Exception("Invalid Configuration: no sample_rate")
        if config.get("samples_per_packet", None) is None:
            raise Exception("Invalid Configuration: no samples_per_packet")

        return config



    def _validate_results_data(self, data):
        try:
            tmp = json.loads(data)
            if isinstance(tmp, dict) and tmp:
                return True
        except Exception as e:
            print(e)

        return False

    def _map_classification(self, results):
        
        if self.class_map:
            results['Classification'] = self.class_map.get(results['Classification'], results['Classification'])
        
        return results

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