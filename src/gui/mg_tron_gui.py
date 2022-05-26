#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from typing import Any

import dearpygui.dearpygui as dpg
from interface import find_device

from helpers import (
    auto_fill_bandwidth,
    auto_fill_custom_save,
    auto_fill_freq,
    auto_fill_power,
    change_inputs,
    custom_load,
    data_vehicle,
    demo_config,
    demo_config_2,
    device_finder,
    device_names,
    kill_channel,
    mission_alpha,
    mission_bravo,
    mission_charlie,
    mission_delta,
    quick_load,
    reset_button,
    quick_save,
    send_all_channels,
    send_vals,
    custom_save,
    two_point_four,
)

logger = logging.getLogger(name=__name__)

RESOLUTION: list[int] = [1250, 735]  # 1200x800
POWER: bool = bool()
ROW_HEIGHT: int = 78
ADJUSTMENT: int = -25
DIVISOR: int = 1.4
SEND_RESET_ALL_HEIGHT: int = 695
CUSTOM_CONFIG_HEIGHT: int = 300
QUICK_CONFIG_HEIGHT: int = 480
DEMO_HEIGHT: int = 330
WIFI_HEIGHT: int = 405
CELLUAR_HEIGHT: int = 240
MAIN_TABLE_HEIGHT: int = 1
BUTTON_WIDTH = 120


dpg.create_context()
logger.info(msg="creating dpg context")


data_vehicle.save_state(False)

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

# White Button Theme
with dpg.theme() as wht_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 255, 255, 255))  # WHITE

# Grey Column Theme
with dpg.theme() as grey_column_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (185, 185, 185, 255))  # WHITE

with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=change_inputs)

with dpg.font_registry():
    default_font_added = dpg.add_font(file="src/gui/MesloLGS NF Regular.ttf", size=40)
    ital_font = dpg.add_font(file="src/gui/MesloLGS NF Italic.ttf", size=20)
    bold_font = dpg.add_font(file="src/gui/MesloLGS NF Bold Italic.ttf", size=40)
    small_font = dpg.add_font(file="src/gui/MesloLGS NF Italic.ttf", size=13)


