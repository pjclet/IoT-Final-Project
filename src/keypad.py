from pad4pi import rpi_gpio
import time

current = ""

def add_current(key):
    global current
    if len(current) > 4:
        print("[KEYPAD] More than 4 keypresses registered. Comparing " + current + "...")
    else:
        current += str(key)

def get_key(key):
    try:
        if key != None:
            print("[KEYPAD] Key received: " + str(key))
            int_key = int(key)
            add_current(key)
    except ValueError:
        print("[KEYPAD] Invalid key received: " + str(key))

def printKey(key):
    print(key)

def get_keypad_input():
    KEYPAD = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        ["*", 0, "#"]
    ]

    # BCM not GPIO
    ROW_PINS = [4, 17, 27, 22]
    COL_PINS = [5, 6, 13]

    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    # register key handler
    final = ""
    keypad.registerKeyPressHandler(get_key)
    global current
    while len(current) < 4:
        time.sleep(1)
    print("[KEYPAD] Final password: {}, length: {}".format(current, len(current)))
    final = current
    current = ""
    keypad.clearKeyPressHandlers()
    return final

if __name__ == '__main__':
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


    # register key handler - later replace this with comparing against the predefined passcode
    keypad.registerKeyPressHandler(printKey)

    while True:
        e = input()
        if e == 'q':
            exit()
