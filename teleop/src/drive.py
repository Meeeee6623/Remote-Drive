import sys

from src.controller import Gamepad
from src.connector import Teleop_Connector

# Drive Computer Remote Telop Client
# Teleop Client
#
# Part of the GSSM Autonomous Golf Cart
# Written by:
#   Benjamin Chauhan, class of 2022
#   Joseph Telaak, class of 2022

# Controller
controller = Gamepad()

# Connector
connector = Teleop_Connector(ip_addr=str(sys.argv[0]),establish_port=69420, command_port=69, log_port=420, response_port=777)

# Init
def init():
    print("Initializing Teleop Client")

    # Establish Server Connection
    if connector.establish_connection():
        connector.startListeners()
    
    else:
        sys.exit(1)

    # Connect Controller
    controller.startLister()

    print("Initialization Complete")

# Run
def run():
    while not controller.buttons['BTN_START']:
        # Controller Byttons
        for button in controller.buttons.keys():
            if controller.buttons[button] == True:
                connector.sendAction(button)
                continue

        # Sticks
        for stick in controller.sticks.keys():
            if controller.sticks[stick] != 0.0:
                connector.sendAction(f"{stick}: {controller.sticks[stick]}")
                continue
            
        # Triggers
        for trigger in controller.triggers.keys():
            if controller.triggers[trigger] != 0.0:
                connector.sendAction(f"{trigger}: {controller.triggers[trigger]}")
                continue

    # Close
    connector.close()