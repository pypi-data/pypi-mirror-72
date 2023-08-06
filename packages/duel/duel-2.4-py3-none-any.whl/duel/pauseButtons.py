import pygame
import os

image_dictionary = dict()

class PauseButton(pygame.sprite.DirtySprite):

    def __init__(self, button_type):
        pygame.sprite.DirtySprite.__init__(self)
        self.button_state = {
            "unhighlighted": True,
            "highlighted": False,
            "clicked": False
        }
        self.button_type = button_type
        self.image = self.getImage(self.getSprite(), image_dictionary)
        self.rect = pygame.Rect(0,0, 220, 50)

    def getImage(self, path, _image_library):
        if path not in _image_library:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), canonicalized_path))
            _image_library[path] = image
        return _image_library[path]

    def update(self):
        self.image = self.getImage(self.getSprite(), image_dictionary)
        self.dirty = 1

    def getSprite(self):
        path = "Resources/Images/Buttons/"
        if self.button_state["unhighlighted"]:
            return path + self.button_type + "ButtonUnhighlighted.png"
        elif self.button_state["highlighted"]:
            return path + self.button_type + "ButtonHighlighted.png"
        elif self.button_state["clicked"]:
            return path + self.button_type + "ButtonClicked.png"

    def updateState(self, state):
        if state == "Highlighted":
            self.button_state["unhighlighted"] = False
            self.button_state["highlighted"] = True
            self.button_state["clicked"] = False
        elif state == "Clicked":
            self.button_state["unhighlighted"] = False
            self.button_state["highlighted"] = False
            self.button_state["clicked"] = True
        elif state == "Unhighlighted":
            self.button_state["unhighlighted"] = True
            self.button_state["highlighted"] = False
            self.button_state["clicked"] = False

    def initializeRect(self):
        if self.button_type == "Play":
            self.rect.center = (500,300)
        if self.button_type == "Restart":
            self.rect.center = (500, 350)
        if self.button_type == "Exit":
            self.rect.center = (500, 400)