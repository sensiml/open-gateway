import pyaudio
import json
import struct
import math
import time
import random
import threading


from open_gateway.sources.base import (
    BaseReader,
    BaseResultReaderMixin,
    BaseStreamReaderMixin,
)


class MICReader(BaseReader):

    name = "MICROPHONE"

    def __init__(self, config, device_id, **kwargs):

        super(MICReader, self).__init__(config, device_id, **kwargs)
        print("MIC index set to", self.device_id)
        
        #TODO 
        # get these info from the UI
        self.source_samples_per_packet = config.get("SAMPLES_PER_PACKET", 100)
        self.sample_rate = config.get("SAMPLE_RATE", 16000)
        
        self._audio_channel = None 
        self._audioStream = None
        
        print("config init: ", config)

    @property
    def smaple_rate(self):
        return self._sample_rate
        
    def get_microphone_info(self):
        
        p = pyaudio.PyAudio()

        devices = p.get_device_count()
        
        mics_list = []
        i = 0 

        for device_index in range(devices):
            device_info = p.get_device_info_by_index(device_index)
            
            if device_info.get('maxInputChannels') > 0:
                mics_list.append({"id": i, "name": device_info.get('name'), "device_id": str(device_index)})
                i+=1
        
        return mics_list

    def list_available_devices(self):
        return self.get_microphone_info()


class MICStreamReader(MICReader, BaseStreamReaderMixin):
    def _send_subscribe(self):
        pass
    
    def open_stream(self):
        
        print("MIC Open Stream ... ")

        
        print("Open Stream id: ", int(self.device_id))
        print("Open Stream rate: ", self.sample_rate)
        print("Open Stream chunk: ", self.source_samples_per_packet)
        
        self._audio_channel = pyaudio.PyAudio()
        
        self._audioStream = self._audio_channel.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        input_device_index = int(self.device_id),
                        frames_per_buffer=self.source_samples_per_packet)
        
    def read_device_config(self):
        
        print("Mic Device Config: ", self.sample_rate, self.source_samples_per_packet)
        config = {}
        config["source_samples_per_packet"] = self.source_samples_per_packet
        config["sample_rate"] = self.sample_rate      
        
        config["column_location"] = {"Microphone": 0}
        config["samples_per_packet"] = self.source_samples_per_packet
        config["data_type"] = "int16"
        
        
        print("device config sample rate: ", self.sample_rate)
        print("device config sampel per pack: ", self.source_samples_per_packet)
        
        print("config: ", config)

        return config
        

    def _read_source(self):
        
        print("Microphone: Reading source stream")

        try:
            self.open_stream()
            
            device_info = self._audio_channel.get_device_info_by_index(int(self.device_id))
            print("Device Name: ", device_info.get('name'))
            print("Sample Rate: ", self.sample_rate)
            
            # self.source_samples_per_packet = 1000
            
            print("Samples per packet: ", self.source_samples_per_packet)
            
            
            
            self.streaming = True
            
            data = self._audioStream.read(100)

            if self.run_sml_model:
                sml = self.get_sml_model_obj()
            else:
                sml = None

            while self.streaming:
                
                data = self._audioStream.read(self.source_samples_per_packet)

                self.buffer.update_buffer(data)

                if self.run_sml_model:
                    model_result = self.execute_run_sml_model(sml, data)
                    if model_result:
                        self.rbuffer.update_buffer([model_result])                        

                time.sleep(0.00001)

            print("Microphone: Sending disconnect command")

        except Exception as e:
            print(e)
            self.close_stream()
            self.disconnect()
            raise e

        self.close_stream()
        
    def close_stream(self):
        
        if self._audioStream:
            self._audioStream.stop_stream()
            self._audioStream.close()
        
        if self._audio_channel:
            self._audio_channel.terminate()
        

class MICResultReader(MICReader, BaseResultReaderMixin):

    def _read_source(self):

        pass
