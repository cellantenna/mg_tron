#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import dearpygui.dearpygui as dpg
import configparser
import json
import logging
import pathlib
import platform
import subprocess
from datetime import datetime
from io import StringIO

import pandas as pd
from pysondb import db, errors

from interface import Megatron, find_device

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
WORKING = ROOT / "src" / "gui"

# datetime object containing current date and time
now = datetime.now()
VERSION: str = "1.1.11"

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
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (105, 105, 105, 255))  # GREY
# Orange Button Theme
with dpg.theme() as orng_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (255, 165, 0, 255))  # ORANGE

# load the intial contents of the database for comparison upon new save
loggey.info(msg="inital loading database")
try:
    init_save_data = db.getDb(f"{ROOT}/src/gui/db/long_save.json")
except FileNotFoundError:
    loggey.exception(msg="No save file detected OR save file corrupted")
    loggey.warning(
        msg="Save file being overwritten due to corruption or nonexistence")
    with open(file=f"{ROOT}/src/gui/db/long_save.json", mode="w") as overwrite_corruption_or_create:
        overwrite_corruption_or_create.write('{"data":[]}')
init_save_data: set = set(data["save_name"]
                          for data in init_save_data.getAll())


def device_names() -> list[str]:
    """Use a bash script to list connected microarchitectures"""

    # Avoid crashing program if there are no devices detected
    try:
        listing_script = [
            f'#!/bin/bash\n'
            f'for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev | grep "ACM"); do\n'
            f'(syspath={"${sysdevpath%/dev}"}\n'
            f'devname={"$(udevadm info -q name -p $syspath)"}\n'
            f'[[ {"$devname"} == "bus/"* ]] && exit\n'
            f'eval "$(udevadm info -q property --export -p $syspath)"\n'
            f'[[ -z "$ID_SERIAL" ]] && exit\n'
            f'echo "/dev/$devname - $ID_SERIAL"\n'
            f') done']
        devices = subprocess.run(
            args=listing_script,
            shell=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            capture_output=False,
        )
    except TypeError:
        loggey.exception(msg="No devices detected")

    devices: list = list(devices.stdout.strip().split(sep="\n"))

    loggey.info(msg=f"Devices found: {devices} | {device_names.__name__}")

    # If there is only one device skip the hooplah
    if len(devices) == 1:
        return devices
    return sorted(devices)


DEVICE: list[str] = device_names()


def callstack_helper(
    channel: int,
    freq_value: float = float(),
    pwr_value: int = int(),
    bw_value: int = int(),
):
    """Helper function to reduce clutter"""

    loggey.info(msg=f"{callstack_helper.__name__}() executed")

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
        percentage=dpg.get_value(
            f"bandwidth_{channel}") if not bw_value else 0,
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

    loggey.info(msg=f"{send_vals.__name__}() executed")

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

    loggey.info(f"{send_all_channels.__name__}() executed")

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

    with open(file=f"{ROOT}/src/gui/db/quick_save.json", mode="w") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        loggey.info("Save Complete")


def quick_load(sender, app_data, user_data) -> None:
    """Load the last daved data"""

    saved_data: list = []
    with open(file=f"{ROOT}/src/gui/db/quick_save.json", mode="r") as file:
        saved_data = json.loads(file.read())
    [
        (
            dpg.set_value(
                item=f"power_{channel}",
                value=saved_data[channel - 1][f"channel {channel}"]["Power"],
            ),
            dpg.set_value(
                item=f"bandwidth_{channel}",
                value=saved_data[channel -
                                 1][f"channel {channel}"]["Bandwidth"],
            ),
            dpg.set_value(
                item=f"freq_{channel}",
                value=saved_data[channel -
                                 1][f"channel {channel}"]["Frequency"],
            ),
        )
        for channel in range(1, 9)
    ]


def custom_save(sender, app_data, user_data) -> None:
    """Save config w/ a custom name"""

    print(f"sender: {sender}")
    print(f"app_data: {app_data}")
    loggey.info(f"{custom_save.__name__}() executed")

    try:
        custom_save_file = db.getDb(f"{ROOT}/src/gui/db/long_save.json")
        custom_save_file.addMany(
            [
                {
                    "save_name": dpg.get_value(item="save_custom_input"),
                    "Power": dpg.get_value(f"power_{channel}"),
                    "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                    "Frequency": dpg.get_value(f"freq_{channel}"),
                    "Date": dt_string
                }
                for channel in range(1, 9)
            ]
        )

    except (
        TypeError,
        IndexError,
        KeyError,
        errors.db_errors.SchemaError,
        AttributeError,
        json.JSONDecodeError,
    ):
        loggey.exception(msg=f"database failure | {custom_save.__name__}()")

    # Clear input and close input
    dpg.set_value(item="save_custom_input", value="")
    dpg.configure_item(item="modal_save", show=False)


