from ast import Str
from numpy import isin
import pytest
from interface import Megatron, serial_call 
def test_change_power(): 
    assert isinstance(Megatron.change_power(Megatron, 1, 30), object) 

def test_change_freq():
    assert isinstance(Megatron.change_freq(Megatron, 1, 1000), object) 

def test_change_bandwith(): 
    assert isinstance(Megatron.change_bandwidth(Megatron, 1, 45), object)