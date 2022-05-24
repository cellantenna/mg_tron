from cmath import exp
from dataclasses import dataclass
import platform
from time import sleep
import serial
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s :: %(name)s :: %(message)s :: %(levelname)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="mg.log",
    filemode="a",
)


BAUDRATE = 230_400
DEVICE_PORT: int = 0


def find_device(DEVICE_NUMBER: int = 0) -> list:
    """Find the Megatron device plugged into the Linux computer"""

    # Determine if system is Linux or WIN
    if platform.system().lower() == "linux":

        # Search Linux filesystem for device
        find = ["find /dev -iname '*acm*'"]
        try:
            results_ = subprocess.run(
                args=find,
                shell=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                encoding="utf-8",
                capture_output=False,
            )
            results = sorted(results_.stdout.strip().splitlines())
            # print(results[DEVICE_NUMBER])
            return results[DEVICE_NUMBER], results
        except IndexError:
            logger.warning("No device connected to machine")
            logger.exception("Device not found")

    elif platform.system().lower() == "windows":
        global PORT
        # Search Windows filesystem for device
        # filename = "COM3"
        # devices = [os.path.join(root, filename) for root, dir,
        #           files in os.walk("/user/") if filename in files]

        return "COM3"


def serial_call(*args) -> None:
    logger.debug(msg="Call to device initiated")
    logger.info(msg=f"Call initiated from {platform.system()} to USB device")
    sleep(0.1)
    global PORT
    try:
        with serial.Serial() as ser:
            ser.baudrate = BAUDRATE
            ser.port = PORT
            ser.timeout = 2  # seconds
            ser.open()
            ser.write(f"{' '.join([arg for arg in args])}".encode("utf-8"))
            # outputs: list[str] = [line.decode('ascii') for line in ser.readlines()]
            # outputs = " ".join(output for output in outputs)
            # print(outputs)
    except (serial.SerialException, NameError):
        logger.exception(msg="No device found")


@dataclass(slots=True)
class Megatron:
    """Class to organize the manipulation of 8 channels"""

    try:
        global PORT
        PORT = find_device(DEVICE_PORT)[0]
    except TypeError:
        logger.error(msg="No device found on system")
        logger.exception(msg="No device found on system")

    def status(self) -> None:
        """Check the status of the board"""

        serial_call("s")

    def change_power(self, channel: int, power_level: int) -> None:
        """
        Change the power level of a channel
        Range: 0 - 63
        """

        serial_call("p", str(channel), str(power_level))

    def change_freq(self, channel: int, frequency: float) -> None:
        """
        Change the frequency of a channel
        Range: 50 - 6400 MHz
        """

        serial_call("f", str(channel), str(frequency))

    def change_bandwidth(self, channel: int, percentage: int) -> None:
        """
        Change the bandwidth of a channel
        Range: 0 - 100
        """

        serial_call("b", str(channel), str(percentage))

    def save_state(self, state: bool) -> None:
        """Save each settings made by the user into memory for next startup"""

        state = 1 if state else 0
        serial_call("x", str(state))

    def amplification(self, channel: int, state: bool) -> None:
        """Output HIGH or LOW logic level out of a chosen channel"""

        state = 1 if state else 0
        serial_call("a", str(channel), str(state))

    def stability(self, state: bool) -> None:
        """Boolean a second filtering stage of capacitors for further stability"""

        state = 1 if state else 0
        serial_call("~", str(state))

    def noise_control(self, state: bool, percentage: int) -> None:
        """
        Optimal settings hardcoded; Input @ %100 Output @ %85
        state 0: Output stage
        state 1: Input stage
        """

        state = 1 if state else 0
        serial_call("n", str(state), str(percentage))

    def reset_board(self) -> None:
        """Reset the parameters of the board"""

        [
            (
                serial_call("p", str(i), "0"),
                serial_call("b", str(i), "0"),
                serial_call("f", str(i), "50.00"),
            )
            for i in range(1, 9)
        ]


def main() -> None:
    import random

    # find_device("linux")
    # test_1 = Megatron()
    print(platform.system().lower())

    # for i in range(8):
    # test_1.change_power(i+1, random.randint(a=10, b=63))
    # sleep(1)
    # test_1.change_freq(i+1, random.randint(a=50, b=6300))
    # sleep(1)
    # test_1.change_bandwidth(i+1, random.randint(a=10, b=100))
    # sleep(1)
    # sleep(1)
    # test_1.reset_board()

    # test_1.change_freq(1, 2545.54)
    # test_1.change_power(1, 63)

    # test_1.status()

    # test_1.amplification(3, True)
    # test_1.stability(True)
    # test_1.save_state(True)


if __name__ == "__main__":
    main()
