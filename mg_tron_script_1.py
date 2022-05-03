
import serial

PORT = "/dev/ttyACM1"
BAUDRATE = 230_400


def serial_call(*args) -> None:

    with serial.Serial() as ser:
        ser.baudrate = BAUDRATE
        ser.port = PORT
        ser.timeout = 4  # seconds
        ser.open()
        ser.write(f"{' '.join([arg for arg in args])}".encode('utf-8'))
        outputs = [line.decode('ascii') for line in ser.readlines()]
        for output in outputs:
            print(output)


class Megatron:
    """Class to organize the manipulation of 8 channels"""

    def __init__(
            self) -> None:
        pass
    #     power: int,
    #     frequency: float,
    #     bandwidth: int,
    #     save_state: bool,
    #     amplifier_enable: bool,
    #     high_stability_mode: bool,
    #     noise_control: bool
    # ) -> None:
    #     self.power = power
    #     self.frequency = frequency
    #     self.bandwidth = bandwidth
    #     self.save_state = save_state
    #     self.amplifier_enable = amplifier_enable
    #     self.high_stability_mode = high_stability_mode
    #     self.noise_control = noise_control

    def status(self) -> None:
        """Check the status of the board"""

        serial_call('s')

    def change_power(self, channel: str, power_level: str) -> None:
        """Change the power level of a channel"""

        serial_call('p', channel, power_level)

    def change_freq(self, channel: str, frequency: str) -> None:
        """Change the power level of a channel"""

        serial_call('f', channel, frequency)

    def change_bandwidth(self, channel: str, width: str) -> None:
        """Change the power level of a channel"""

        serial_call('b', channel, width)

    def reset_board(self) -> None:

        [serial_call('p', str(i), '0') for i in range(1, 8)]
        # [serial_call('f', str(i), '50') for i in range(1, 8)]
        [serial_call('b', str(i), '0') for i in range(1, 8)]


def main() -> None:

    test_1 = Megatron()
    test_1.reset_board()
    #test_1.change_power("2", "63")
    #test_1.change_freq("2", "800")
    #test_1.change_bandwidth("2", "100")



if __name__ == '__main__':
    main()