def custom_load() -> list:
    """Load config /w a custom name"""

    loggey.debug(msg="Attempting to load custom save data")

    try:
        custom_save_file = db.getDb(f"{ROOT}/src/gui/db/long_save.json")
    except FileNotFoundError:
        loggey.exception(msg="No custom save file found")

    try:
        return custom_save_file.getAll()
    except json.JSONDecodeError:
        loggey.exception(msg="No save file detected OR save file corrupted")
        loggey.warning(
            msg="Save file being overwritten due to corruption or nonexistence")
        with open(file=f"{ROOT}/src/gui/db/long_save.json", mode="w") as overwrite_corruption_or_create:
            overwrite_corruption_or_create.write('{"data":[]}')
        return custom_save_file.getAll()


def load_chosen(sender=None, app_data=None, user_data: tuple[str, int] = None) -> None:
    """Take in the chosen file to be loaded"""

    loggey.info(f"{load_chosen.__name__}() executed")
    _custom_load = db.getDb(f"{ROOT}/src/gui/db/long_save.json")
    _ret_data: list[dict[str]] = _custom_load.getBy(
        {"save_name": user_data[0]})

    [
        (
            dpg.set_value(item=f"freq_{itera}", value=data["Frequency"]),
            dpg.set_value(item=f"power_{itera}", value=data["Power"]),
            dpg.set_value(item=f"bandwidth_{itera}", value=data["Bandwidth"])
        )
        for itera, data in enumerate(_ret_data, start=1)
    ]


def delete_chosen(sender=None, app_data=None, user_data: tuple[str, int] = None) -> None:
    """Delete a saved file"""

    # Get the list of saved objects
    _custom_load = db.getDb(f"{ROOT}/src/gui/db/long_save.json")

    # Get primary key for every name in the database matching the chosen name
    _ret_data: list[dict[str]] = _custom_load.getBy(
        {"save_name": user_data[0]})

    # Get the primary key for every chosen name
    primary_keys: list[int] = [data["id"] for data in _ret_data]

    # Set show=False for delete menu items that are no longer validl; Live update
    dpg.configure_item(item=f"delete_{user_data[1]}", show=False)
    dpg.configure_item(item=f"load_{user_data[1]}", show=False)

    loggey.info(
        f"Live update of delete and load menu items | {delete_chosen.__name__}()")

    try:
        # Loop through the primary keys and delete them
        loggey.info(f"Deleted {user_data[0]}")
        [
            _custom_load.deleteById(pk=primary_key) for primary_key in primary_keys
        ]
        dpg.configure_item(item="modal_delete", show=False)

        # Popup confirmation of deletion of the loaded options
        # with dpg.popup(
        #     parent="delete_button",
        # ):
        #     dpg.add_text(
        #         default_value=f"Deleted {user_data[0]}",
        #         tag="delete_popup",
        #     )
    except (errors.db_errors.IdNotFoundError):
        loggey.exception(
            msg=f"database deletion error | {delete_chosen.__name__}()")


