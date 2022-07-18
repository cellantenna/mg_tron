import time
import serial as sr
from colorama import Fore as F


R = F.RESET


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
        "25": (1900, 8040),
        "26": (859, 8690),
        "27": (852, 9040),
        "28": (758, 9210),
        "29": (717, 9660),
        "30": (2350, 9770),
        "31": (462.5, 9870),
        "32": (1900, 9920),
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
        "66": (2100, 66436),
        "71": (617, 66436),
    }

    @classmethod
    def _band_ranges(self) -> dict[list[int]]:
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
        band_25 = [i for i in range(8040, 8690)]
        band_26 = [i for i in range(8690, 9040)]
        band_27 = [i for i in range(9040, 9210)]
        band_28 = [i for i in range(9210, 9660)]
        band_29 = [i for i in range(9660, 9770)]  # Downlink only
        band_30 = [i for i in range(9770, 9870)]
        band_31 = [i for i in range(9870, 9920)]
        band_32 = [i for i in range(9920, 10360)]  # Downlink only
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
        band_66 = [i for i in range(66436, 67336)]
        band_71 = [i for i in range(68586, 68936)]

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
            "25": band_25,
            "26": band_26,
            "27": band_27,
            "28": band_28,
            "29": band_29,
            "30": band_30,
            "31": band_31,
            "32": band_32,
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
            "66": band_66,
            "71": band_71,
        }

    @classmethod
    def convert_to_frequency(self, earfcn: int) -> float | None:
        """Convert the earfcn to a center band frequency"""

        for band in E_UTRA._band_ranges().items():
            # print(band[1])
            for i in band[1]:
                if i == earfcn:
                    try:
                        FDL_low, NOffs_DL = self.TABLE.get(
                            band[0])[0], self.TABLE.get(band[0])[1]
                        return FDL_low + 0.1 * (earfcn - NOffs_DL)
                    except TypeError:
                        return None


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
        start = time.time()
        key_word = 'AT+QCOPS=4,0,0,1\r'
        self.ser.write(key_word.encode())
        self.ser.flush()

        band_scan = self.ser.readlines()

        end = time.time()

        # show time taken in colorama red
        print(f"{F.BLUE}Time taken to scan bands{R}: {F.RED}{str(end - start)}{R} secs")

        return band_scan


def main():
    # eg25g = EG25G("/dev/ttyUSB3")
    # eg25g.data_carrier_detection_mode()
    # time.sleep(1)
    # print("earfcn, pcid, rsrq, rsrp, rssi, sinr, srxlev, cell_resel_priority, s_non_intra_search, thresh_serving_low, s_intra_search")
    # eg25g.set_modem_ready()
    # time.sleep(1)
    # [print(f"{tower.split(',')[0]}") for tower in eg25g.get_neighborcell_list()]
    # print(eg25g.get_neighborcell_list()[0])
    # [print(long_scan) for long_scan in eg25g.get_band_scan()]
    earfcns: list = [2600, 5035, 5230, 9820, 67061, 68661,
                     750, 2175, 5110, 66961, 66786, 66661, 650, 1100, 2300]
    cell_modem: list = [1100, 2300, 2175, 2600, 5035, 5110, 5230, 8190, 650]

    # earfcns: list = [E_UTRA.convert_to_frequency(i) for i in sorted(earfcns)]
    # cell_modem: list = [E_UTRA.convert_to_frequency(
    #     i) for i in sorted(cell_modem)]

    # print the values of the earfcn that are in the cell_modem in colorama yellow
    for earfcn in sorted(earfcns):
        if earfcn in cell_modem:
            print(f"{F.YELLOW}{E_UTRA.convert_to_frequency(earfcn)}{R} MHz")
        else:
            print(f"{F.RED}{E_UTRA.convert_to_frequency(earfcn)}{R} MHz")

    # show earfcn in colorama blue
    # for earfcn in earfcns:
    #     print(f"{F.BLUE}{E_UTRA.convert_to_frequency(earfcn)}{R} MHz")

    # print band scan results in colorama yellow
    # for band_scan in eg25g.get_band_scan():
    #     print(f"{F.YELLOW}{band_scan.decode()}{R}")


if __name__ == "__main__":
    main()
