import serial as sr


class EG25G:
    """Get the neighborhood list of local celluar towers"""

    POWER_DOWN = "AT+QPOWD\r\n"
    DATA_CARRIER_DETECTION_MODE = "AT&C0\r\n"  # Always ON

    def __init__(self, port):
        self.port = port
        self.ser = sr.Serial(port, 9600, timeout=2)

    def power_down(self):
        self.ser.write(self.POWER_DOWN.encode())
        self.ser.flush()
        self.ser.close()

    def data_carrier_detection_mode(self):
        self.ser.write(self.DATA_CARRIER_DETECTION_MODE.encode())
        self.ser.flush()

    def check_connection(self):
        self.ser.write("AT+GMM\r\n".encode())
        self.ser.flush()
        return self.ser.readlines()[1:][0].decode().strip('\n').strip('\r')

    def get_neighborcell_list(self) -> list[list[str]]:

        key_word = 'AT+QENG="neighbourcell"\r\n'
        self.ser.write(key_word.encode())
        self.ser.flush()
        neighborcell = [line.decode().strip('\n').strip('\r')
                        for line in self.ser.readlines()][1:-2]
        neighborcell = [neighborcell.split("',")
                        for neighborcell in neighborcell]
        neighborcell = [neighborcell[:][i][0][35:] for i in range(
            len(neighborcell))]  # remove the first 35 characters

        return neighborcell

    def get_band_scan(self) -> list[list[str]]:
        key_word = f'AT+QCOP={7,1,1,2}\r\n'
        self.ser.write(key_word.encode())
        self.ser.flush()
        band_scan = [line.decode().strip('\n').strip('\r')
                     for line in self.ser.readlines()][1:-2]
        band_scan = [band_scan.split("',")
                     for band_scan in band_scan]
        band_scan = [band_scan[:][i][0][35:] for i in range(
            len(band_scan))]

        return band_scan


def main():
    eg25g = EG25G("/dev/ttyUSB3")
    eg25g.data_carrier_detection_mode()
    # print("earfcn, pcid, rsrq, rsrp, rssi, sinr, srxlev, cell_resel_priority, s_non_intra_search, thresh_serving_low, s_intra_search")
    [print(f"{tower}") for tower in eg25g.get_neighborcell_list()]
    # [print(long_scan) for long_scan in eg25g.get_band_scan()]
    # print(eg25g.check_connection())
    eg25g.power_down()


if __name__ == "__main__":
    main()
