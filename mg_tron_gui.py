#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any

import dearpygui.dearpygui as dpg

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
    mission_alpha,
    mission_bravo,
    mission_charlie,
    quick_load,
    reset_button,
    quick_save,
    send_all_channels,
    send_vals,
    custom_save,
    two_point_four,
)

RESOLUTION: list[int] = [1250, 735]  # 1200x800
POWER: bool = bool()
ROW_HEIGHT: int = 78
ADJUSTMENT: int = 40
DIVISOR: int = 1.4
SEND_RESET_ALL_HEIGHT: int = 695
CUSTOM_CONFIG_HEIGHT: int = 300
QUICK_CONFIG_HEIGHT: int = 480
DEMO_HEIGHT: int = 330
WIFI_HEIGHT: int = 405
CELLUAR_HEIGHT: int = 240

dpg.create_context()


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
    default_font_added = dpg.add_font(file="MesloLGS NF Regular.ttf", size=40)
    ital_font = dpg.add_font(file="MesloLGS NF Italic.ttf", size=20)
    bold_font = dpg.add_font(file="MesloLGS NF Bold Italic.ttf", size=22)

# Primary Window
with dpg.window(
    label="MGTron Control",
    tag="Primary Window",
    height=RESOLUTION[0],
    width=RESOLUTION[1],
    pos=(0, 0),
):

    # Header Column Channel
    with dpg.child_window(
        pos=(0,),  # (x, y)
        width=50,
        height=ROW_HEIGHT - ADJUSTMENT,
    ):
        dpg.add_text(default_value=f"CH", pos=(19, 39 - ADJUSTMENT + 5))

    # Header Column Frequency
    with dpg.child_window(
        pos=(50,),  # (x, y)
        width=150,
        height=ROW_HEIGHT - ADJUSTMENT,
    ):
        dpg.add_text(default_value=f"Freq.: 6.4GHz", pos=(5, 39 - ADJUSTMENT + 5))

    # Header Column Power
    with dpg.child_window(
        pos=(200,),  # (x, y)
        width=150,
        tag="col_pwr",
        height=ROW_HEIGHT - ADJUSTMENT,
    ):
        dpg.add_text(
            default_value=f"Power: 63",
            pos=(dpg.get_item_width("col_pwr") / 4, 39 - ADJUSTMENT + 5),
        )

    # Header Column Bandwidth
    with dpg.child_window(
        pos=(350,),  # (x, y)
        tag="col_bw",
        width=150,
        height=ROW_HEIGHT - ADJUSTMENT,
    ):
        dpg.add_text(
            default_value=f"BW: 100%",
            pos=(dpg.get_item_width(item="col_bw") / 3.7, 39 - ADJUSTMENT + 5),
        )

    # Right Header Column Channel Status
    with dpg.child_window(
        pos=(500,),  # (x, y)
        width=250,
        height=ROW_HEIGHT - ADJUSTMENT,
    ):
        dpg.add_text(default_value=f"Channel Status", pos=(60, 39 - ADJUSTMENT + 5))

    ####################################
    # Column buttons, inputs, and text #
    ####################################
    for i in range(8):

        # First Column
        with dpg.child_window(
            tag=f"row_{i+1}",
            pos=(0, ROW_HEIGHT * (i + 1) - ADJUSTMENT),  # (x, y)
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
            pos=(50, ROW_HEIGHT * (i + 1) - ADJUSTMENT),  # (x, y)
            width=150,
            height=ROW_HEIGHT,
        ):
            dpg.add_input_float(
                tag=f"freq_{i+1}",
                default_value=650.00 * ((i + 1)),
                min_value=50.00,
                max_value=6400.00,
                min_clamped=True,
                max_clamped=True,
                width=141,
                step=10,
                step_fast=20,
                pos=(2, ROW_HEIGHT / 2 - 15),
            )
        # Power Column Input
        with dpg.child_window(
            label=f"Channel {i+1}",
            pos=(200, ROW_HEIGHT * (i + 1) - ADJUSTMENT),  # (x, y)
            width=150,
            height=ROW_HEIGHT,
        ):
            dpg.add_input_int(
                tag=f"power_{i+1}",
                min_value=0,
                max_value=63,
                min_clamped=True,
                max_clamped=True,
                width=125,
                step_fast=3,
                pos=(13, ROW_HEIGHT / 2 - 15),
            )

        # Bandwidth Channel Input
        with dpg.child_window(
            label=f"Channel {i+1}",
            pos=(350, ROW_HEIGHT * (i + 1) - ADJUSTMENT),  # (x, y)
            width=150,
            height=ROW_HEIGHT,
        ):
            dpg.add_input_int(
                tag=f"bandwidth_{i+1}",
                min_value=0,
                max_value=100,
                min_clamped=True,
                max_clamped=True,
                width=125,
                step_fast=10,
                pos=(13, ROW_HEIGHT / 2 - 15),
            )
        # Send Button Column
        with dpg.child_window(
            pos=(500, ROW_HEIGHT * (i + 1) - ADJUSTMENT),
            width=(250),
            height=ROW_HEIGHT,
        ):
            # SEND Buttons
            dpg.add_button(
                label="SEND",
                tag=f"send_btn_{i+1}",
                height=50,
                width=50,
                callback=send_vals,
                user_data=i + 1,
                pos=(170, ROW_HEIGHT / 2 - 25),
            )

            # Status LED Buttons
            dpg.add_button(
                tag=f"stats_{i+1}",
                width=30,
                height=30,
                pos=(60, 30),
                enabled=True,
            )

            dpg.bind_item_theme(
                item=f"row_{i+1}",
                theme=grey_column_theme,
            )

    ########################
    # Auto Fill button row #
    ########################
    with dpg.child_window(
        pos=(50, ROW_HEIGHT * 9 - (ADJUSTMENT)),
        tag="auto_fill",
        height=65,
        width=150 * 3,
        border=False,
    ):
        dpg.add_button(
            label="AUTO\nFILL",
            tag="auto_fill_frequency",
            height=50,
            width=50,
            callback=auto_fill_freq,
            pos=(
                dpg.get_item_width(item="auto_fill") / 8,
                dpg.get_item_height(item="auto_fill") / 3 - 10,
            ),
        )
        dpg.add_button(
            label="AUTO\nFILL",
            tag="auto_fill_power",
            height=50,
            width=50,
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
            width=50,
            callback=auto_fill_bandwidth,
            pos=(
                dpg.get_item_width(item="auto_fill") / 1.3,
                dpg.get_item_height(item="auto_fill") / 3 - 10,
            ),
        )

    ################
    # Side buttons #
    ################
    with dpg.child_window(
        pos=(900, 0),
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
            width=70,
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
            height=70,
            width=70,
            callback=send_all_channels,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - SEND_RESET_ALL_HEIGHT) / 2,
            ),
        )
        dpg.add_text(
            default_value="SEND\nALL",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 240) / DIVISOR,
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
            width=70,
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
            width=70,
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
            width=70,
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
                # default_value=,
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
            width=70,
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
                    callback=lambda: print("\nMenu item called\n"),
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
            width=70,
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
            width=70,
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
            width=70,
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
            width=70,
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
            width=70,
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
            width=70,
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
            callback=mission_charlie,
            label="DELTA\nCONFIG",
            height=70,
            width=70,
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
            callback=mission_charlie,
            label="ECHO\nCONFIG",
            height=70,
            width=70,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - 80),
            ),
        )


dpg.bind_font(font=ital_font)
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

[
    (
        dpg.bind_item_theme(item=f"send_btn_{i+1}", theme=blue_btn_theme),
        dpg.bind_item_theme(item=f"stats_{i+1}", theme=grey_btn_theme),
    )
    for i in range(8)
]  # Propgation loop


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
