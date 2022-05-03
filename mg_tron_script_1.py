
from dataclasses import dataclass
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


@dataclass
class Megatron:
    """Class to organize the manipulation of 8 channels"""

    def status(self) -> None:
        """Check the status of the board"""

        serial_call('s')

    def change_power(self, channel: int, power_level: int) -> None:
        """
        Change the power level of a channel
        Range: 0 - 63
        """

        serial_call('p', str(channel), str(power_level))

    def change_freq(self, channel: int, frequency: float) -> None:
        """
        Change the frequency of a channel
        Range: 50 - 6400 MHz
        """

        serial_call('f', str(channel), str(frequency))

    def change_bandwidth(self, channel: int, percentage: int) -> None:
        """
        Change the bandwidth of a channel
        Range: 0 - 100
        """

        serial_call('b', str(channel), str(percentage))

    def save_state(self, state: bool) -> None:
        """Save each settings made by the user into memory for next startup"""

        state = 1 if state else 0
        serial_call('x', str(state))

    def amplification(self, channel: int, state: bool) -> None:
        """Output HIGH or LOW logic level out of a chosen channel"""

        state = 1 if state else 0
        serial_call('a', str(channel), str(state))

    def stability(self, state: bool) -> None:
        """Boolean a second filtering stage of capacitors for further stability"""

        state = 1 if state else 0
        serial_call('~', str(state))

    def noise_control(self, state: bool, percentage: int) -> None:
        """
        Optimal settings hardcoded; Input @ %100 Output @ %85
        state 0: Output stage
        state 1: Input stage
        """

        state = 1 if state else 0
        serial_call('n', str(state), str(percentage))

    def reset_board(self) -> None:
        """Reset the parameters of the board"""

        [serial_call('p', str(i), '0') for i in range(1, 9)]
        [serial_call('b', str(i), '0') for i in range(1, 9)]
        self.save_state(False)


def main() -> None:

    test_1 = Megatron()
    test_1.reset_board()
    # test_1.change_power(3, 55)
    # test_1.change_freq(3, 1800)
    # test_1.change_bandwidth(3, 40)
    # test_1.amplification(3, True)
    # test_1.stability(True)
    # test_1.save_state(True)


if __name__ == '__main__':
    main()
