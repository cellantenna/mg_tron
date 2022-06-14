from sre_constants import ASSERT_NOT
from xml.etree.ElementPath import find

from numpy import isin
from gui.helpers import kill_channel
import dearpygui.dearpygui as dpg

from gui.helpers import find_signals_and_frequencies

def test_kill_channel() -> None:
    
    assert kill_channel.__name__


def test_wifi_scanner(): 
    assert isinstance(find_signals_and_frequencies(), dict)

def test_frequency_and_signal_value_exists():
    x = find_signals_and_frequencies()
    assert len(x) != 0, 'Dictionary should not be empty'


def test_frequency_for_string():
    assert "Infra" not in find_signals_and_frequencies()

def test_frequency_value():
    assert "2412" in find_signals_and_frequencies()

def test_frequency_value2():
    assert "2447" in find_signals_and_frequencies()
print(find_signals_and_frequencies())