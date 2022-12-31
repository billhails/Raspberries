# SPDX-FileCopyrightText: 2019 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_il0398`
================================================================================

CircuitPython displayio drivers for IL0398 driven e-paper displays


* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython (5+) firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_IL0398.git"

# TODO: Try LUTs from:
# https://github.com/waveshare/e-Paper/blob/master/STM32/STM32-F103ZET6/User/e-Paper/EPD_4in2.c


def command(command, params, delay):
    result = [command, len(params) | (0x80 if delay else 0x00)]

    for param in params:
        result.append(param)

    if delay:
        result.append(delay)

    return bytearray(result)


_START_SEQUENCE = (
    # power on and wait 200 ms
    command(0x04, [], 200)
    +
    # Panel setting and Temperature sensor, boost and other related timing settings
    command(0x00, [0x8F, 0x89], 0)
    +
    # Resolution
    command(0x61, [0x80, 0x01, 0x28], 0)
    +
    # VCOM and data interval setting (WBRmode: VBDW)
    command(0x50, [0x77], 0)
)

_STOP_SEQUENCE = (
    # Power off and wait for 15 ms
    command(0x02, [], 15)
    +
    # Deep sleep
    command(0x07, [0xA5], 0)
)

# pylint: disable=too-few-public-methods
class IL0398(displayio.EPaperDisplay):
    """IL0398 driver"""

    def __init__(self, bus, **kwargs):
        width = kwargs["width"]
        height = kwargs["height"]
        if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
            width, height = height, width
        if "highlight_color" in kwargs:
            write_black_ram_command = 0x10
            write_color_ram_command = 0x13
        else:
            write_color_ram_command = 0x10
            write_black_ram_command = 0x13
        super().__init__(
            bus,
            _START_SEQUENCE,
            _STOP_SEQUENCE,
            **kwargs,
            ram_width=160,
            ram_height=296,
            busy_state=False,
            write_black_ram_command=write_black_ram_command,
            write_color_ram_command=write_color_ram_command,
            color_bits_inverted=True,
            refresh_display_command=0x12,
        )