def refresh_save_data(sender, app_data, user_data) -> None:
    """Refresh the saved data and send to the GUI"""

    loggey.info(
        msg=f"Refresh save data method called | {refresh_save_data.__name__}")

    # Refresh the saved data
    try:
        _custom_load = db.getDb(f"{ROOT}/src/gui/db/long_save.json")
    except FileNotFoundError:
        loggey.exception(msg="No custom save file found")

    # Compare the database before and after a new item is saved
    unique_names: set = set(data["save_name"]
                            for data in _custom_load.getAll())
    global init_save_data

    # Detect if new saved data has been added
    new_data: set = unique_names.difference(init_save_data)

    loggey.info(
        msg=f"New save data detected | {refresh_save_data.__name__}()") if new_data else loggey.info(
            msg=f"No new save data detected | {refresh_save_data.__name__}()")

    if new_data:
        loggey.debug(msg="Custom load options compared")

        # Get the length of the initial save data
        init_save_data_length: int = len(init_save_data)

        with dpg.popup(
            parent="custom_load_button",
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_loaded",
        ):

            # Using one for loop for both did not work as expected
            {
                dpg.add_menu_item(
                    parent="modal_loaded",
                    label=unique,
                    tag=f"load_{itera + init_save_data_length}",
                    callback=load_chosen,
                    user_data=(unique, itera+init_save_data_length),
                ) for itera, unique in enumerate(unique_names, start=0)
            }

        with dpg.popup(
            parent="delete_button",
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_deleted",
        ):

            {
                dpg.add_menu_item(
                    parent="modal_deleted",
                    label=unique,
                    tag=f"delete_{itera + init_save_data_length}",
                    callback=delete_chosen,
                    user_data=(unique, itera+init_save_data_length),
                ) for itera, unique in enumerate(unique_names, start=0)
            }

    # make the new save data the initial save data
    init_save_data = unique_names


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
                abs(dpg.get_value(f"freq_{i-2}") -
                    dpg.get_value(f"freq_{i-1}"))
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
        dpg.set_value(item=f"bandwidth_{i}",
                      value=dpg.get_value(item="bandwidth_1"))
        for i in range(2, 9)
    ]


def change_inputs(sender, app_data, user_data) -> None:
    """Use the mouse wheel to change the field inputs"""

    loggey.info(f"app data: {app_data}")

    if dpg.is_item_focused(item="power_1"):

        loggey.debug(dpg.get_value("power_1"))


def read_config(file: str) -> tuple[str, DEVICE]:
    """Read the config file and return the contents"""

    devices = DEVICE
    parser = configparser.ConfigParser()
    parser.read(filenames=file, encoding="utf-8")
    loggey.info(msg=f"file {file} read")

    return parser, devices


def mission_alpha(sender, app_data, user_data) -> None:
    """Mission alpha user facing button configuration"""

    loggey.info(msg=f"{mission_alpha.__name__}() executed")

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_alpha.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(msg="Error in reading the config file")
    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def mission_bravo(sender, app_data, user_data) -> None:
    """Mission bravo facing button config"""

    loggey.info(msg=f"{mission_bravo.__name__}() executed")

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_bravo.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(msg="Error in reading the config file")
    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def mission_charlie(sender, app_data, user_data) -> None:
    """Mission delta facing button config"""

    loggey.info(msg=f"{mission_charlie.__name__}() executed")

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_charlie.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(msg="Error in reading the config file")
    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def mission_delta(sender, app_data, user_data) -> None:
    """Mission delta facing button config"""

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_delta.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(msg="Error in reading the config file")
    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def mission_echo(sender, app_data, user_data) -> None:
    """Mission echo facing button config"""

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_echo.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        dpg.popup(
            parent="mission_buttons_border",
            modal=True,
            no_move=True,
            # mousebutton=dpg.mvMouseButton_Left,
        )
        loggey.exception(
            msg="Error in reading the config file OR config file does not exist")

    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def mission_golf(sender, app_data, user_data) -> None:
    """Mission golf facing button config"""

    [
        (
            dpg.set_value(item="freq_4", value=i),
            # callstack_helper(channel=4),
        )
        for i in range(50, 100, 10)
    ]
    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_golf.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(msg="Error in reading the config file")
    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def mission_fox(sender, app_data, user_data) -> None:
    """Mission fox facing button config"""

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/{mission_fox.__name__}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(msg="Error in reading the config file")
    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def auto_fill_custom_save(sender, app_data, user_data) -> None:
    """Grab the first and last frequency input and put as save name"""

    loggey.info(msg=f"{auto_fill_custom_save.__name__}() executed")

    freq_1 = dpg.get_value("freq_1")
    freq_8 = dpg.get_value("freq_8")

    dpg.set_value(item="save_custom_input", value=str(f"{freq_1} - {freq_8}"))


def kill_channel(sender, app_data, user_data: int) -> None:
    """Kill channel w/out resetting power on user facing screen"""

    data_vehicle.change_power(
        channel=user_data,
        power_level=0,
    ),
    dpg.bind_item_theme(item=f"stats_{user_data}", theme=grey_btn_theme),


