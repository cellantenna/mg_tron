#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import subprocess
import dearpygui.dearpygui as dpg
from numpy import equal

from interface import Megatron, find_device

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

loggey = logging.getLogger(name=__name__)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

loggey.info(msg="class Megatron instatiated")
data_vehicle: Megatron = Megatron()

loggey.info(msg="Remote colors initialized")
dpg.create_context()

# Green Button Theme
with dpg.theme() as grn_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 255))  # GREEN
# Red Button Theme
with dpg.theme() as red_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RED
# Blue Button Theme
with dpg.theme() as blue_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 255, 255))  # BLUE
# Grey Button Theme
with dpg.theme() as grey_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (105, 105, 105, 255))  # GREY
# Orange Button Theme
with dpg.theme() as orng_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 165, 0, 255))  # ORANGE


def callstack_helper(
    channel: int,
    freq_value: float = float(),
    pwr_value: int = int(),
    bw_value: int = int(),
):
    """Helper function to reduce clutter"""

    loggey.info(msg=f"{callstack_helper.__name__} executed")

    dpg.bind_item_theme(
        item=f"stats_{channel}",
        theme=orng_btn_theme,
    )

    loggey.info(f"Channel {channel} Information Sent")

    data_vehicle.change_power(
        channel=channel,
        power_level=dpg.get_value(f"power_{channel}") if not pwr_value else 0,
    )

    data_vehicle.change_bandwidth(
        channel=channel,
        percentage=dpg.get_value(f"bandwidth_{channel}") if not bw_value else 0,
    )

    data_vehicle.change_freq(
        channel=channel,
        frequency=dpg.get_value(f"freq_{channel}") if not freq_value else 0.0,
    )

    loggey.info("Ready for next command.\n")

    [
        dpg.bind_item_theme(
            item=f"stats_{channel}",
            theme=grn_btn_theme,
        )
        if dpg.get_value(f"power_{channel}")
        else dpg.bind_item_theme(
            item=f"stats_{channel}",
            theme=grey_btn_theme,
        )
    ]


