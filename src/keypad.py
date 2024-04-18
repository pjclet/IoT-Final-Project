from pad4pi import rpi_gpio

def get_key(key):
    return key

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
    final_password = ""
    while len(final_password) < 4:
        current_input = keypad.registerKeyPressHandler(get_key)
        if (current_input):
            final_password = final_password + str(current_input).strip()
            print("[KEYPAD] Received input: {}".format(current_input))
    
    print("[KEYPAD] Final password: {}, length: {}".format(final_password, len(final_password)))
    return final_password



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