def device_finder(sender=None, app_data=None, user_data: int = int()) -> None:
    """List all the usb microcontrollers connected to the machine"""

    # user data contains the chosen port number
    try:
        # reinitialize the method to update the device selected
        new_device = find_device(user_data)[0]
        devices = DEVICE
        device = [device.split(sep="_") for device in devices]

        for dev in range(len(device)):
            if int(new_device[-1]) == int(device[dev][0].split(sep="-")[0][-2]):
                dpg.set_value(
                    item="device_indicator", value=f"Device:{device[dev][-1]}"
                )
                dpg.configure_item(item="modal_device_config", show=False)

        # print(f"new device: {device[user_data][0].split(sep='-')[0][-2]}")
        # print(f"device indicator: {dpg.get_value('device_indicator')}")

        if dpg.get_value(item="device_indicator") != device[user_data][-1]:
            card_list: set = {1, 2, 3, 4, 5, 6, 7, 8}
            card_list.remove(device[user_data][0].split(sep='-')[0][-2] + 1)
            [dpg.bind_item_theme(
                item=f"card_{h}", theme=blue_btn_theme) for h in card_list]

    except TypeError:
        loggey.exception(msg="No devices found")


def device_refresh(sender, app_data, user_data) -> None:
    """Refresh the device list"""

    device_finder()


def fill_config():
    """Automatically fill the config file with devices detected"""

    parser, devices = read_config(
        file=f"{ROOT}/src/gui/_configs/card_config.ini")

    try:
        if not parser["mgtron"]["card_1"]:
            loggey.warning(msg="The config file was not populated")

            # Ensure eight spot in the config file are filled in if there are not eight devices
            [devices.append("0") for _ in range(8-len(devices))]

            # Automatically fill in an empty config file
            parser["mgtron"] = {
                f"card_{i+1}": str(dev.split(sep="_")[-1])
                for i, dev in enumerate(devices)
            }
            with open(file=f"{ROOT}/src/gui/_configs/card_config.ini", mode="w") as config_file:
                parser.write(config_file)
            loggey.info(msg="Config file has been automatically filled")
        else:
            loggey.info(msg="Config file already filled")
    except (KeyError, IndexError):
        loggey.exception(msg="Config file error")
        with open(file=f"{ROOT}/src/gui/_configs/card_config.ini", mode="w") as config_file:
            config_file.write("[mgtron]\n")
            config_file.write(f"card_1=\n")
        fill_config()


def config_intake() -> None:
    """Read a config file and assign card buttons"""

    parser, devices = read_config(
        file=f"{ROOT}/src/gui/_configs/card_config.ini")

    if len(devices) > 1:
        try:
            for dev_count, _ in enumerate(parser["mgtron"], start=1):
                for _, card in enumerate(devices):
                    match card.split(sep="_")[-1] == parser["mgtron"][f"card_{dev_count}"]:
                        case True if len(card) > 1:
                            dpg.bind_item_theme(
                                item=f"card_{dev_count}", theme=blue_btn_theme)
                            dpg.configure_item(
                                item=f"card_{dev_count}", enabled=True)
                            loggey.debug(
                                f"{card} is assigned to {parser['mgtron'][f'card_{dev_count}']}")
                        case False if len(card) == 1:
                            loggey.info(
                                msg=f"No device filled in on this line {platform.machine()} | {config_intake.__name__}"
                            )
                        case False:
                            loggey.warning(
                                msg=f"Device ID not detected in order OR not at all on {platform.machine()} | {config_intake.__name__}"
                            )
        except (KeyError, SystemError):
            loggey.exception(
                msg=f"No config file error | {config_intake.__name__}")


def find_signals_and_frequencies() -> dict:

    output = subprocess.Popen(
        ["nmcli", "-f", "FREQ", "dev", "wifi"], stdout=subprocess.PIPE
    )
    output2 = subprocess.Popen(
        ["nmcli", "-f", "SIGNAL", "dev", "wifi"], stdout=subprocess.PIPE
    )
    b = StringIO(output.communicate()[0].decode("utf-8"))

    df = pd.read_csv(b,
                     index_col=False,
                     delim_whitespace=True,
                     engine="python")

    c = StringIO(output2.communicate()[0].decode("utf-8"))

    signals = pd.read_csv(c,
                          index_col=False,
                          delim_whitespace=True,
                          engine="python")

    signal_column = signals.loc[:, "SIGNAL"]
    signal_list = list(signal_column)

    frequency_column = df.loc[:, "FREQ"]
    frequency_column.unique()
    freq_list = list(frequency_column)

    filtered_frequencies = [
        i for i in freq_list if i >= 2400]
    freq_and_signal = {}
    for freq in filtered_frequencies:
        for signal in signal_list:
            freq_and_signal[freq] = signal
            signal_list.remove(signal)
            break
        loggey.info(
            msg=f"Freq and Strength: {freq_and_signal} | {find_signals_and_frequencies.__name__}"
        )
    return freq_and_signal


