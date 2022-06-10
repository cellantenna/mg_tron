from typing import type_check_only
from gui.helpers import kill_channel
import dearpygui.dearpygui as dpg
from src.gui.helpers import find_signals_and_frequencies

def test_kill_channel() -> None:
    
    assert kill_channel.__name__


def test_wifi_scanner(): 
    
    assert isinstance(find_signals_and_frequencies(), dict)
