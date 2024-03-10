from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config

class FileDatasource:
    def __init__(self, accelerometer_data, gps_data):
        self.accelerometer_file_name = accelerometer_data #  назва файлу, звідки зчитується датасет accelerometer
        self.gps_file_name = gps_data #  назва файлу, звідки зчитується датасет gps
        self.accelerometer_file = None #  обєкт файлу для зчитування даних
        self.gps_file = None #  обєкт файлу для зчитування даних

    def startReading(self):
        try:
            self.accelerometer_file = open(self.accelerometer_file_name, 'r')
            self.gps_file = open(self.gps_file_name, 'r')

            # Пропускаємо перший рядок header
            next(self.accelerometer_file)
            next(self.gps_file)
        except Exception as e:
            print(f"Error opening files: {e}")
            raise

    def read(self) -> AggregatedData:
        accelerometer_data = self.accelerometer_file.readline().split(',') # зчитуємо дані, пропускаємо коми
        gps_data = self.gps_file.readline().split(',')

        if accelerometer_data and gps_data:
            latitude = float(gps_data[0])
            longitude = float(gps_data[1])
            gps = Gps(latitude, longitude)

            x = int(accelerometer_data[0])
            y = int(accelerometer_data[1])
            z = int(accelerometer_data[2])
            accelerometer = Accelerometer(x, y, z)

            time = datetime.now()

            return AggregatedData(accelerometer, gps, time, config.USER_ID)

    def stopReading(self):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
