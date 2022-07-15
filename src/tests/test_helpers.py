from sre_constants import ASSERT_NOT
from xml.etree.ElementPath import find

from numpy import isin
from gui.helpers import kill_channel
import dearpygui.dearpygui as dpg

from gui.helpers import find_signals_and_frequencies
from neighborhood_list import E_UTRA

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
    assert 2412 in find_signals_and_frequencies()

def test_frequency_value2():
    assert 2437 in find_signals_and_frequencies()

def test_signal_string():
    assert "MHz" not in find_signals_and_frequencies()
print(find_signals_and_frequencies())

def test_earfcn_value():
    assert 1980.0 == E_UTRA.convert_to_frequency(1100)

for i in range(0,600):
    def test_earfcn_is_in_band_range_1():
        assert i in E_UTRA.band_ranges().get('1')

for j in range(600, 1200):
    def test_earfcn_is_in_band_range_2():
        assert j in E_UTRA.band_ranges().get('2')

for k in range(1200, 1950):
    def test_earfcn_is_in_band_range_3():
        assert k in E_UTRA.band_ranges().get('3')

for q in range(1950, 2400):
    def test_earfcn_is_in_band_range_4():
        assert q in E_UTRA.band_ranges().get('4')


