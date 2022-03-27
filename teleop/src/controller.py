from inputs import get_gamepad

import threading

# Drive Computer Remote Telop Client
# Controller
#
# Part of the GSSM Autonomous Golf Cart
# Written by:
#   Benjamin Chauhan, class of 2022
#   Joseph Telaak, class of 2022

class Gamepad:
    # Controller Buttons
    buttons = {
        'BTN_TL': False,
        'BTN_TR': False,
        'BTN_NORTH': False,
        'BTN_EAST': False,
        'BTN_SOUTH': False,
        'BTN_WEST': False,
        'BTN_THUMBL': False,
        'BTN_THUMBR': False,
        'BTN_START': False,
        'BTN_SELECT': False,
        'DPAD_NORTH': False,
        'DPAD_SOUTH': False,
        'DPAD_EAST': False,
        'DPAD_WEST': False
    }

    # Controller Sticks
    sticks = {
        'LSTICK_X': 0.0,
        'LSTICK_Y': 0.0,
        'RSTICK_X': 0.0,
        'RSTICK_Y': 0.0
    }

    # Controller Triggers
    triggers = {
        'ABS_Z': 0.0,
        'ABS_RZ': 0.0
    }

    # Constructor
    def __init__(self):
        self.listener = threading.Thread(target=self.listen, daemon=True)

    # Start the Listener
    def startLister(self):
        self.listener.start()

    # Update the keypress
    def update(self):
        events = get_gamepad()

        for event in events:
            if event.ev_type == 'Sync':
                return

            if event.ev_type == 'Key':
                if event.state == 1:
                    self.buttons[event.code] = True

                elif event.state == 0:
                    self.buttons[event.code] = False

            elif event.ev_type == 'Absolute':
                if event.code in self.sticks.keys():
                    # joystick values: -32768 --> 32767
                    self.sticks[event.code] = event.state / 32768  # normalize values between -1 and 1

                elif event.code in self.triggers.keys():
                    # max trigger value: 255
                    self.triggers[event.code] = event.state / 255  # 0 --> 1

                else:
                    if event.code == 'ABS_HAT0Y':
                        if event.state == -1:
                            self.buttons['DPAD_SOUTH'] = True

                        elif event.state == 1:
                            self.buttons['DPAD_NORTH'] = True

                        else:
                            self.buttons['DPAD_SOUTH'] = False
                            self.buttons['DPAD_NORTH'] = False

                    if event.code == 'ABS_HAT0X':
                        if event.state == -1:
                            self.buttons['DPAD_WEST'] = True

                        elif event.state == 1:
                            self.buttons['DPAD_EAST'] = True

                        else:
                            self.buttons['DPAD_WEST'] = False
                            self.buttons['DPAD_EAST'] = False

        return

    # Listener
    def listen(self):
        while True:
            self.update()
