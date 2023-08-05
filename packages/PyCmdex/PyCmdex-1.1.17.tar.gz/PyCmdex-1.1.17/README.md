# PyCmdex

## PyCmdex library

The PyCmdex is a Python library used to develop computer and microcontroller cooperation applications. It provides plentiful APIs for microcontroller interfacing. With this library, you can make computer-based control and monitoring application easier and faster.

## Supported Microcontroller

All of the microcontrollers running the Cmdex firmware can communicate to the PyCmdex through a serial port (UART). A USB-to-Serial adapter can be used. Note, the Cmdex firmware is a firmware of the microcontroller (not PyCmdex).

## Requirements

1) **Python 3.8** and **pip3** or higher.
2) The microcontroller board running the **Cmdex firmware**.
3) USB cable.

> The **Proteus** circuit simulator with Cmdex.hex can be used in the development process (no microcontroller board and USB cable are required).

## PyCmdex Installation using *pip3*

1) Uninstall the previous version

```
pip3 uninstall pycmdex
```

2) Install the latest version

```
pip3 install pycmdex
```

3) Checking and open the git repository

```
pycmdex web
```
