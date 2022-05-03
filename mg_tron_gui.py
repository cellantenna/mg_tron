from gc import callbacks
import dearpygui.dearpygui as dpg
from interface import Megatron

sender = Megatron()

def callstack(sender, app_data, user_data) -> None:
    """Relational connection between GUI and Megatron class"""

    print(f"\nSender: {sender}\n"
          f"app_data: {app_data}\n")




dpg.create_context()


with dpg.window(label="MGTron Control", tag="Primary Window", height=600, width=800):

    for i in range(8):
        with dpg.child_window(label=f"Channel {i}", tag=f"channel_{i}", pos=(0, 95*i)):
            dpg.add_text(f"Channel {i+1}")
            slide_frequency = dpg.add_slider_float(
                label="Frequency Range (50 - 6400 MHz)",
                tag=f"freq_{i+1}",
                min_value=50,
                max_value=6400,
                clamped=True)
            slide_power = dpg.add_slider_int(
                label="Power Level (0 - 63)",
                tag=f"power_{i+1}",
                min_value=0,
                max_value=63,
                clamped=True)
            slide_bandwidth = dpg.add_slider_int(
                label="Bandwidth Level (0 - 100%)",
                tag=f"bandwidth_{i+1}",
                min_value=0,
                max_value=100,
                clamped=True)

            dpg.add_button(
                label="Submit",
                small=False,
                callback=callstack,
                user_data=f"freq_{i}",
                pos=(173, 100),
                parent=f"channel_{i}"
                )


with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (255, 140, 23), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,
                            5, category=dpg.mvThemeCat_Core)


dpg.bind_theme(global_theme)


dpg.create_viewport(
    title='MGTron Command Interface',
    width=600, height=800,
    resizable=True,
    always_on_top=True,
)
dpg.setup_dearpygui()

dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
