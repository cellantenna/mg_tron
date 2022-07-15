import serial as sr


class E_UTRA:
    """Table 5.7.3-1 E-UTRA channel numbers"""

    TABLE: dict[list[int], tuple[float, int]] = {
        # Band: (FDL_low, NOffs_DL)
        "1": (2100, 0),
        "2": (1930, 600),
        "3": (1805, 1200),
        "4": (2110, 1950),
        "5": (869, 2400),
        "6": (875, 2650),
        "7": (2620, 2750),
        "8": (925, 3450),
        "9": (1844.9, 3800),
        "10": (2110, 4150),
        "11": (1475.9, 4750),
        "12": (729, 5010),
        "13": (746, 5180),
        "14": (758, 5280),
        "17": (734, 5730),
        "18": (860, 5850),
        "19": (875, 6000),
        "20": (791, 6150),
        "21": (1495.9, 6450),
        "24": (1525, 7700),
        "33": (1900, 36000),
        "34": (2010, 36200),
        "35": (1850, 36350),
        "36": (1930, 36950),
        "37": (1910, 37550),
        "38": (2570, 37750),
        "39": (1880, 38250),
        "40": (2300, 38650),
        "41": (2496, 39650),
        "42": (3400, 41590),
        "43": (3600, 43590),
        "44": (3700, 45590),
    }

    @classmethod
    def band_ranges(self) -> dict[list[int]]:
        """Define the ranges of earfcns for each band"""

        band_1 = [i for i in range(0, 600)]
        band_2 = [i for i in range(600, 1200)]
        band_3 = [i for i in range(1200, 1950)]
        band_4 = [i for i in range(1950, 2400)]
        band_5 = [i for i in range(2400, 2650)]
        band_6 = [i for i in range(2650, 2750)]
        band_7 = [i for i in range(2750, 3450)]
        band_8 = [i for i in range(3450, 3800)]
        band_9 = [i for i in range(3800, 4150)]
        band_10 = [i for i in range(4150, 4750)]
        band_11 = [i for i in range(4750, 4950)]
        band_12 = [i for i in range(5010, 5180)]
        band_13 = [i for i in range(5180, 5280)]
        band_14 = [i for i in range(5280, 5380)]
        band_17 = [i for i in range(5730, 5850)]
        band_18 = [i for i in range(5850, 6000)]
        band_19 = [i for i in range(6000, 6150)]
        band_20 = [i for i in range(6150, 6450)]
        band_21 = [i for i in range(6450, 6600)]
        band_24 = [i for i in range(7700, 8040)]
        band_33 = [i for i in range(36000, 36200)]
        band_34 = [i for i in range(36200, 36350)]
        band_35 = [i for i in range(36350, 36950)]
        band_36 = [i for i in range(36950, 37550)]
        band_37 = [i for i in range(37550, 37750)]
        band_38 = [i for i in range(37750, 38250)]
        band_39 = [i for i in range(38250, 38650)]
        band_40 = [i for i in range(38650, 39650)]
        band_41 = [i for i in range(39650, 41590)]
        band_42 = [i for i in range(41590, 43590)]
        band_43 = [i for i in range(43590, 45590)]
        band_44 = [i for i in range(45590, 46590)]

        return {
            "1": band_1,
            "2": band_2,
            "3": band_3,
            "4": band_4,
            "5": band_5,
            "6": band_6,
            "7": band_7,
            "8": band_8,
            "9": band_9,
            "10": band_10,
            "11": band_11,
            "12": band_12,
            "13": band_13,
            "14": band_14,
            "17": band_17,
            "18": band_18,
            "19": band_19,
            "20": band_20,
            "21": band_21,
            "24": band_24,
            "33": band_33,
            "34": band_34,
            "35": band_35,
            "36": band_36,
            "37": band_37,
            "38": band_38,
            "39": band_39,
            "40": band_40,
            "41": band_41,
            "42": band_42,
            "43": band_43,
            "44": band_44,
        }

    @classmethod
    def convert_to_frequency(self, earfcn: int) -> float | None:
        """Convert the earfcn to a center band frequency"""

        for band in E_UTRA.band_ranges().items():
            # print(band[1])
            for i in band[1]:
                if i == earfcn:
                    FDL_low, NOffs_DL = self.TABLE.get(
                        band[0])[0], self.TABLE.get(band[0])[1]
                    return FDL_low + 0.1 * (earfcn - NOffs_DL)


class EG25G:
    """Get the neighborhood list of local celluar towers"""

    POWER_DOWN = "AT+QPOWD\r\n"
    DATA_CARRIER_DETECTION_MODE = "AT&C0\r\n"  # Always ON

    def __init__(self, port):
        self.port = port
        self.ser = sr.Serial(port, 9600, timeout=600)

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

    def set_modem_ready(self) -> bool:
        key_word = 'AT&D0\r\n'
        self.ser.write(key_word.encode())
        self.ser.flush()
        return True

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

    def get_band_scan(self) -> list[str]:
        key_word = 'AT+QCOPS=6,1,0,2\r'
        self.ser.write(key_word.encode())
        self.ser.flush()

        band_scan = self.ser.readlines()

        return band_scan

    def get_frequency_from_neighborcell_list(self) -> list[int]:

        neighborcell = self.get_neighborcell_list()

        # convert neighborcell into frequency based on EARFCN calulation
        frequency = []

        return frequency


def main():
    # eg25g = EG25G("/dev/ttyUSB3")
    # eg25g.data_carrier_detection_mode()
    # print("earfcn, pcid, rsrq, rsrp, rssi, sinr, srxlev, cell_resel_priority, s_non_intra_search, thresh_serving_low, s_intra_search")
    # eg25g.set_modem_ready()
    # [print(f"{tower.split(',')[0]}") for tower in eg25g.get_neighborcell_list()]
    # [print(f"Freq: {i}") for i in eg25g.get_frequency_from_neighborcell_list()]
    # print(eg25g.get_neighborcell_list())
    # [print(long_scan) for long_scan in eg25g.get_band_scan()]

    print(E_UTRA.convert_to_frequency(1100))

    # print(eg25g.get_band_scan())
    # print(E_UTRA.TABLE.get("4"))
    # print(eg25g.check_connection())
    # eg25g.power_down()


if __name__ == "__main__":
    main()
