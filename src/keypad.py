from pad4pi import rpi_gpio
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

# BCM not GPIO dont fuck up pinout
ROW_PINS = [4, 17, 27, 22]
COL_PINS = [5, 6, 13]

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
def printKey(key):
    print(key)

# register key handler - later replace this with comparing against the predefined passcode
keypad.registerKeyPressHandler(printKey)

while True:
    e = input()
    if e == 'q':
        exit()
