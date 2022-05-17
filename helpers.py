#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
from time import sleep
import dearpygui.dearpygui as dpg

from interface import Megatron

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

data_vehicle: Megatron = Megatron()

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

    dpg.bind_item_theme(
        item=f"stats_{channel}",
        theme=orng_btn_theme,
    )

    print(f"Channel {channel} Information Sent")

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

    print("Ready for next command.\n")

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
            print(f"Unrecognized GUI report of a channel: \n")
            print(
                f"Sender: {sender}\n"
                f"App data: {app_data}\n"
                f"User data: {user_data}\n"
            )


def reset_button(sender, app_data, user_data) -> None:
    """Reset all channel power levels to zero"""

    print("Reset All command Sent")

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

    print("Ready for next command.\n")


def send_all_channels(sender=None, app_data=None, user_data=None) -> None:
    """Send the data from all channels at once"""

    print("Send All command executed")

    callstack_helper(channel=1)
    callstack_helper(channel=2)
    callstack_helper(channel=3)
    callstack_helper(channel=4)
    callstack_helper(channel=5)
    callstack_helper(channel=6)
    callstack_helper(channel=7)
    callstack_helper(channel=8)

    print("Ready for next command.\n")


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
        print("Save Complete")


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

    print("Custom Save enacted\n")

    prelim_data: list[dict[str, dict[str, str, str, str]]] = [
        {
            f"channel {channel}": {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
                "Date": dt_string,
                "Save_name": dpg.get_value("save_input"),
            },
        }
        for channel in range(1, 9)
    ]

    with open(file="long_save.json", mode="a") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        print(json.dumps(obj=prelim_data, indent=2))
        print("Save Complete")

    # Clear input and close input
    dpg.set_value(item="save_input", value="")
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
    print(app_data)
    if dpg.is_item_focused(item="power_1"):
        print(dpg.get_value("power_1"))


def two_point_four(sender, app_data, user_data) -> None:
    """Auto Fill the WIFI band"""

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

    auto_fill_freq(
        freq_val=650,
        freq_constant=28.54,
    )


def mission_bravo(sender, app_data, user_data) -> None:
    """Auto Fill the band 4 celluar band"""

    auto_fill_freq(
        freq_val=1950,
        freq_constant=57.1429,
    )


def mission_charlie(sender, app_data, user_data) -> None:
    """Auto Fill the band 5 celluar band"""

    auto_fill_freq(
        freq_val=2450,
        freq_constant=157.1429,
    )


def demo_config(sender, app_data, user_data) -> None:
    """Demonstration of frequency hopping"""

    # Send all constant power small freq range
    count: int = 1
    while count <= 10:

        [
            (
                dpg.set_value(item=f"freq_{i}", value=2400 + (i * 10)),
                dpg.set_value(item=f"power_{i}", value=60),
            )
            for i in range(1, 9)
        ]

        callstack_helper(channel=1)
        callstack_helper(channel=2)
        callstack_helper(channel=3)
        callstack_helper(channel=4)
        callstack_helper(channel=5)
        callstack_helper(channel=6)
        callstack_helper(channel=7)
        callstack_helper(channel=8)

        dpg.set_value(
            item=f"freq_1",
            value=0,
        )
        dpg.set_value(
            item=f"power_1",
            value=50,
        )
        callstack_helper(channel=1)
        dpg.set_value(item=f"freq_1", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=1)

        dpg.set_value(
            item=f"power_2",
            value=50,
        )
        dpg.set_value(
            item=f"freq_2",
            value=0,
        )
        callstack_helper(channel=2)
        dpg.set_value(item=f"freq_2", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=2)

        dpg.set_value(
            item=f"power_3",
            value=50,
        )
        dpg.set_value(
            item=f"freq_3",
            value=0,
        )
        callstack_helper(channel=3)
        dpg.set_value(item=f"freq_3", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=3)

        dpg.set_value(
            item=f"power_4",
            value=50,
        )
        dpg.set_value(
            item=f"freq_4",
            value=0,
        )
        callstack_helper(channel=4)
        dpg.set_value(item=f"freq_4", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=4)

        dpg.set_value(
            item=f"power_5",
            value=50,
        )
        dpg.set_value(
            item=f"freq_5",
            value=0,
        )
        callstack_helper(channel=5)
        dpg.set_value(item=f"freq_5", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=5)

        dpg.set_value(
            item=f"power_6",
            value=50,
        )
        dpg.set_value(
            item=f"freq_6",
            value=0,
        )
        callstack_helper(channel=6)
        dpg.set_value(item=f"freq_6", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=6)

        dpg.set_value(
            item=f"power_7",
            value=50,
        )
        dpg.set_value(
            item=f"freq_7",
            value=0,
        )
        callstack_helper(channel=7)
        dpg.set_value(item=f"freq_7", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=7)

        dpg.set_value(
            item=f"power_8",
            value=50,
        )
        dpg.set_value(
            item=f"freq_8",
            value=0,
        )
        callstack_helper(channel=8)
        dpg.set_value(item=f"freq_8", value=random.randint(a=2400, b=2500))
        callstack_helper(channel=8)

        count += count
        # ....


def demo_config_2(sender, app_data, user_data) -> None:
    """Demo 2 config"""

    # Take any freq 1 input
    freq_1 = dpg.get_value(
        item="freq_1",
    )

    # 100% BW
    dpg.set_value(
        item="bandwidth_1",
        value=0,
    )

    # Power: 50
    dpg.set_value(
        item="power_1",
        value=50,
    )

    callstack_helper(channel=1)

    # Add 0.2 MHz to the freq 1 value
    [
        (
            dpg.set_value(
                item="freq_1",
                value=freq_1 + i,
            ),
            sleep(0.2),
            callstack_helper(channel=1),
        )
        for i in range(1000)
        if dpg.get_value(item="freq_1") != freq_1 + 1000
    ]

    # Stop at 1GHz of travel
    freq_2 = dpg.get_value(
        item="freq_1",
    )

    # Subtract 0.2 MHz until back to start
    [
        (
            dpg.set_value(
                item="freq_1",
                value=freq_2 - _,
            ),
            sleep(0.2),
            callstack_helper(channel=1),
        )
        for _ in range(1000)
    ]

    # 100% BW
    dpg.set_value(
        item="bandwidth_1",
        value=0,
    )
    dpg.set_value(
        item="power_1",
        value=0,
    )
    callstack_helper(channel=1)


def auto_fill_custom_save(sender, app_data, user_data) -> None:
    """Grab the first and last frequency input and put as save name"""

    freq_1 = dpg.get_value("freq_1")
    freq_8 = dpg.get_value("freq_8")

    dpg.set_value(item="save_custom_input", value=str(f"{freq_1} - {freq_8}"))


def mission_delta(sender, app_data, user_data) -> None:
    """GPS blocking presets"""

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
    