# Primary Window
with dpg.window(
    label="MGTron Control",
    tag="Primary Window",
    height=RESOLUTION[0],
    width=RESOLUTION[1],
    pos=(0, 0),
    no_scrollbar=True,
    horizontal_scrollbar=False,
):

    # Header Column Channel
    with dpg.child_window(
        pos=(0,),  # (x, y)
        width=50,
        height=ROW_HEIGHT - ADJUSTMENT,
        border=False,
    ):
        dpg.add_text(default_value=f"CH", pos=(19, 39 - ADJUSTMENT + 5))

    # Header Column Frequency
    with dpg.child_window(
        pos=(80,),  # (x, y)
        width=200,
        height=ROW_HEIGHT - ADJUSTMENT,
        border=False,
    ):
        dpg.add_text(default_value=f"Frequency: 6.4GHz", pos=(9, 39 - ADJUSTMENT + 5))

    # Header Column Power
    with dpg.child_window(
        pos=(300,),  # (x, y)
        width=150,
        tag="col_pwr",
        height=ROW_HEIGHT - ADJUSTMENT,
        border=False,
    ):
        dpg.add_text(
            default_value=f"Power: 63",
            pos=(dpg.get_item_width("col_pwr") / 4, 39 - ADJUSTMENT + 5),
        )

    # Header Column Bandwidth
    with dpg.child_window(
        pos=(500,),  # (x, y)
        tag="col_bw",
        width=150,
        height=ROW_HEIGHT - ADJUSTMENT,
        border=False,
    ):
        dpg.add_text(
            default_value=f"BW: 100%",
            pos=(dpg.get_item_width(item="col_bw") / 3.7, 39 - ADJUSTMENT + 5),
        )

    # Right Header Column Channel Status
    # with dpg.child_window(
    #     pos=(620,),  # (x, y)
    #     width=250,
    #     height=ROW_HEIGHT - ADJUSTMENT,
    #     border=False,
    # ):
    #     dpg.add_text(default_value=f"Channel Status", pos=(60, 39 - ADJUSTMENT + 5))

    ####################################
    # Column buttons, inputs, and text #
    ####################################
    for i in range(8):

        # First Column
        with dpg.child_window(
            tag=f"row_{i+1}",
            pos=(0, ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT),  # (x, y)
            width=50,
            height=ROW_HEIGHT,
        ):
            dpg.add_text(
                default_value=i + 1,
                tag=f"channel_{i+1}",
                pos=(13, ROW_HEIGHT / 2 - 21),
            )

        # Frequency Column Input
        with dpg.child_window(
            label=f"Channel {i+1}",
            pos=(50, ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT),  # (x, y)
            width=250,
            height=ROW_HEIGHT,
        ):
            dpg.add_input_float(
                tag=f"freq_{i+1}",
                default_value=650.00 * ((i + 1)),
                min_value=50.00,
                max_value=6400.00,
                min_clamped=True,
                max_clamped=True,
                width=236,
                step=1,
                step_fast=20,
                pos=(2, ROW_HEIGHT / 2 - 15),
            )
        # Power Column Input
        with dpg.child_window(
            label=f"Channel {i+1}",
            pos=(300, ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT),  # (x, y)
            width=180,
            height=ROW_HEIGHT,
        ):
            dpg.add_input_int(
                tag=f"power_{i+1}",
                min_value=0,
                max_value=63,
                min_clamped=True,
                max_clamped=True,
                width=145,
                step_fast=3,
                pos=(13, ROW_HEIGHT / 2 - 15),
            )

        # Bandwidth Channel Input
        with dpg.child_window(
            label=f"Channel {i+1}",
            pos=(480, ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT),  # (x, y)
            width=180,
            height=ROW_HEIGHT,
        ):
            dpg.add_input_int(
                tag=f"bandwidth_{i+1}",
                min_value=0,
                max_value=100,
                min_clamped=True,
                max_clamped=True,
                width=160,
                step_fast=10,
                pos=(13, ROW_HEIGHT / 2 - 15),
            )
        # Send Button Column
        with dpg.child_window(
            pos=(660, ROW_HEIGHT * (i + MAIN_TABLE_HEIGHT) - ADJUSTMENT),
            width=(200),
            height=ROW_HEIGHT,
        ):
            # SEND Buttons
            dpg.add_button(
                label="SEND",
                tag=f"send_btn_{i+1}",
                height=50,
                width=70,
                callback=send_vals,
                user_data=i + 1,
                pos=(110, ROW_HEIGHT / 2 - 25),
            )

            # Status LED Buttons
            dpg.add_button(
                tag=f"stats_{i+1}",
                width=30,
                height=30,
                pos=(30, 25),
                enabled=True,
                callback=kill_channel,
                user_data=i + 1,
            )

            dpg.bind_item_theme(
                item=f"row_{i+1}",
                theme=grey_column_theme,
            )

    ########################
    # Auto Fill button row #
    ########################
    with dpg.child_window(
        pos=(80,),
        tag="auto_fill",
        height=65,
        width=200 * 3,
        border=False,
    ):
        dpg.add_button(
            label="AUTO\nFILL",
            tag="auto_fill_frequency",
            height=50,
            width=70,
            callback=auto_fill_freq,
            pos=(
                dpg.get_item_width(item="auto_fill") / 9,
                dpg.get_item_height(item="auto_fill") / 3 - 10,
            ),
        )
        dpg.add_button(
            label="AUTO\nFILL",
            tag="auto_fill_power",
            height=50,
            width=70,
            callback=auto_fill_power,
            pos=(
                dpg.get_item_width(item="auto_fill") / 2.2,
                dpg.get_item_height(item="auto_fill") / 3 - 10,
            ),
        )
        dpg.add_button(
            label="AUTO\nFILL",
            tag="auto_fill_bandwidth",
            height=50,
            width=70,
            callback=auto_fill_bandwidth,
            pos=(
                dpg.get_item_width(item="auto_fill") / 1.3,
                dpg.get_item_height(item="auto_fill") / 3 - 10,
            ),
        )

    [
        (
            dpg.bind_item_theme(item=f"send_btn_{i+1}", theme=blue_btn_theme),
            dpg.bind_item_theme(item=f"stats_{i+1}", theme=grey_btn_theme),
        )
        for i in range(8)
    ]  # Propgation loop

    #################
    # Device Config #
    #################
    with dpg.child_window(
        pos=(680,),
        tag="device_config",
        border=False,
        width=200,
        height=75,
    ):

        device_config = dpg.add_button(
            label="Device Config",
            tag="device_config_btn",
            pos=(0,),
        )

        with dpg.popup(
            parent=device_config,
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_device_config",
            no_move=True,
        ):

            dpg.add_menu(
                parent="modal_device_config",
                label="Choose Device: ",
                tag="choose_device",
            )

            try:
                # Grab the list of devices connected
                devices: list[str] = device_names()
                # print("DEVICE NAMES", device_names())

                [
                    dpg.add_menu_item(
                        parent="choose_device",
                        label=f"Device Number: {i}, {device}",
                        tag=f"device_menu_item_{i}",
                        callback=device_finder,
                        user_data=i,
                    )
                    for i, device in enumerate(devices)
                ]

                dpg.add_text(
                    parent="device_config",
                    tag="device_indicator",
                    default_value=f"Device:{devices}",
                    pos=(5, 35),
                )

            except (TypeError, NameError):
                dpg.add_menu_item(
                    parent="choose_device",
                    label=f"Device Number: Not Found",
                    callback=lambda: dpg.configure_item(
                        item="modal_device_config", show=False
                    ),
                )
                logger.exception(msg="No device detected")
                [
                    dpg.bind_item_theme(
                        item=f"stats_{channel}",
                        theme=red_btn_theme,
                    )
                    for channel in range(1, 9)
                ]

            dpg.add_button(
                label="Quit",
                tag="Quit",
                callback=lambda: dpg.configure_item(
                    item="modal_device_config", show=False
                ),
            )

    ################
    # Side buttons #
    ################
    with dpg.child_window(
        pos=(870, 0),
        tag="big_buttons",
        width=300,
        height=dpg.get_item_height(item="Primary Window") / 1.72,
        border=False,
    ):

        ####################
        # Reset All button #
        ####################
        reset_all = dpg.add_button(
            tag="Reset All Channels",
            height=70,
            width=BUTTON_WIDTH,
            callback=reset_button,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT) / 2,
            ),
        )
        dpg.add_text(
            default_value="RESET\nALL",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 40) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT) / 2,
            ),
            color=(0, 0, 0, 255),
        )

        ###################
        # Send All button #
        ###################
        send_all = dpg.add_button(
            tag="Send All",
            height=85,
            width=BUTTON_WIDTH,
            callback=send_all_channels,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 260) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT) / 2,
            ),
        )
        dpg.add_text(
            default_value="SEND\nALL",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 200) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT) / 2,
            ),
            color=(0, 0, 0, 255),
        )

        #####################
        # Quick Save button #
        #####################
        save_all = dpg.add_button(
            tag="save button",
            callback=quick_save,
            label="QUICK\n SAVE\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - QUICK_CONFIG_HEIGHT) / 2,
            ),
        )

        #####################
        # Quick Load button #
        #####################
        load_all = dpg.add_button(
            tag="load_all",
            callback=quick_load,
            label="QUICK\n LOAD\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - QUICK_CONFIG_HEIGHT) / 2,
            ),
        )

        ###############
        # Custom save #
        ###############
        custom_save_button = dpg.add_button(
            tag="custom_save",
            height=70,
            label="CUSTOM\nCONFIG\nSAVE",
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - CUSTOM_CONFIG_HEIGHT) / 2,
            ),
        )

        with dpg.popup(
            parent=custom_save_button,
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_save",
        ):
            dpg.add_input_text(
                label="Save Name: ",
                tag="save_custom_input",
            )
            dpg.add_button(
                label="Save",
                tag="save_button",
                callback=custom_save,
            )
            dpg.add_button(
                label="Quit",
                callback=lambda: dpg.configure_item(item="modal_save", show=False),
            )

        ###############
        # Custom load #
        ###############
        custom_load_button = dpg.add_button(
            tag="custom_load_button",
            height=70,
            width=BUTTON_WIDTH,
            label="CUSTOM\nCONFIG\nLOAD",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - CUSTOM_CONFIG_HEIGHT) / 2,
            ),
        )

        with dpg.popup(
            parent=custom_load_button,
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_load",
        ):
            dpg.add_menu(
                parent="modal_load",
                label="Load File: ",
                tag="load_input",
            )
            [
                dpg.add_menu_item(
                    parent="load_input",
                    label=f"Previously Saved custom named item {i}",
                    callback=lambda: logger.info(msg="\nMenu item called\n"),
                )
                for i in range(1, 9)
            ]

            dpg.add_button(
                label="Quit",
                callback=lambda: dpg.configure_item(item="modal_load", show=False),
            )

        ###############
        # DEMO 1 button #
        ###############
        demo_button = dpg.add_button(
            tag="demo",
            height=70,
            width=BUTTON_WIDTH,
            callback=demo_config,
            label="DEMO\nCONFIG",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + (DEMO_HEIGHT - 250)) / 2,
            ),
        )

        ###############
        # DEMO 2 button #
        ###############
        demo_two_button = dpg.add_button(
            tag="demo_two",
            height=70,
            width=BUTTON_WIDTH,
            callback=demo_config_2,
            label="DEMO\nTWO\nCONFIG",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + (DEMO_HEIGHT - 250)) / 2,
            ),
        )

        ########################
        # Mission Alpha button #
        ########################
        mission_alpha_button = dpg.add_button(
            tag="mssn_alpha",
            callback=mission_alpha,
            label="ALPHA\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + CELLUAR_HEIGHT) / 2,
            ),
        )

        ########################
        # Mission Bravo button #
        ########################
        mission_bravo_button = dpg.add_button(
            tag="mssn_bravo",
            callback=mission_bravo,
            label="BRAVO\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + CELLUAR_HEIGHT) / 2,
            ),
        )

        ##################
        # WIFI preset #
        ##################
        two_point_four_button = dpg.add_button(
            tag="two_point_four",
            callback=two_point_four,
            label="WIFI\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + WIFI_HEIGHT) / 2,
            ),
        )

        ##########################
        # Mission Charlie preset #
        ##########################
        mission_charlie_button = dpg.add_button(
            tag="mssn_charlie",
            callback=mission_charlie,
            label="CHARLIE\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + WIFI_HEIGHT) / 2,
            ),
        )
        ########################
        # Mission Delta preset #
        ########################
        mission_delta_button = dpg.add_button(
            tag="mssn_delta",
            callback=mission_delta,
            label="DELTA\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 50) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - 80),
            ),
        )
        #######################
        # Mission Echo preset #
        #######################
        mission_echo_button = dpg.add_button(
            tag="mssn_echo",
            # callback=mission_charlie,
            label="ECHO\nCONFIG",
            height=70,
            width=BUTTON_WIDTH,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - 80),
            ),
        )

    ###############
    # Version Tag #
    ###############
    with dpg.child_window(
        tag="version",
        height=15,
        width=70,
        border=False,
        no_scrollbar=True,
        pos=(
            RESOLUTION[0] - 65,
            RESOLUTION[1] - 30,
        ),
    ):
        dpg.add_text(
            default_value="ver. 0.9.0",
            tag="ver_num",
        )

