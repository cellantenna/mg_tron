from typing import List
import dearpygui.dearpygui as dpg
from interface import Megatron

data_vehicle: Megatron = Megatron()
RESOLUTION: List[int] = [1250, 735]  # 1200x800
POWER: bool = bool()
ROW_HEIGHT: int = 78
ADJUSTMENT: int = 40

dpg.create_context()


def callstack(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class"""

    match user_data:
        case 1:
            global POWER
            POWER = True
            print("Channel 1 information")
            data_vehicle.change_power(1, dpg.get_value("power_1"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_1"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_1"))
        case 2:
            print("Channel 2 information")
            data_vehicle.change_power(1, dpg.get_value("power_2"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_2"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_2"))
        case 3:
            print("Channel 3 information")
            data_vehicle.change_power(1, dpg.get_value("power_3"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_3"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_3"))
        case 4:
            print("Channel 4 information")
            data_vehicle.change_power(1, dpg.get_value("power_4"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_4"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_4"))
        case 5:
            print("Channel 5 information")
            data_vehicle.change_power(1, dpg.get_value("power_5"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_5"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_5"))
        case 6:
            print("Channel 6 information")
            data_vehicle.change_power(1, dpg.get_value("power_6"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_6"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_6"))
        case 7:
            print("Channel 7 information")
            data_vehicle.change_power(1, dpg.get_value("power_7"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_7"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_7"))
        case 8:
            print("Channel 8 information")
            data_vehicle.change_power(1, dpg.get_value("power_8"))
            data_vehicle.change_bandwidth(1, dpg.get_value("bandwidth_8"))
            data_vehicle.change_frequency(1, dpg.get_value("freq_8"))
        case _:
            print(f"Unrecognized GUI report of a channel: \n")
            print(
                f"Sender: {sender}\n"
                f"App data: {app_data}\n"
                f"User data: {user_data}\n"
            )


def reset_button(sender, app_data, user_data) -> None:
    """Reset all channel power levels to zero"""

    data_vehicle.save_state(state=True)
    data_vehicle.reset_board()


def toggle_off(sender, app_data, user_data) -> None:
    """Turn all power levels to zero"""

    [data_vehicle.change_power(i+1, 0) for i in range(8)]


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

    for i in range(8):

        # Header Column Channel
        with dpg.child_window(pos=(0,),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT-ADJUSTMENT,
                              ):
            dpg.add_text(default_value=f"Channel", pos=(42, 39-ADJUSTMENT+5))

        # Right Header Column Channel
        with dpg.child_window(pos=(700,),  # (x, y)
                              width=250,
                              height=ROW_HEIGHT-ADJUSTMENT,
                              ):
            dpg.add_text(default_value=f"Channel Status",
                         pos=(60, 39-ADJUSTMENT+5))

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

        # Header Column Power
        with dpg.child_window(pos=(450,),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT-ADJUSTMENT,
                              ):
            dpg.add_text(default_value=f"Bandwidth", pos=(40, 39-ADJUSTMENT+5))

        # First Column
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(0, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_text(default_value=i+1,
                         tag=f"channel_{i}", pos=(70, ROW_HEIGHT/2-15))

        # Frequency Column
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(150, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_input_float(tag=f"freq_{i+1}",
                                default_value=50.000,
                                min_value=50,
                                max_value=6400,
                                width=125,
                                )
        # Power Column
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(300, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_input_int(tag=f"power_{i+1}",
                              min_value=0,
                              max_value=63,
                              width=125,
                              )
        # Bandwidth Channel
        with dpg.child_window(label=f"Channel {i+1}",
                              pos=(450, ROW_HEIGHT*(i+1)-ADJUSTMENT),  # (x, y)
                              width=150,
                              height=ROW_HEIGHT,
                              ):
            dpg.add_input_int(tag=f"bandwidth_{i+1}",
                              min_value=0,
                              max_value=100,
                              width=125,
                              )
        # Send Button Column
        with dpg.child_window(pos=(700, ROW_HEIGHT*(i+1)-ADJUSTMENT),
                              width=(250), height=ROW_HEIGHT,
                              ):

            colored_btn = dpg.add_color_button(default_value=(0, 0, 199, 255),
                                               label="Colored Button",
                                               tag=f"colored_btn_{i+1}",
                                               height=50,
                                               width=50,
                                               callback=callstack,
                                               user_data=i+1,
                                               )
            dpg.add_text(default_value="SEND", pos=(14, 20))
            dpg.add_text(default_value=i+1, pos=(134, 5))

            # Status Buttons
            if POWER:
                dpg.add_color_button(default_value=(0, 255, 0, 255),
                                     tag=f"stats_{i+1}",
                                     width=90,
                                     height=30,
                                     pos=(90, 30),
                                     enabled=False,
                                     no_border=True,
                                     )
            else:
                dpg.add_color_button(default_value=(105, 105, 105, 255),
                                     tag=f"stats_{i+1}",
                                     width=90,
                                     height=30,
                                     pos=(90, 30),
                                     enabled=False,
                                     no_border=True,
                                     )

    # Big Buttons
    with dpg.child_window(pos=(975, ROW_HEIGHT-ADJUSTMENT),
                          width=250,
                          autosize_y=True,

                          border=False,
                          ):

        # Reset All Channels big button
        dpg.add_color_button(default_value=(255, 0, 0, 255),  # RED
                             label="Reset All Channels",
                             height=150,
                             width=220,
                             callback=reset_button,
                             pos=(10, 10),
                             )
        dpg.add_text(default_value="RESET ALL",
                     pos=(70, 70), color=(0, 0, 0, 255))

        # Toggle All Off big button
        dpg.add_color_button(default_value=(255, 0, 0, 255),  # RED
                             label="Toggle All Off",
                             height=150,
                             width=220,
                             callback=toggle_off,
                             pos=(10, 256),
                             )
        dpg.add_text(default_value="TOGGLE ALL OFF",
                     pos=(55, 315), color=(0, 0, 0, 255))

        # Send All big button
        dpg.add_color_button(default_value=(0, 255, 0, 255),  # GREEN
                             label="Send All",
                             height=150,
                             width=220,
                             callback=toggle_off,
                             pos=(10, 503)
                             )
        dpg.add_text(default_value="SEND ALL", pos=(
            74, 569), color=(0, 0, 0, 255))

    with dpg.tooltip(colored_btn, show=False):
        pass

    dpg.bind_font(font=ital_font)


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
