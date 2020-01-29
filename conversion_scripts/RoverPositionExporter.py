from utils import convert_ubx
import struct
import datetime
import numpy as np


class RoverPositionExporter:
    csv_headers_hppos = 'GPSTimeOfWeek[s], lon[deg], lat[deg], h[m], h_msl[m], horizontalAcc[m], verticalAcc[m]\n'
    csv_headers_gga = 'UTC,lat[deg],N/S,lon[deg],E/W,quality,satellites[-],HDOP,altitude_msl[m],altitude_unit,geoid_sep[m],geoid_unit,diffAge[s],diffStat\n'

    def __init__(self, filepath, out_filepath):
        self.filepath = filepath
        self.out_filepath = out_filepath
        self.decode_hpposllh()
        self.decode_nmea_gga()

    def decode_hpposllh(self):
        with open(self.filepath, 'rb') as binary_file:
            with open(f'hppos_{self.out_filepath}', 'w') as csv_file:
                csv_file.write(self.csv_headers_hppos)
                binary_file.seek(0, 2)
                num_bytes = binary_file.tell()
                count = 0
                for i in range(num_bytes):
                    binary_file.seek(i)
                    four_bytes = binary_file.read(4)
                    if four_bytes == b"\xb5\x62\x01\x14":
                        count += 1
                        next_bytes = binary_file.read(2)
                        message_length = int.from_bytes(next_bytes, byteorder='little', signed=False)
                        next_bytes = binary_file.read(1)
                        version = struct.unpack('<B', next_bytes)
                        next_bytes = binary_file.read(2) # reserved
                        next_bytes = binary_file.read(1) # flags
                        next_bytes = binary_file.read(4) # GPSTow
                        iTOW = struct.unpack('<L', next_bytes)
                        next_bytes = binary_file.read(4) # lon
                        lon = struct.unpack('<l', next_bytes)
                        next_bytes = binary_file.read(4) # lat
                        lat = struct.unpack('<l', next_bytes)
                        next_bytes = binary_file.read(4) # height
                        height = struct.unpack('<l', next_bytes)
                        next_bytes = binary_file.read(4) # height msl
                        hMSL = struct.unpack('<l', next_bytes)
                        next_bytes = binary_file.read(1)
                        lonHp = struct.unpack('<b', next_bytes)
                        next_bytes = binary_file.read(1)
                        latHp = struct.unpack('<b', next_bytes)
                        next_bytes = binary_file.read(1)
                        heightHp = struct.unpack('<b', next_bytes)
                        next_bytes = binary_file.read(1)
                        hMSLHp = struct.unpack('<b', next_bytes)
                        next_bytes = binary_file.read(4)
                        hAcc = struct.unpack('<L', next_bytes)
                        next_bytes = binary_file.read(4)
                        vAcc = struct.unpack('<L', next_bytes)

                        cur_lon = lon[0] * 10**-7
                        cur_lat = lat[0] * 10**-7

                        cur_lonHp = lonHp[0] * 10**-9
                        cur_latHp = latHp[0] * 10**-9

                        cur_heightHp = heightHp[0] * 0.1
                        cur_hMSLHp = hMSLHp[0] * 0.1

                        cur_hAcc = hAcc[0] * 0.1
                        cur_vAcc = vAcc[0] * 0.1

                        hpplon = cur_lon + cur_lonHp
                        hpplat = cur_lat + cur_latHp
                        hppheight = height[0] + cur_heightHp
                        hpphMSL = hMSL[0] + cur_hMSLHp

                        to_write = f'{iTOW[0]/1000.:.3f},{hpplon:.9f},{hpplat:.9f},{hppheight/1000.:.4f},{hpphMSL/1000.:.4f},{cur_hAcc/1000.:.4f},{cur_vAcc/1000.:.4f}\n'
                        csv_file.write(to_write)

    def decode_nmea_gga(self):
        with open(self.filepath, 'rb') as binary_file:
            with open(f'gga_{self.out_filepath}', 'w') as csv_file:
                csv_file.write(self.csv_headers_gga)
                binary_file.seek(0, 2)
                num_bytes = binary_file.tell()
                count = 0
                for i in range(num_bytes):
                    binary_file.seek(i)
                    seven_bytes = binary_file.read(7)
                    if seven_bytes == b"\x24\x47\x4e\x47\x47\x41\x2c":
                        count += 1
                        message = []
                        while True:
                            count += 1
                            next_byte = binary_file.read(1)
                            if next_byte == b'*':
                                break
                            message.append(next_byte.decode("utf-8"))
                        csv_file.write(''.join(message)+'\n')
