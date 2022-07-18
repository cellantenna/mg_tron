#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pathlib
from typing import Any

import dearpygui.dearpygui as dpg


from helpers import (
    DEVICE,
    VERSION,
    auto_fill_bandwidth,
    auto_fill_freq,
    auto_fill_power,
    card_selection,
    change_inputs,
    config_intake,
    custom_load,
    data_vehicle,
    delete_chosen,
    device_finder,
    device_refresh,
    fill_config,
    kill_channel,
    load_chosen,
    mission_alpha,
    mission_bravo,
    mission_charlie,
    mission_delta,
    mission_echo,
    mission_fox,
    mission_golf,
    neighborhood_list,
    quick_load,
    refresh_save_data,
    reset_button,
    quick_save,
    send_all_channels,
    send_vals,
    custom_save,
    wifi_scan_jam,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

logger = logging.getLogger(name=__name__)

logger.debug(msg=f"Working dir: {ROOT}")

logger.info(msg=f"Imports imported in GUI file")
RESOLUTION: list[int] = [1250, 735]  # 1200x800
POWER: bool = bool()
ROW_HEIGHT: int = 78
ADJUSTMENT: int = -25
DIVISOR: int = 1.5
SEND_RESET_ALL_HEIGHT: int = 695
CUSTOM_CONFIG_HEIGHT: int = 300
QUICK_CONFIG_HEIGHT: int = 480
DEMO_HEIGHT: int = -470
WIFI_HEIGHT: int = -400
CELLUAR_HEIGHT: int = -560
MAIN_TABLE_HEIGHT: int = 1
BUTTON_WIDTH = 120

dpg.create_context()
logger.info(msg="creating dpg context")

logger.info(msg="Set save state of MGTron API to True")
data_vehicle.save_state(True)
fill_config()

logger.info(msg="Setting GUI colors")
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

# White Button Theme
with dpg.theme() as wht_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (255, 255, 255, 255))  # WHITE

# Grey Column Theme
with dpg.theme() as grey_column_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (185, 185, 185, 255))  # WHITE
logger.info(msg="GUI colors set")

with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=change_inputs)
    dpg.add_key_down_handler(key=dpg.mvKey_Return, callback=custom_save)

with dpg.font_registry():
    try:  # Stop gap incase the files cannot be found
        default_font_added = dpg.add_font(
            file=f"{ROOT}/src/gui/fonts/MesloLGS NF Regular.ttf", size=40)
        ital_font = dpg.add_font(
            file=f"{ROOT}/src/gui/fonts/MesloLGS NF Italic.ttf", size=20)
        bold_font = dpg.add_font(
            file=f"{ROOT}/src/gui/fonts/MesloLGS NF Bold Italic.ttf", size=40)
        small_font = dpg.add_font(
            file=f"{ROOT}/src/gui/fonts/MesloLGS NF Italic.ttf", size=13)
    except SystemError:
        logger.exception(msg="Unable to locate font files")

