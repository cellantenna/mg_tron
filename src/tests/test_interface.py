from numpy import isin
import pytest
from interface import Megatron
def test_change_power(): 
    assert isinstance(Megatron.change_power(Megatron, 1, 39), object) 


def test_change_freqchan1():
    assert isinstance(Megatron.change_freq(Megatron, 1, 1000), object) 


def test_change_bandwithchannel1(): 
    assert isinstance(Megatron.change_bandwidth(Megatron, 1, 45), object)


def test_change_bandwithallchannels():
    for i in range(1,8):
            assert isinstance(Megatron.change_bandwidth(Megatron, i, 30), object)

        
def test_change_allfreqallchannels(): 
    for i in range(1,8):
        for x in range(63):
            assert isinstance(Megatron.change_freq(Megatron, i, x), object)


def test_change_powerallchannels():
    for i in range(1,8):
        assert isinstance(Megatron.change_power(Megatron, i, 42), object)