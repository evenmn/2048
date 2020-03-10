from pynput.keyboard import Key, Listener
import threading
import time


class Player:
    def __init__(self, game, engine, gui):
        self.game = game
        self.engine = engine
        self.gui = gui

    def play_game(self):
        while not self.game.done:
            self.gui.render(self.game)
            action = self.engine(self.game)
            self.game = self.game(action)

        self.gui.render(self.game)
        self.gui.tear_down()


def random_engine(game, speed=1):
    from random import choice

    time.sleep(speed)
    return choice(list(game.ACTIONS.values()))


class KeyboardListener:
    def __init__(self, game):
        self.game = game
        self.action_list = []

        listener = Listener(on_press=self.on_press)
        listener.start()

    def on_press(self, key):

        if key == Key.up:
            self.action_list.append(self.game.ACTIONS["UP"])

        if key == Key.right:
            self.action_list.append(self.game.ACTIONS["RIGHT"])
            
        if key == Key.down:
            self.action_list.append(self.game.ACTIONS["DOWN"])
            
        if key == Key.left:
            self.action_list.append(self.game.ACTIONS["LEFT"])

        if key == Key.esc:
            self.game.done = True

    def __call__(self, game):
    
        action = self.game.ACTIONS["NONE"]
    
        if len(self.action_list) > 0:
            action = self.action_list.pop(0)

        return action


if __name__ == "__main__":
    from tzfe import Game
    from gui import TerminalGui, MatplotlibGui

    game = Game(4, 4)
    keyboard_listener = KeyboardListener(game)

    player = Player(game, random_engine, TerminalGui())
    player.play_game()