dpg.bind_font(font=ital_font)
dpg.bind_item_font(item="ver_num", font=small_font)
# dpg.bind_item_font(item="")
[
    (
        dpg.bind_item_font(item=f"freq_{i}", font=bold_font),
        dpg.bind_item_font(item=f"power_{i}", font=bold_font),
        dpg.bind_item_font(item=f"bandwidth_{i}", font=bold_font),
        dpg.bind_item_font(item=f"channel_{i}", font=default_font_added),
    )
    for i in range(1, 9)
]

# Global Theme
with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )

    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
        )

# Button colors and global theme
blue_btn_list: list[Any] = [
    save_all,
    load_all,
    custom_save_button,
    two_point_four_button,
    mission_alpha_button,
    custom_load_button,
    mission_bravo_button,
    mission_charlie_button,
    mission_delta_button,
    mission_echo_button,
    demo_button,
    demo_two_button,
]

dpg.bind_theme(global_theme)

[
    dpg.bind_item_theme(
        item=btn,
        theme=blue_btn_theme,
    )
    for btn in blue_btn_list
]
dpg.bind_item_theme(item=send_all, theme=grn_btn_theme)
dpg.bind_item_theme(item=reset_all, theme=red_btn_theme)


############################
# DearPyGUI required setup #
############################
TM = "\U00002122"
dpg.create_viewport(
    title=f"CellAntenna MGTron {TM}",
    width=RESOLUTION[0],
    height=RESOLUTION[1],
    resizable=False,
    always_on_top=True,
    x_pos=0,
    y_pos=0,
)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=False)
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