def send_vals(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class"""

    loggey.info(msg=f"{send_vals.__name__} executed")

    match user_data:
        case 1:
            callstack_helper(channel=1)
        case 2:
            callstack_helper(channel=2)
        case 3:
            callstack_helper(channel=3)
        case 4:
            callstack_helper(channel=4)
        case 5:
            callstack_helper(channel=5)
        case 6:
            callstack_helper(channel=6)
        case 7:
            callstack_helper(channel=7)
        case 8:
            callstack_helper(channel=8)
        case _:
            loggey.warning(f"Unrecognized GUI report of a channel: \n")
            loggey.debug(
                f"Sender: {sender}\n"
                f"App data: {app_data}\n"
                f"User data: {user_data}\n"
            )


def reset_button(sender, app_data, user_data) -> None:
    """Reset all channel power levels to zero"""

    loggey.info("Reset All command Sent")

    [dpg.bind_item_theme(f"stats_{i+1}", orng_btn_theme) for i in range(8)]
    data_vehicle.save_state(state=True)
    data_vehicle.reset_board()
    [
        (
            dpg.bind_item_theme(f"stats_{i+1}", grey_btn_theme),
            dpg.set_value(item=f"power_{i+1}", value=0),
            dpg.set_value(item=f"bandwidth_{i+1}", value=0),
            dpg.set_value(item=f"freq_{i+1}", value=412 + (i * 5)),
        )
        for i in range(8)
    ]

    loggey.info("Ready for next command.\n")


def send_all_channels(sender=None, app_data=None, user_data=None) -> None:
    """Send the data from all channels at once"""

    loggey.info(f"{send_all_channels.__name__} executed")

    callstack_helper(channel=1)
    callstack_helper(channel=2)
    callstack_helper(channel=3)
    callstack_helper(channel=4)
    callstack_helper(channel=5)
    callstack_helper(channel=6)
    callstack_helper(channel=7)
    callstack_helper(channel=8)

    loggey.info("Ready for next command.\n")


def quick_save(sender, app_data, user_data) -> None:
    """Save the present inputs of the fields"""

    prelim_data: list[dict[str, dict[str, str, str, str]]] = [
        {
            f"channel {channel}": {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
                "Date": dt_string,
            },
        }
        for channel in range(1, 9)
    ]

    with open(file="quick_save.json", mode="w") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        loggey.info("Save Complete")


def quick_load(sender, app_data, user_data) -> None:
    """Load the last daved data"""

    saved_data: list = []
    with open(file="quick_save.json", mode="r") as file:
        saved_data = json.loads(file.read())
    [
        (
            dpg.set_value(
                item=f"power_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Power"],
            ),
            dpg.set_value(
                item=f"bandwidth_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Bandwidth"],
            ),
            dpg.set_value(
                item=f"freq_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Frequency"],
            ),
        )
        for channel in range(1, 9)
    ]


def custom_save(sender, app_data, user_data) -> None:
    """Save config w/ a custom name"""

    loggey.info(f"{custom_save.__name__} executed")

    prelim_data: list[dict[str, dict[str, str, str, str]]] = [
        {
            f"channel {channel}": {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
                "Date": dt_string,
                "Save_name": dpg.get_value(item="save_custom_input")
                if dpg.get_value(item="custom_save_input")
                else dpg.set_value(item="save_custom_input", value="Must be filled"),
            },
        }
        for channel in range(1, 9)
    ]

    with open(file="long_save.json", mode="a") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        loggey.debug(json.dumps(obj=prelim_data, indent=2))
        loggey.info("long save Complete")

    # Clear input and close input
    dpg.set_value(item="save_custom_input", value="")
    dpg.configure_item(item="modal_save", show=False)


def custom_load(sender, app_data, user_data) -> None:
    """Load config /w a custom name"""

    saved_data: list = []
    with open(file="quick_save.json", mode="r") as file:
        saved_data = json.loads(file.read())
    [
        (
            dpg.set_value(
                item=f"power_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Power"],
            ),
            dpg.set_value(
                item=f"bandwidth_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Bandwidth"],
            ),
            dpg.set_value(
                item=f"freq_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Frequency"],
            ),
        )
        for channel in range(1, 9)
        if dpg.get_value(item="modal_load")
        == saved_data[channel - 1][f"channel {channel}"]["Save_name"]
    ]


def auto_fill_freq(
    sender=None,
    app_data=None,
    user_data=None,
    freq_val: float = 0.0,
    freq_constant: float = 5.0,
) -> None:
    """Auto fill the frequency column based on the first input"""

    [
        dpg.set_value(
            item=f"freq_{i}",
            value=(
                abs(dpg.get_value(f"freq_{i-2}") - dpg.get_value(f"freq_{i-1}"))
                + dpg.get_value(f"freq_{i-1}")
            )
            if int(dpg.get_value(item=f"freq_{i}")) <= 6400
            else 6400,
        )
        for i in range(3, 9)
        if not freq_constant
    ]

    [
        dpg.set_value(
            item=f"freq_{i}",
            value=freq_val + freq_constant * (i - 1)
            if float(dpg.get_value(item=f"freq_{i}")) <= 6400.00
            else 6400.00,
        )
        for i in range(1, 9)
        if freq_constant
    ]


def auto_fill_power() -> None:
    """Auto fill the power column based on the first input"""

    [
        dpg.set_value(item=f"power_{i}", value=dpg.get_value(item="power_1"))
        for i in range(2, 9)
    ]


def auto_fill_bandwidth() -> None:
    """Auto fill the bandwidth column based on the first input"""

    [
        dpg.set_value(item=f"bandwidth_{i}", value=dpg.get_value(item="bandwidth_1"))
        for i in range(2, 9)
    ]


def change_inputs(sender, app_data, user_data) -> None:
    """Use the mouse wheel to change the field inputs"""
    loggey.info(f"app data: {app_data}")
    if dpg.is_item_focused(item="power_1"):
        loggey.debug(dpg.get_value("power_1"))


def two_point_four(sender, app_data, user_data) -> None:
    """Auto Fill the WIFI band"""

    loggey.info(f"{two_point_four.__name__} executed")

    dpg.set_value(item=f"freq_1", value=2415)
    dpg.set_value(item=f"freq_2", value=2440)
    dpg.set_value(item=f"freq_3", value=2455)
    dpg.set_value(item=f"freq_4", value=5213)
    dpg.set_value(item=f"freq_5", value=5760)
    dpg.set_value(item=f"freq_6", value=5195)
    dpg.set_value(item=f"freq_7", value=5510)
    dpg.set_value(item=f"freq_8", value=5705)


def mission_alpha(sender, app_data, user_data) -> None:
    """Auto Fill the band 2 celluar band"""

    loggey.info(msg=f"{mission_alpha.__name__} executed")

    auto_fill_freq(
        freq_val=650,
        freq_constant=28.54,
    )


def mission_bravo(sender, app_data, user_data) -> None:
    """Auto Fill the band 4 celluar band"""

    loggey.info(msg=f"{mission_bravo.__name__} executed")

    auto_fill_freq(
        freq_val=1950,
        freq_constant=57.1429,
    )


def mission_charlie(sender, app_data, user_data) -> None:
    """Auto Fill the band 5 celluar band"""

    loggey.info(msg=f"{mission_charlie.__name__} executed")

    auto_fill_freq(
        freq_val=2450,
        freq_constant=157.1429,
    )


def demo_config(sender, app_data, user_data) -> None:
    """Demonstration of frequency hopping"""

    loggey.info(msg=f"{demo_config.__name__} executed")


def demo_config_2(sender, app_data, user_data) -> None:
    """Demo 2 config"""

    loggey.info(msg=f"{demo_config_2.__name__} executed")


def auto_fill_custom_save(sender, app_data, user_data) -> None:
    """Grab the first and last frequency input and put as save name"""

    loggey.info(msg=f"{auto_fill_custom_save.__name__} executed")

    freq_1 = dpg.get_value("freq_1")
    freq_8 = dpg.get_value("freq_8")

    dpg.set_value(item="save_custom_input", value=str(f"{freq_1} - {freq_8}"))


def mission_delta(sender, app_data, user_data) -> None:
    """GPS blocking presets"""

    loggey.info(msg=f"{mission_delta.__name__} executed")

    dpg.set_value(item=f"freq_1", value=1221)
    dpg.set_value(item=f"power_1", value=10)
    dpg.set_value(item=f"bandwidth_1", value=100)

    dpg.set_value(item=f"freq_2", value=1236)
    dpg.set_value(item=f"power_2", value=10)
    dpg.set_value(item=f"bandwidth_2", value=100)

    dpg.set_value(item=f"freq_3", value=1248)
    dpg.set_value(item=f"power_3", value=10)
    dpg.set_value(item=f"bandwidth_3", value=100)

    dpg.set_value(item=f"freq_4", value=1260)
    dpg.set_value(item=f"power_4", value=10)
    dpg.set_value(item=f"bandwidth_4", value=100)

    dpg.set_value(item=f"freq_5", value=1557)
    dpg.set_value(item=f"power_5", value=10)
    dpg.set_value(item=f"bandwidth_5", value=100)

    dpg.set_value(item=f"freq_6", value=1572)
    dpg.set_value(item=f"power_6", value=10)
    dpg.set_value(item=f"bandwidth_6", value=100)

    dpg.set_value(item=f"freq_7", value=1587)
    dpg.set_value(item=f"power_7", value=10)
    dpg.set_value(item=f"bandwidth_7", value=100)

    dpg.set_value(item=f"freq_8", value=1605)
    dpg.set_value(item=f"power_8", value=10)
    dpg.set_value(item=f"bandwidth_8", value=100)


def kill_channel(sender, app_data, user_data: int) -> None:
    """Kill channel w/out resetting power on user facing screen"""

    data_vehicle.change_power(
        channel=user_data,
        power_level=0,
    ),
    dpg.bind_item_theme(item=f"stats_{user_data}", theme=grey_btn_theme),


def device_names() -> list[str]:
    """Use a bash script to list connected microarchitectures"""

    try:
        devices: str = subprocess.check_output(
            "src/gui/find_dev.sh", stderr=subprocess.STDOUT
        ).decode("utf-8")
    except TypeError:
        loggey.exception(msg="No devices detected")

    devices: list = devices.strip().split(sep="\n")

    return sorted(devices)


def device_finder(sender, app_data, user_data: int) -> None:
    """List all the usb microcontrollers connected to the machine"""

    # user data contains the chosen port number

    # reinitialize the method to update the device selected
    new_device = find_device(user_data)[0]
    devices = device_names()
    device = [device.split(sep="_") for device in devices]
    # print_device = [device[dev][-1] for dev in device if dev[0].split(sep="-")[0] == new_device]
    # print("New Device: ", int(new_device[-1]))
    # print("Old Device: ", str(device[0][0].split(sep="-")[0])[-2])
    for dev in range(len(device)):
        if int(new_device[-1]) == int(device[dev][0].split(sep="-")[0][-2]):
            dpg.set_value(item="device_indicator", value=f"Device:{device[dev][-1]}")


loggey.debug(msg="EOF")