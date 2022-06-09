from sre_constants import ASSERT_NOT

from numpy import isin
from gui.helpers import kill_channel
import dearpygui.dearpygui as dpg
from gui.helpers import find_signals_and_frequencies

def test_kill_channel() -> None:
    
    assert kill_channel.__name__


def test_wifi_scanner(): 
    x = find_signals_and_frequencies()
    assert isinstance(find_signals_and_frequencies(), dict)


def test_frequency_dict_for_string():

    val = "Infra"
    if val in find_signals_and_frequencies(): 
        assert isinstance(find_signals_and_frequencies(), list)