def card_config(card_number: int = int()) -> None:

    try:

        parser, _ = read_config(
            file=f"{ROOT}/src/gui/_configs/card_{card_number}.ini")

        [
            (
                dpg.set_value(
                    item=f"freq_{config}",
                    value=float(parser['freq'][f'freq_{config}'])),

                dpg.set_value(
                    item=f"power_{config}",
                    value=float(parser['power'][f'power_{config}'])),

                dpg.set_value(
                    item=f"bandwidth_{config}",
                    value=float(parser['bandwidth'][f'bw_{config}'])),
            )

            for config in range(1, 9)
        ]

    except KeyError:
        loggey.exception(
            msg="Error in reading the config file OR config file does not exist")

    except SystemError:
        loggey.exception(
            msg="Invalid data type;  Expected floating point value")


def card_selection(sender, app_data, user_data: int) -> None:
    """Load the selected cards prefix when selected"""

    parser, _ = read_config(file=f"{ROOT}/src/gui/_configs/card_config.ini")

    loggey.info(msg=f"selected card: {user_data} | {card_selection.__name__}")

    # Manipulate the set to accomplish a loop without the currently selected button
    card_list: set[int] = {1, 2, 3, 4, 5, 6, 7, 8}
    match user_data:

        case 1:
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_1']}"
            )
            device_finder(user_data=0)

            # Blue all other active card buttons and make this one green when clicked
            card_list.remove(1)
            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=1)
            loggey.info(
                msg=f"Card 1 config loaded | {card_selection.__name__}")

        case 2:
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_2']}"
            )
            device_finder(user_data=1)

            card_list.remove(2)
            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=2)
            loggey.info(
                msg=f"Card 2 config loaded | {card_selection.__name__}")

        case 3:
            card_list.remove(3)
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_3']}"
            )
            device_finder(user_data=2)

            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=3)
            loggey.info(
                msg=f"Card 3 config loaded | {card_selection.__name__}")

        case 4:
            card_list.remove(4)
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_4']}"
            )
            device_finder(user_data=3)

            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=4)
            loggey.info(
                msg=f"Card 4 config loaded | {card_selection.__name__}")

        case 5:
            card_list.remove(5)
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_4']}"
            )
            device_finder(user_data=4)

            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=5)
            loggey.info(
                msg=f"Card 5 config loaded | {card_selection.__name__}")

        case 6:
            card_list.remove(6)
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_6']}"
            )
            device_finder(user_data=5)

            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=6)
            loggey.info(
                msg=f"Card 6 config loaded | {card_selection.__name__}")

        case 7:
            card_list.remove(7)
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_7']}"
            )
            device_finder(user_data=6)

            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=7)
            loggey.info(
                msg=f"Card 7 config loaded | {card_selection.__name__}")

        case 8:
            card_list.remove(8)
            dpg.bind_item_theme(item=f"card_{user_data}", theme=grn_btn_theme)
            dpg.set_value(
                item="device_indicator", value=f"Device:{parser['mgtron']['card_8']}"
            )
            device_finder(user_data=7)

            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]

            card_config(card_number=8)
            loggey.info(
                msg=f"Card 8 config loaded | {card_selection.__name__}")

        case _:
            loggey.warning(msg=f"Invalid card selection: {user_data}")
            card_list.remove(user_data)
            [
                dpg.bind_item_theme(
                    item=f"card_{greyed_card}", theme=blue_btn_theme)
                for greyed_card in card_list
            ]
            loggey.warning(
                msg=f"No card data loaded | {card_selection.__name__}")


def wifi_scan_jam(sender, app_data, user_data) -> None:
    """Scan the local wifi channels and jam them"""

    loggey.info(msg="Scan jammer method called")
    freq_and_strength: dict = find_signals_and_frequencies()
    [
        (
            dpg.set_value(item=f"freq_{i}", value=float(freq)),
            dpg.set_value(item=f"power_{i}", value=40),
            dpg.set_value(item=f"bandwidth_{i}", value=100),
            loggey.debug(
                msg=f"Frequency, in sig strength order, discovered: {freq}"),
            # callstack_helper(channel=i),

        )
        for i, freq in enumerate(sorted(freq_and_strength), start=1)
    ]


loggey.debug(msg="EOF")


def main():
    print(find_signals_and_frequencies())


if __name__ == '__main__':
    main()
