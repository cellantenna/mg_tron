from typing import List
import dearpygui.dearpygui as dpg
from interface import Megatron

data_vehicle = Megatron()
RESOLUTION: List[int] = [1200, 800]  # 1200x800

dpg.create_context()


def callstack(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class"""

    match user_data:
        case 1:
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
    ital_font = dpg.add_font(file="MesloLGS NF Italic.ttf", size=16)
    bold_font = dpg.add_font(file="MesloLGS NF Bold Italic.ttf", size=22)


with dpg.window(label="MGTron Control", tag="Primary Window", height=RESOLUTION[0], width=RESOLUTION[1], pos=(0, 0)):

    for i in range(8):

        with dpg.child_window(label=f"Channel {i+1}",
                              tag=f"channel_{i+1}",
                              pos=(0, 98*i),
                              width=(700)
                              ):
            slide_frequency = dpg.add_slider_float(
                label="Frequency Range (50 - 6400 MHz)",
                tag=f"freq_{i+1}",
                default_value=50.000,
                min_value=50,
                max_value=6400,
                clamped=True,
                width=455,
            )
            slide_power = dpg.add_slider_int(
                label="Power Level (0 - 63)",
                tag=f"power_{i+1}",
                min_value=0,
                max_value=63,
                clamped=True,

            )
            slide_bandwidth = dpg.add_slider_int(
                label="Bandwidth Level (0 - 100%)",
                tag=f"bandwidth_{i+1}",
                min_value=0,
                max_value=100,
                clamped=True,

            )

        with dpg.child_window(pos=(700, 98*i), width=(250)):
            dpg.add_color_button(default_value=(115, 60, 199, 100),
                                 label="Colored Button",
                                 height=50,
                                 width=50,
                                 callback=callstack,
                                 user_data=i+1,
                                 )
            dpg.add_text(default_value="SEND", pos=(17, 23))

    with dpg.child_window(pos=(950, ), width=250, height=250):
        rst = dpg.add_color_button(default_value=(200, 55, 0, 100),
                                   label="Reset All Channels",
                                   height=150,
                                   width=230,
                                   callback=reset_button,
                                   )
        dpg.add_text(default_value="RESET ALL", pos=(85, 69))

    with dpg.child_window(pos=(950, 249), width=250, height=250):
        toggle = dpg.add_color_button(default_value=(100, 155, 0, 100),
                                      label="Toggle All Off",
                                      height=150,
                                      width=230,
                                      callback=toggle_off,
                                      )
        dpg.add_text(default_value="TOGGLE ALL OFF", pos=(70, 69))

    with dpg.child_window(pos=(950, 498), width=250, height=250):
        send_all = dpg.add_color_button(default_value=(100, 0, 0, 100),
                                        label="Send All",
                                        height=150,
                                        width=230,
                                        callback=toggle_off,
                                        )
        dpg.add_text(default_value="SEND ALL", pos=(89, 69))
    dpg.bind_font(font=ital_font)
    dpg.bind_item_font(item=toggle, font=bold_font)


with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,
                            5, category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvInputInt):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (140, 255, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,
                            5, category=dpg.mvThemeCat_Core)

# dpg.show_font_manager()
dpg.bind_theme(global_theme)

dpg.create_viewport(
    title='MGTron Command Interface',
    width=RESOLUTION[0], height=RESOLUTION[1],
    resizable=True,
    always_on_top=False,
    x_pos=0,
    y_pos=0,
)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
