from datetime import datetime
from PySide6.QtCore import QObject, Signal
import time
import openhrv.sensor as Sensor

class Logger(QObject):
    recording_status = Signal(int)
    status_update = Signal(str)

    def __init__(self):
        super().__init__()
        self.file = None
        self.start_time = 0
        self.record_data = Sensor.SensorClient()

    def start_recording(self, file_path: str):
        if self.file:
            self.status_update.emit(f"Already writing to a file at {self.file.name}.")
            return
        self.file = open(file_path, "a+")
        self.file.write("timestamp,elapsed time,heart rate,RR interval,HRV SDNN,HRV RMSSD\n")
        self.recording_status.emit(0)
        self.status_update.emit(f"Started recording to {self.file.name}.")
        self.start_time = time.time()

    def save_recording(self):
        if not self.file:
            return
        self.file.close()
        self.recording_status.emit(1)
        self.status_update.emit(f"Saved recording at {self.file.name}.")
        self.file = None

    def write_to_file(self, data):
        if not self.file:
            return
        
        if len(data) != 4:
            self.status_update.emit("Invalid data received.")
            #return
        
        
        timestamp = datetime.now().isoformat()
        elapsed_time = time.time() - self.start_time

        self.file.write(f"{timestamp},{elapsed_time},{data[0]},{data[1]},{data[2]},{data[3]}\n")

    def handle_sensor_data(self, data):
        # This method will be called when data is processed by SensorClient
        self.write_to_file(data)
