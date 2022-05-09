from typing import List

import dearpygui.dearpygui as dpg

from helpers import (callstack, change_inputs, reset_button, save_inputs,
                     send_all_channels, load_inputs, data_vehicle)

RESOLUTION: List[int] = [1250, 735]  # 1200x800
POWER: bool = bool()
ROW_HEIGHT: int = 78
ADJUSTMENT: int = 40

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
# White Button Theme
with dpg.theme() as wht_btn_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (255, 255, 255, 255))  # WHITE


with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=change_inputs)

with dpg.font_registry():
    default_font_added = dpg.add_font(file="MesloLGS NF Regular.ttf", size=16)
    ital_font = dpg.add_font(file="MesloLGS NF Italic.ttf", size=20)
    bold_font = dpg.add_font(file="MesloLGS NF Bold Italic.ttf", size=22)

# Primary Window
with dpg.window(label="MGTron Control",
                tag="Primary Window",
                height=RESOLUTION[0],
                width=RESOLUTION[1],
                pos=(0, 0),
                ):

    # Header Column Channel
    with dpg.child_window(pos=(0,),  # (x, y)
                          width=150,
                          height=ROW_HEIGHT-ADJUSTMENT,
                          ):
        dpg.add_text(default_value=f"Channel", pos=(42, 39-ADJUSTMENT+5))

    # Header Column Frequency
    with dpg.child_window(pos=(150,),  # (x, y)
                          width=150,
                          height=ROW_HEIGHT-ADJUSTMENT,
                          ):
        dpg.add_text(default_value=f"Frequency", pos=(37, 39-ADJUSTMENT+5))

    # Header Column Power
    with dpg.child_window(pos=(300,),  # (x, y)
                          width=150,
                          height=ROW_HEIGHT-ADJUSTMENT,
                          ):
        dpg.add_text(default_value=f"Power", pos=(48, 39-ADJUSTMENT+5))

    # Header Column Bandwidth
    with dpg.child_window(pos=(450,),  # (x, y)
                          width=150,
                          height=ROW_HEIGHT-ADJUSTMENT,
                          ):
        dpg.add_text(default_value=f"Bandwidth", pos=(40, 39-ADJUSTMENT+5))

    # Right Header Column Channel Status
    with dpg.child_window(pos=(600,),  # (x, y)
                          width=250,
                          height=ROW_HEIGHT-ADJUSTMENT,
                          ):
        dpg.add_text(default_value=f"Channel Status",
                     pos=(60, 39-ADJUSTMENT+5))

    for i in range(8):

        # First Column
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(0, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_text(default_value=i+1,
                         tag=f"channel_{i}", pos=(70, ROW_HEIGHT/2-15))

        # Frequency Column Input
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(150, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_input_float(tag=f"freq_{i+1}",
                                default_value=50.00,
                                min_value=50.00,
                                max_value=6400.00,
                                min_clamped=True,
                                max_clamped=True,
                                width=145,
                                step=0.01,
                                pos=(2, ROW_HEIGHT/2-15),
                                )
        # Power Column Input
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(300, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_input_int(tag=f"power_{i+1}",
                              min_value=0,
                              max_value=63,
                              min_clamped=True,
                              max_clamped=True,
                              width=125,
                              pos=(13, ROW_HEIGHT/2-15),
                              )
        # Bandwidth Channel Input
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(450, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_input_int(tag=f"bandwidth_{i+1}",
                              min_value=0,
                              max_value=100,
                              min_clamped=True,
                              max_clamped=True,
                              width=125,
                              pos=(13, ROW_HEIGHT/2-15),
                              )
        # Send Button Column
        with dpg.child_window(pos=(600, ROW_HEIGHT*(i+1)-ADJUSTMENT),
                              width=(250), height=ROW_HEIGHT,
                              ):
            # SEND Buttons
            dpg.add_button(label="SEND",
                           tag=f"send_btn_{i+1}",
                           height=50,
                           width=50,
                           callback=callstack,
                           user_data=i+1,
                           pos=(170, ROW_HEIGHT/2-25),
                           )

            # Status Buttons
            dpg.add_button(tag=f"stats_{i+1}",
                               width=30,
                               height=30,
                               pos=(60, 30),
                               enabled=True,
                           )

    # Big Buttons
    with dpg.child_window(pos=(975, ROW_HEIGHT-ADJUSTMENT),
                          width=250,
                          autosize_y=True,
                          border=False,
                          ):

        # Reset All Channels big button
        reset_all = dpg.add_button(tag="Reset All Channels",
                                   height=150,
                                   width=220,
                                   callback=reset_button,
                                   pos=(10, 10),
                                   )
        dpg.add_text(default_value="RESET ALL",
                     pos=(70, 65), color=(0, 0, 0, 255))

        # RESET All Off big button
        # reset_power = dpg.add_button(tag="Reset Power",
        #                              height=150,
        #                              width=220,
        #                              callback=toggle_off,
        #                              pos=(10, 256),
        #                              )
        # dpg.add_text(default_value="RESET ALL POWER",
        #              pos=(55, 320), color=(0, 0, 0, 255))

        # Send All big button
        send_all = dpg.add_button(tag="Send All",
                                  height=150,
                                  width=220,
                                  callback=send_all_channels,
                                  pos=(10, 503)
                                  )
        dpg.add_text(default_value="SEND ALL",
                     pos=(78, 569),
                     color=(0, 0, 0, 255),
                     )

    # Save buttons
    with dpg.child_window(pos=(900, dpg.get_item_height(item="Primary Window") / 4),
                          tag="save_window",
                          width=450,
                          height=100,
                          border=False,
                          ):
        save_all = dpg.add_button(tag="save button",
                                  callback=save_inputs,
                                  height=70,
                                  width=70,
                                  pos=((dpg.get_item_width(item="save_window")-50)/2,
                                       (dpg.get_item_height(item="save_window")-50)/2),
                                  )
        dpg.add_text(default_value="SAVE\nCONFIG",
                     pos=((dpg.get_item_width(item=save_all)+350)/2,
                          (dpg.get_item_height(item=save_all))/2),
                     color=(0, 0, 0, 255),
                     )

        load_all = dpg.add_button(tag="load_all",
                                  callback=load_inputs,
                                  height=70,
                                  width=70,
                                  pos=((dpg.get_item_width(item="save_window")-250)/2,
                                       (dpg.get_item_height(item="save_window")-50)/2),
                                  )
        dpg.add_text(default_value="LOAD\nCONFIG",
                     pos=((dpg.get_item_width(item=load_all)+150)/2,
                          (dpg.get_item_height(item=load_all))/2),
                     color=(0, 0, 0, 255),
                     )

dpg.bind_font(font=ital_font)

# Global Theme
with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,
                            5, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvInputInt):
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBg,(140, 255, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,
                            5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)
# Big Button Colors
dpg.bind_item_theme(send_all, grn_btn_theme)
# dpg.bind_item_theme(reset_power, red_btn_theme)  # Disabled due to redundancy
dpg.bind_item_theme(reset_all, red_btn_theme)
dpg.bind_item_theme(save_all, wht_btn_theme)
dpg.bind_item_theme(load_all, wht_btn_theme)
[
    (
        dpg.bind_item_theme(f"send_btn_{i+1}", blue_btn_theme),
        dpg.bind_item_theme(f"stats_{i+1}", grey_btn_theme),
    )
    for i in range(8)]  # Propgation loop

dpg.create_viewport(
    title='MGTron Command Interface',
    width=RESOLUTION[0], height=RESOLUTION[1],
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
