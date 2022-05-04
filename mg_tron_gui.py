from typing import List
import dearpygui.dearpygui as dpg
from interface import Megatron

sender = Megatron()
RESOLUTION: List[int] = [1200, 800]  # 1200x800

dpg.create_context()


def callstack(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class"""

    # Create a function for each channel

    print(f"\nSender: {sender}\n"
          f"app_data: {app_data}\n"
          f"user_data:",
          {
              "Frequency": dpg.get_value(f'freq_{1}'),
              "Power": dpg.get_value(f'power_{1}'),
              "Bandwidth": dpg.get_value(f'bandwidth_{1}'),
          }
          )

    match sender:
        case 27:
            print("Channel 1 information")
            sender.change_power(1, dpg.get_value("power_1"))
            sender.change_bandwidth(1, dpg.get_value("bandwidth_1"))
            sender.change_frequency(1, dpg.get_value("freq_1"))
        case 33:
            print("Channel 2 information")
        case 39:
            print("Channel 3 information")
        case 45:
            print("Channel 4 information")
        case 51:
            print("Channel 5 information")
        case 57:
            print("Channel 6 information")
        case 63:
            print("Channel 7 information")
        case 69:
            print("Channel 8 information")


with dpg.window(label="MGTron Control", tag="Primary Window", height=RESOLUTION[0], width=RESOLUTION[1], pos=(0, 0)):

    for i in range(8):

        with dpg.child_window(label=f"Channel {i+1}", tag=f"channel_{i+1}", pos=(0, 98*i), width=(700)):
            slide_frequency = dpg.add_slider_float(
                label="Frequency Range (50 - 6400 MHz)",
                tag=f"freq_{i+1}",
                default_value=50.000,
                min_value=50,
                max_value=6400,
                clamped=True,
                width=455,
                payload_type="float",
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

        with dpg.child_window(pos=(700, 98*i), width=(500)):
            dpg.add_color_button(default_value=(115+3*i, 60+3*i, 199+2*i, 100),
                                 label="Colored Button",
                                 height=50,
                                 width=50,
                                 callback=callstack)


with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (255, 140, 23), category=dpg.mvThemeCat_Core)
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
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
