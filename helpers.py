import json
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
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (0, 0, 255, 255))  # BLUE
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


def callstack_helper(channel: int):
    """Helper function to reduce clutter"""

    dpg.bind_item_theme(f"stats_{channel}", orng_btn_theme)
    print(f"Channel {channel} Information Sent")
    data_vehicle.change_power(channel, dpg.get_value(f"power_{channel}"))
    data_vehicle.change_bandwidth(
        channel, dpg.get_value(f"bandwidth_{channel}"))
    data_vehicle.change_freq(channel, dpg.get_value(f"freq_{channel}"))
    print("Ready for next command.\n")
    dpg.bind_item_theme(f"stats_{channel}", grn_btn_theme)


def callstack(sender, app_data, user_data) -> None:
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

    [
        dpg.bind_item_theme(f"stats_{i+1}", orng_btn_theme)
        for i in range(8)
    ]
    data_vehicle.save_state(state=True)
    data_vehicle.reset_board()
    [
        dpg.bind_item_theme(f"stats_{i+1}", grey_btn_theme)
        for i in range(8)
    ]

    print("Ready for next command.\n")


def send_all_channels(sender, app_data, user_data) -> None:
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


def toggle_off(sender, app_data, user_data) -> None:
    """Turn all power levels to zero"""

    print("RESET POWER Command Executed")
    [data_vehicle.change_power(i+1, 0) for i in range(8)]
    print("Ready for next command.\n")


def save_inputs(sender, app_data, user_data) -> None:
    """Save the present inputs of the fields"""

    prelim_data: list[dict[str, dict[str, str]]] = [
        {
            f"channel {channel}":
            {
                "Power": dpg.get_value(f"power_{channel}"),
                "Bandwidth": dpg.get_value(f"bandwidth_{channel}"),
                "Frequency": dpg.get_value(f"freq_{channel}"),
            },
        }
        for channel in range(1, 9)]

    with open(file="mg_tron_presets.json", mode="w") as file:
        file.write(json.dumps(obj=prelim_data, indent=2))
        print(json.dumps(obj=prelim_data, indent=2))
        print("Save Complete")


def load_inputs(sender, app_data, user_data) -> None:
    """Load the last daved data"""

    saved_data: list = []
    with open(file="mg_tron_presets.json", mode="r") as file:
        saved_data = json.loads(file.read())
    [
        (
            dpg.set_value(
                item=f"power_{channel}",
                value=saved_data[channel-1][f"channel {channel}"]["Power"]),
            dpg.set_value(
                item=f"bandwidth_{channel}",
                value=saved_data[channel-1][f"channel {channel}"]["Bandwidth"]),
            dpg.set_value(
                item=f"freq_{channel}",
                value=saved_data[channel-1][f"channel {channel}"]["Frequency"]),
        )
        #print(saved_data[channel-1][f"channel {channel}"]["Frequency"])
        for channel in range(1, 9)
    ]


def auto_fill_freq() -> None:
    """Auto fill the frequency column based on the first input"""

    [dpg.set_value(item=f"freq_{i}", value=dpg.get_value(item="freq_1"))
     for i in range(2, 9) if dpg.get_value(item="freq_1")]


def auto_fill_power() -> None:
    """Auto fill the power column based on the first input"""

    [dpg.set_value(item=f"power_{i}", value=dpg.get_value(item="power_1"))
     for i in range(2, 9) if dpg.get_value(item="power_1")]


def auto_fill_bandwidth() -> None:
    """Auto fill the bandwidth column based on the first input"""

    [dpg.set_value(item=f"bandwidth_{i}", value=dpg.get_value(item="bandwidth_1"))
     for i in range(2, 9) if dpg.get_value(item="bandwidth_1")]


def change_inputs(sender, app_data) -> None:
    """Use the mouse wheel to change the field inputs"""
    print(app_data)
    if dpg.is_item_focused(item="power_1"):
        print(dpg.get_value("power_1"))
