# CHANGELOG

Author: Hunter, Christerpher

All notable changes will be appended here.

This project, henceforth, will recongnize [semantic versioning](https://semver.org/).

## [⭐.✴️.✳️] - YEAR MONTH DAY

Here we write upgrade and change notes.

⭐ MAJOR version when you make incompatible API changes,

✴️ MINOR version when you add functionality in a backwards compatible manner

✳️ PATCH version when you make backwards compatible bug fixes.

## ✳️[0.12.1] - 2022 JUN 7

- Removed the `find_dev.sh` script completely and retained that functionality
- Critical error in `find_dev.sh`; linux device finding listing script
- All phonetic mission buttons are configurable via config files

## ✴️[0.12.0] - 2022 JUN 6

- The eight button on the right border correspond to up to eight cards
- Custom save configured and working

## ✴️[0.11.0] - 2022 JUN 3

- Scan and jam wifi automatically in RSSI order
- Added box around mission buttons

## ✳️[0.10.2] - 2022 JUN 3

- Automatically create config file and automatically populate config file
- Remove the word `CONFIG` from the buttons

## ✳️[0.10.1] - 2022 JUN 2

- Corrected multiple device bug
- Created an .ini config file and read contents
- Automatically fill in config if card_1 is not fillied in
- Changed name of all mission buttons
- Added `MISSIONS` above the mission buttons
- Card buttons turn blue if that number of cards are detected, disabled otherwise.

## ✴️[0.10.0] - 2022 JUN 1

- Added a set of buttons along the starboard side of the GUI
- New buttons highlight green when selected and grey when not
- When a device is chosen from the list the list promptly dissapears
- Added graceful exit

## ✳️[0.9.1] - 2022 MAY 31

- Device indicator reads no device detected if no device detected
- Fixed device listing bug
- Optimized scenario for if a single device detected

## ✴️[0.9.0] - 2022 MAY 25

- Now show device location and name
- Turn indicator buttons red if no device detected
- Add loggin to serial calls
- Connected devices are in numerical order

## ✳️[0.8.3] - 2022 MAY 25

- Added version number in bottom right of GUI

## ✳️[0.8.2] - 2022 MAY 24

- GUI will launch with no devices detected

## ✳️[0.8.1] - 2022 MAY 23

- Filling in list that holds all of the devices the GUI can access.

## ✴️[0.8.0] - 2022 MAY 23

- Changelog created.
- Project evolved enough to function and actuate hardware as expected.
