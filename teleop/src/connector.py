import socket
import logging
import sys
import threading
import time

import src.util as util

# Drive Computer Remote Telop Client
# Connector
#
# Part of the GSSM Autonomous Golf Cart
# Written by:
#   Benjamin Chauhan, class of 2022
#   Joseph Telaak, class of 2022

class Teleop_Connector:

    def __init__(self, ip_addr, establish_port, command_port, log_port, response_port):
        # Create Ports
        self.logging_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.response_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Keystroke Logger (Useful for training and repeating actions)
        self.keystroke_logger = logging.getLogger("keystroke")
        self.keystroke_logger.setLevel(logging.DEBUG)
        keystroke_file_handler = logging.FileHandler("recored_presses.log")
        keystroke_file_handler.setFormatter("%(asctime)s - %(message)s")
        self.keystroke_logger.addHandler(keystroke_file_handler)

        # Cart Response Logger
        self.response_logger = logging.getLogger("response_log")
        self.response_logger.setLevel(logging.DEBUG)

        response_file_handler = logging.FileHandler("responses.log")
        response_file_handler.setFormatter("%(asctime)s - %(message)s")
        self.response_logger.addHandler(response_file_handler)

        response_console_handler = logging.StreamHandler(sys.stdout)
        response_console_handler.setFormatter("%(asctime)s - %(name)s - %(message)s")
        self.response_logger.addHandler(response_console_handler)

        # Cart Response Logger
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        log_file_handler = logging.FileHandler("log.log")
        log_file_handler.setFormatter("%(asctime)s - %(message)s")
        self.logger.addHandler(log_file_handler)

        log_console_handler = logging.StreamHandler(sys.stdout)
        log_console_handler.setFormatter("%(asctime)s - %(name)s - %(message)s")
        self.logger.addHandler(log_console_handler)

        # Config
        self.ip_addr = ip_addr
        self.establish_port = establish_port
        self.command_port = command_port
        self.log_port = log_port
        self.response_port = response_port

        # Threads
        self.log_listener_thread = threading.Thread(target=self.log_listener, name="log listener", daemon=True)
        self.response_listener_thread = threading.Thread(target=self.response_lister, name="response listener", daemon=True)

        # Kill
        self.kill = False

    # Sends a command to enable the server on the drice computer
    # Returns boolean
    def establish_connection(self, max_attempts = 5):
        print(f"Attempting to Establish Connection with {self.ip_addr}")

        connected = False
        attempts = 0

        while not connected:
            # Create Connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip_addr, self.establish_port))

            # Send request
            s.send(("Bruh, lemme control you with dis joystick!").encode())
            data = s.recv(1024)
        
            # Check message
            if data.decode() == "Okay no cap!":
                print("Connection Successful")
                return True

            else:
                # Increment Attempts Counter
                attempts += 1

                # Exit
                if attempts == max_attempts:
                    print(util.to_color("Connection Failed, Exiting...", "red"))
                    sys.exit(1)

    # Close the connector
    def close(self):
        print("Exiting. Killing all threads and closing sockets")
        self.kill = True

        # Create Connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_addr, self.establish_port))

        # Send request
        s.send(("I think we need to talk").encode())
        
        # Wait and close
        time.sleep(2)

    # Sends an action to the sever
    def sendAction(self, action):
        self.keystroke_logger.info(str(action))
        self.command_socket.sendto(bytes(action, 'utf-8'), (self.ip_addr, self.command_port))

    # Starts the listner threads
    def startListeners(self):
        self.log_listener_thread.start()
        self.response_listener_thread.start()

    # Listens for log info from the server
    def log_listener(self):
        # Accept Connectiond
        self.logging_socket.listen()

        while not self.kill:
            # Get Connection
            (clientConnected, clientAddress) = self.logging_socket.accept()
            data = clientConnected.recv(1024).decode()

            # Log
            self.logger.info(data)
            
    # Listens for repsonses from the server
    def response_lister(self):
        # Accept Connections
        self.response_socket.listen()

        while not self.kill:
            # Get Connection
            (clientConnected, clientAddress) = self.response_socket.accept()
            data = clientConnected.recv(1024).decode()

            # Log
            self.response_logger.info(data)
