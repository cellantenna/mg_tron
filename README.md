# MGTron Signal Generator Interface

## A functional mutlti card interface for the MGTron Signal Generator

This project revolves around the MGTron signal generator.  The graphical user interface (GUI) is written purely in python.  There are some facets that utilize linux command line tools.  Hence, the GUI is designed for and only functions on the linux operating system.  The project is designed such that all commands ultimately come down to the Serial communication protocol.  Serial communication, via the  [pyserial](https://pyserial.readtodata.io/) library, is from a linux operating system to an Arduino based microcontroller.  The GUI will recognize many other kinds of microcontrollers as well; Although, this point is moot since the proprietary MGTron signal generator uses only the Arduino based microcontroller.  

* Set the frequency, power, and bandwidth of each of the eight channels.
* Send to all channels at once or individually.
* Easy one-click to turn off a generating channel.
* Choose a specific device based on its serial number.
* Easy install to most Linux distributions.
* Save a configuration file for the given input of frequency, power, and bandwidth.
* Pre-configurable configurations for up to eight devices.
* Phonetically names mission buttons.
* Pre-configurable mission buttons.
* Can set MGTron Signal Generator to auto resume on power up.
* Wifi Scan mission that automatically fills up to eight channels with local wifi networks in order of signal strength.

## Visualization
![mgtron_demo](https://user-images.githubusercontent.com/25860608/174464184-1511b551-a6ca-4b74-84f8-aeec5d31d9a4.gif)


## Installation

### Requirements

* Python 3.10+

### Easy install

    `pip install mgtron`

### Less Easy install

    `git clone https://github.com/cellantenna/mg_tron.git`
----------
    `cd mg_tron`
----------
    `pip install .`