logger.info(msg="Setting Primary Window in GUI file")
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
        dpg.add_text(default_value=f"Frequency: 6.4GHz",
                     pos=(9, 39 - ADJUSTMENT + 5))

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
                step_fast=100,
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
        height=100,
    ):

        device_config = dpg.add_button(
            label="Device Config",
            tag="device_config_btn",
            pos=(0,),
        )

        # Add refresh button
        dpg.add_button(
            parent="device_config",
            label="Refresh",
            tag="refresh_devices",
            callback=device_refresh,
            # user_data="refresh",
            pos=(
                0,
                70
            ),
        )

        with dpg.popup(
            parent=device_config,
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_device_config",
            no_move=True,
        ):

            try:
                # Grab the list of devices connected
                devices: list[str] = DEVICE

                if len(devices) == 1 and devices[0]:

                    dpg.add_menu_item(
                        label=f"{devices[0].split(sep='_')[0]} {devices[0].split(sep='_')[-1]}",
                    )

                elif len(devices) > 1:
                    {
                        dpg.add_menu_item(
                            label=f"{device.split(sep='_')[0]} {device.split(sep='_')[-1]}",
                            callback=device_finder,
                            user_data=int(
                                device.split(sep="_")[0][11:12]
                            ) if device.split(sep="_")[0][11:12] else None,
                            # Grab the integer at the end of `/dev/ttyACM[0:]`
                        )
                        for device in devices
                    }
                else:
                    assert devices[0] == False

                dpg.add_text(
                    parent="device_config",
                    tag="device_indicator",
                    default_value=f"Device:{devices[0].split(sep='_')[-1]}",
                    pos=(5, 35),
                )

            except (TypeError, NameError, SystemError, AssertionError, ValueError):
                dpg.add_menu_item(
                    parent="choose_device",
                    label="Device Number: Not Found",
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
                dpg.add_text(
                    parent="device_config",
                    tag="device_indicator",
                    default_value="",
                    pos=(5, 35),
                )

    ################
    # Side buttons #
    ################
    with dpg.child_window(
        pos=(860, 0),
        tag="big_buttons",
        width=290,
        height=dpg.get_item_height(item="Primary Window") / 1.72,
        no_scrollbar=True,
        border=False,
    ):

        ####################
        # Reset All button #
        ####################
        logger.info(msg="RESET ALL button initialized")
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
        logger.info(msg="SEND ALL button initialized")
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
        logger.info(msg="Quick save button initialized")
        save_all = dpg.add_button(
            tag="save button",
            callback=quick_save,
            label="QUICK\n SAVE",
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
        logger.info(msg="Quick Load button initialized")
        load_all = dpg.add_button(
            tag="load_all",
            callback=quick_load,
            label="QUICK\n LOAD",
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
        logger.info(msg="Custom Save button initialized")
        custom_save_button = dpg.add_button(
            tag="custom_save",
            height=70,
            label="SAVE\nCONFIG",
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

        ###############
        # Custom load #
        ###############
        logger.info(msg="Custom Load button initialized")
        custom_load_button = dpg.add_button(
            tag="custom_load_button",
            height=70,
            width=BUTTON_WIDTH,
            label="LOAD\nCONFIG",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 250) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") - CUSTOM_CONFIG_HEIGHT) / 2,
            ),
        )

        # Add refresh button
        dpg.add_button(
            parent="big_buttons",
            label="Refresh",
            tag="refresh_button",
            callback=refresh_save_data,
            # user_data="refresh",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 220) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + (330 - 480)) / 2,
            ),
        )

        SAVED_LIST: list[dict[str]] = custom_load()
        with dpg.popup(
            parent=custom_load_button,
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_load",
        ):
            SAVED_LIST: list[dict[str]] = custom_load()
            try:

                unique_names: list = list(
                    set(save["save_name"] for save in SAVED_LIST))

                logger.debug(msg="Custom load options loaded")
                {
                    dpg.add_menu_item(
                        parent="modal_load",
                        label=unique,
                        callback=load_chosen,
                        user_data=(unique, l),
                        tag=f"load_{l}",
                    )
                    for l, unique in enumerate(unique_names)
                }
            except (KeyError, TypeError):
                logger.exception(msg="Save file corrupted")

        ############################
        # Delete Saved Item button #
        ############################
        delete_button = dpg.add_button(
            parent="big_buttons",
            label="Delete",
            tag="delete_button",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 10) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + (330 - 480)) / 2,
            ),
        )

        with dpg.popup(
            parent=delete_button,
            mousebutton=dpg.mvMouseButton_Left,
            modal=True,
            tag="modal_delete",
        ):
            try:
                SAVED_LIST: list[dict[str]] = custom_load()

                unique_names: list[str] = list(
                    set(
                        save["save_name"] for save in SAVED_LIST
                    )
                )

                logger.debug(msg="Custom load options loaded")
                {
                    dpg.add_menu_item(
                        parent="modal_delete",
                        label=unique,
                        callback=delete_chosen,
                        user_data=(unique, l),
                        tag=f"delete_{l}",
                        show=True,
                    )
                    for l, unique in enumerate(unique_names)
                }
            except (KeyError, TypeError):
                logger.exception(msg="Save file corrupted")

        ####################
        # MISSIONS SECTION #
        ####################
        dpg.add_text(
            default_value="MISSIONS",
            pos=(
                (dpg.get_item_width(item="big_buttons") - 120) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + (330 - 320)) / 2,
            ),
        )

        ##########################
        # Mission buttons border #
        ##########################
        with dpg.child_window(
            border=True,
            tag="mission_buttons_border",
            height=330,
            width=BUTTON_WIDTH * 2 + 23,
            no_scrollbar=True,
            pos=(
                (dpg.get_item_width(item="big_buttons") - 255) / DIVISOR,
                (dpg.get_item_height(item="big_buttons") + (330 - 270)) / 2,
            ),
        ):

            ########################
            # Mission Alpha button #
            ########################
            logger.info(msg="Alpha button initialized")
            mission_alpha_button = dpg.add_button(
                tag="Alpha\nConfig",
                height=70,
                width=BUTTON_WIDTH,
                callback=mission_alpha,
                label="ALPHA\n",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + (DEMO_HEIGHT - 250)) / 2,
                ),
            )

            ########################
            # Mission Bravo button #
            ########################
            logger.info(msg="Bravo button initialized")
            mission_bravo_button = dpg.add_button(
                tag="Bravo\nConfig",
                height=70,
                width=BUTTON_WIDTH,
                callback=mission_bravo,
                label="BRAVO\n",
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + (DEMO_HEIGHT - 250)) / 2,
                ),
            )

            ##########################
            # Mission Charlie button #
            ##########################
            logger.info(msg="Mission Charlie button initialized")
            mission_charlie_button = dpg.add_button(
                tag="mssn_charlie",
                callback=mission_charlie,
                label="CHARLIE\n",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + CELLUAR_HEIGHT) / 2,
                ),
            )

            ########################
            # Mission Delta button #
            ########################
            logger.info(msg="Mission Delta button initialized")
            mission_delta_button = dpg.add_button(
                tag="mssn_delta",
                callback=mission_delta,
                label="DELTA\n",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + CELLUAR_HEIGHT) / 2,
                ),
            )

            #######################
            # Mission Echo button #
            #######################
            logger.info(msg="Mission Echo button initialized")
            mission_echo_button = dpg.add_button(
                tag="mssn_echo",
                callback=mission_echo,
                label="ECHO\n",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + WIFI_HEIGHT) / 2,
                ),
            )

            ##########################
            # Mission Fox preset #
            ##########################
            logger.info(msg="Mission Fox button initialized")
            mission_fox_button = dpg.add_button(
                tag="mssn_fox",
                callback=mission_fox,
                label="FOX\n",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") + WIFI_HEIGHT) / 2,
                ),
            )

            #######################
            # Mission Golf preset #
            #######################
            logger.info(msg="Mission Golf button initialized")
            mission_golf_button = dpg.add_button(
                tag="mssn_golf",
                callback=neighborhood_list,
                label="NEIGHBORHOOD\n    LIST",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 285) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - 480),
                ),
            )

            ################################
            # Mission Wifi Scan Jam preset #
            ################################
            logger.info(msg="Mission WiFi scan jam button initialized")
            wifi_scan_jam_button = dpg.add_button(
                tag="mssn_scan_jam",
                callback=wifi_scan_jam,
                label="WiFi\nScan\nJam",
                height=70,
                width=BUTTON_WIDTH,
                pos=(
                    (dpg.get_item_width(item="big_buttons") - 85) / DIVISOR,
                    (dpg.get_item_height(item="big_buttons") - 480),
                ),
            )

    ##########################
    # Card Selection Buttons #
    ##########################
    with dpg.child_window(
        tag="card_presets",
        height=RESOLUTION[1] - 50,
        width=70,
        pos=(
            RESOLUTION[0] - 86,
            10,
        ),
        border=False,
    ):

        [
            (
                dpg.add_button(
                    label=f"Card {card}",
                    tag=f"card_{card}",
                    height=60,
                    width=65,
                    pos=(0, 85 * card - 72),
                    callback=card_selection,
                    user_data=card,
                    enabled=False,
                ),
                # dpg.bind_item_theme(item=f"card_{card}", theme=grey_btn_theme),
            )
            for card in range(1, 9)
        ]

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
            RESOLUTION[0] - 80,
            RESOLUTION[1] - 30,
        ),
    ):

        dpg.add_text(
            default_value=f"ver. {VERSION}",
            tag="ver_num",
        )

