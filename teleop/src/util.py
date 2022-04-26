import pyfiglet

# Drive Computer Remote Telop Client
# Utils
#
# Part of the GSSM Autonomous Golf Cart
# Written by:
#   Benjamin Chauhan, class of 2022
#   Joseph Telaak, class of 2022

# ASCII Art Header for Console Output
title = pyfiglet.figlet_format("GSSM AutoCart", font="slant")

# Info Block Printed to Console on Init
info_block = """
    GSSM's Auto Golf Cart Project
    Core Drive Computer Teleop Client

    Project Built for Dr. Parshall's Engineering Projects Course

    Software written by 
        Joseph Telaak (The1TrueJoe), GSSM Class of 2022, Stanford Class of 2026
        Benjamin Chauhan (Meeeee6623), GSSM Class of 2022, Duke Class of 2026

    See https://github.com/GSSM-AutoGolfCart
"""

def to_color(string, color):
    colors = {
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "purple": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
        "reset": "\033[0m"

    }

    return colors[color] + str(string) + colors["reset"]