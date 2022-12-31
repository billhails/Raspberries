import time
import board
import displayio
import terminalio
import adafruit_il0398
import busio
from adafruit_display_text import label
import fortune

displayio.release_displays()


BLACK = 0x000000
RED = 0xFF0000
WHITE = 0xFFFFFF

FOREGROUND_COLOR = BLACK
BACKGROUND_COLOR = WHITE
HIGHLIGHT_COLOR = RED
DISPLAY_WIDTH = 296
DISPLAY_HEIGHT = 128

spi = busio.SPI(board.GP10, MOSI=board.GP11)  # Uses SCK and MOSI
epd_cs = board.GP9
epd_dc = board.GP8
epd_reset = board.GP12
epd_busy = board.GP13

display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=4_000_000
)

time.sleep(1)

display = adafruit_il0398.IL0398(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    seconds_per_frame=20,
    busy_pin=epd_busy,
    highlight_color=HIGHLIGHT_COLOR,
    rotation=90,
)

font = terminalio.FONT
CHARACTER_WIDTH = 6
CHARACTER_HEIGHT = 13

bitmap = displayio.Bitmap(296, 128, 1)

dark_palette = displayio.Palette(1)
dark_palette[0] = RED

light_palette = displayio.Palette(1)
light_palette[0] = WHITE

fortune_cookies = fortune.fortune(
    file="/fortunes", max_line_length=49, max_line_count=10
)

for count in range(5):
    text_color = 0
    palette = 0
    cookie = fortune_cookies.get()

    if len(cookie["author"]) > 0:
        text_color = BLACK
        palette = light_palette
    else:
        text_color = RED
        palette = light_palette

    group = displayio.Group()
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    group.append(tile_grid)
    total_height = len(cookie["body"]) + len(cookie["author"]) * 13
    y_offset = int((DISPLAY_HEIGHT - total_height) / 4)

    if y_offset < 4:
        y_offset = 4

    centering_group = displayio.Group(scale=1, x=1, y=y_offset)

    # Create the text labels
    for i in range(len(cookie["body"])):
        text_area = label.Label(font, text=cookie["body"][i], color=text_color)
        y_offset = i * CHARACTER_HEIGHT
        text_group = displayio.Group(scale=1, x=0, y=y_offset)
        text_group.append(text_area)
        centering_group.append(text_group)

    for i in range(len(cookie["author"])):
        text_area = label.Label(font, text=cookie["author"][i], color=RED)
        x_offset = (DISPLAY_WIDTH - 2) - len(cookie["author"][i]) * CHARACTER_WIDTH
        y_offset = (i + len(cookie["body"])) * CHARACTER_HEIGHT
        text_group = displayio.Group(scale=1, x=x_offset, y=y_offset)
        text_group.append(text_area)
        centering_group.append(text_group)

    group.append(centering_group)

    while display.busy:
        time.sleep(1)

    time.sleep(display.time_to_refresh)

    display.show(group)

    display.refresh()

    time.sleep(300)