try:  # Stop gap in case the font files cannot be found
    dpg.bind_font(font=ital_font)
    dpg.bind_item_font(item="ver_num", font=small_font)

    [
        (
            dpg.bind_item_font(item=f"freq_{i}", font=bold_font),
            dpg.bind_item_font(item=f"power_{i}", font=bold_font),
            dpg.bind_item_font(item=f"bandwidth_{i}", font=bold_font),
            dpg.bind_item_font(item=f"channel_{i}", font=default_font_added),
        )
        for i in range(1, 9)
    ]

except NameError:
    logger.exception(msg="Font files error")

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
    mission_golf_button,
    mission_alpha_button,
    custom_load_button,
    mission_bravo_button,
    mission_charlie_button,
    mission_delta_button,
    mission_echo_button,
    mission_fox_button,
    wifi_scan_jam_button,
]
config_intake()

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
    resizable=True,
    always_on_top=True,
    x_pos=0,
    y_pos=0,
    small_icon="network_wireless.ico",
    large_icon="network_wireless.ico",
)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=False)
dpg.set_primary_window(window="Primary Window", value=True)
try:
    dpg.start_dearpygui()
except KeyboardInterrupt:
    logger.exception(msg="Ctrl C executed")
    exit  # Exit the program gracefully upon user input to quit
dpg.destroy_context()
