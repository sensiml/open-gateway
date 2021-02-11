import json
import copy
import threading
import array
SHORT = 2

import time



class RingBuffer(object):
    """ class that implements a not-yet-full buffer """
    def __init__(self,size_max):
        self.max = size_max
        self.data = array('h', [0 for _ in 512])

    """ class that implements a full buffer """
    def append(self, x):
        """ Append an element overwriting the oldest one. """
        self.data[self.cur] = x
        self.cur = (self.cur+1) % self.max

    def extend(self, x):
        """ add multiple elements to the array, overwriting the oldes ones. """

        end = self.get_post_to_end()
        data_size = len(x)

        if self.cur+data_size >= self.max:
            self.data[self.cur:] = x[:end]
            self.data[:data_size-end] = x[end:]
            self.cur=data_size-end
        else:
            self.data[self.cur:self.cur+data_size]=x
            self.cur+=data_size            

    def get(self):
        """ return list of elements in correct order """
        return self.data[self.cur:]+self.data[:self.cur]


    def get_size_to_end(self):
        return self.max - self.cur

    def get_size_from_start(self):
        return self.cur

    def get_data_length(self, pos):
        if pos > self.cur:
            return self.max-pos+self.cur

        return self.cur-pos

    def get_pos_to_end(self, pos):
        if pos > self.cur:
            return self.max - pos

        return 0


    def get_pos_from_start(self, pos):
        if pos > self.cur:
            return self.cur

        return self.pos-self.cur

    def get_data_packet(self, pos, packet_size):
        pass



class CircularBufferQueue(object):
    def __init__(self, lock, num_buffers=4, buffer_size=128):
        self._lock = lock
        self._data = [b"" for _ in range(num_buffers)]
        self._index = 0
        self._maxsize = buffer_size
        self._num_buffers = num_buffers

    def describe_buffer_state(self):
        print('current index', self._index)
        for i in range(self._num_buffers):
            print(i, "len:", len(self._data[i]))


    def _increment(self):
        """ Increment and clear next buffer """
        self._index = (self._index+1) % self._num_buffers
        self._data[self._index] = b""

    def update_buffer(self, data):

        with self._lock:             
            size = len(self._data[self._index])+len(data)
            # print('data', len(self._data[self._index]), 'new data', len(data), "max_size", self._maxsize)

            if size > 2*self._maxsize:
                raise Exception("Size of data is too large for buffer, increase max buffer size!")

            if  size <= self._maxsize:
                # print('updatding data')
                self._data[self._index] += data
            
            elif size >= self._maxsize:
                self._data[self._index]+=data[:size-self._maxsize]
                # print("first part", len(data[:size-self._maxsize]), "data size", len(self._data[self._index]))
                self._increment()
                self._data[self._index]+=data[size-self._maxsize:]
                # print("second part", len(data[size-self._maxsize:]), "data size", len(self._data[self._index]))

            if self.is_buffer_full(self._index):
                # print('buffer was filled')
                self._increment()

            # self.describe_buffer_state()

    def get_index(self, index):
        return index % self._num_buffers    

    def is_buffer_full(self, index):
        if len(self._data[index]) == self._maxsize:
            return True
        
        return False

    def read_buffer(self, buffer_index):

        with self._lock:
            return copy.deepcopy(self._data[buffer_index])

    def reset_buffer(self):
        for i in range(self._num_buffers):
            self._data[i] = b""

    def get_latest_buffer(self):
        latest_buffer = self._index-1

        if self.is_buffer_full(latest_buffer):
            return latest_buffer
        
        return None

    def get_next_index(self, index):
        return (index+1) % self._num_buffers

class BufferMixin(object):

    def _init_result_buffer(self):

        self._new_data = False
        self._r_data_buffer_1 = []
        self._r_data_buffer_2 = []
        self._r_data_buff = 1

    def _update_result_buffer(self, data):

        with self._lock:
            self._new_data = True
            if self._r_data_buff == 1:
                self._r_data_buffer_1.append(data)
            if self._r_data_buff == 2:
                self._r_data_buffer_2.append(data)

    def _read_result_buffer(self):

        with self._lock:
            if self._new_data:
                self._new_data = False
                if self._r_data_buff == 1:
                    self._r_data_buff = 2
                    tmp = copy.deepcopy(self._r_data_buffer_1)
                    self._r_data_buffer_1 = []

                    return tmp

                if self._r_data_buff == 2:
                    self._r_data_buff = 1
                    tmp = copy.deepcopy(self._r_data_buffer_2)
                    self._r_data_buffer_2 = []

                    return tmp
            else:
                return None



class BaseReader(BufferMixin):
    """ Base Reader Object, describes the methods that must be implemented for each data source"""

    def __init__(self, config, device_id=None, **kwargs):
        self.samples_per_packet = config["CONFIG_SAMPLES_PER_PACKET"]
        self.sample_rate = config["CONFIG_SAMPLE_RATE"]
        self.config_columns = config.get("CONFIG_COLUMNS")
        self.data_width = len(config.get("CONFIG_COLUMNS", []))
        self.class_map = config.get("CLASS_MAP", None)
        self.device_id = device_id

        self.streaming = False

        self._thread = None
        self._lock = threading.Lock()

        self.buffer = CircularBufferQueue(self._lock, buffer_size=self.packet_buffer_size)

        self._init_result_buffer()

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
            results["Classification"] = self.class_map.get(
                results["Classification"], results["Classification"]
            )

        return results

    def send_connect(self):

        if self._thread is None:
            "Assume if there is a thread, we are already connected"

            self.send_subscribe()

            time.sleep(1)

            self.buffer.reset_buffer()

            self._thread = threading.Thread(target=self._read_source)
            self._thread.start()

        else:
            print("Thread Already Started!")

    def disconnect(self):
        self.streaming = False
        self._thread = None

        self._init_buffer()

    def read_data(self):

        print("starting read")

        if self._thread:
            pass
        else:
            print("sent connect")
            self.send_connect()

        index = self.buffer.get_latest_buffer()

        while self.streaming:                    

            if index is None:
                index = self.buffer.get_latest_buffer()                
                time.sleep(.1)
                continue
            
            if self.buffer.is_buffer_full(index):                
                data = self.buffer.read_buffer(index)
                index = self.buffer.get_next_index(index)                    

                if data:
                    yield data

            time.sleep(.1)


        print("stream ended")

    def read_result_data(self):

        print("starting read")

        if self._thread:
            pass
        else:
            print("sent connect")
            self.send_connect()

        print("starting stream")
        while self.streaming:
            data = self._read_result_buffer()
            if data is None:
                time.sleep(0.1)
                continue

            for result in data:
                if self._validate_results_data(result):
                    result = self._map_classification(json.loads(result))
                    yield json.dumps(result) + "\n"

    def read_config(self):
        pass

    def list_available_devices(self):
        return []

    def _read_source(self):
        pass

    def set_config(self, config):
        pass

    def send_subscribe(self):
        pass
