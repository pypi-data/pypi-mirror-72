import duel.window
import duel.gameEngine
from duel import *
import pygame
import os

def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    duel.gameEngine.mainMenu(duel.window.startScreen())


if __name__ == '__main__':
    main()

