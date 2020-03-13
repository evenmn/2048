import os
import numpy as np
import matplotlib.pyplot as plt

class color:
   PURPLE    = '\033[95m'
   CYAN      = '\033[96m'
   DARKCYAN  = '\033[36m'
   BLUE      = '\033[94m'
   GREEN     = '\033[92m'
   YELLOW    = '\033[93m'
   RED       = '\033[91m'
   BOLD      = '\033[1m'
   UNDERLINE = '\033[4m'
   GRAY      = '\033[2m'
   KURSIV    = '\033[3m'
   END       = '\033[0m'

class NoGui:
    def __init__(self, title="2048"):
        self.title = title + " score: {0}"

    def render(self, state):
        print(self.title.format(state.score))

    def tear_down(self):
        pass


class MatplotlibGui:
    def __init__(self, title="2048"):
        plt.figure()
        self.title = title + " score: {0}"
        plt.title(self.title.format(0))

    def render(self, state):
        plt.clf()
        plt.title(self.title.format(state.score))
        plt.imshow(np.array(state.board))
        plt.axis('off')
        plt.pause(0.01)
        plt.draw()

    def tear_down(self):
        plt.clf()


class TerminalGui:
    def __init__(self, title="2048"):
        self.title = title + " score: {0}"
        self._clear_terminal()

    def _clear_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")

    def render(self, state):
        self._clear_terminal()

        print("\n", self.title.format(state.score), "\n")
        
        for i in range(state.board_height):
            row = []
            for j in range(state.board_width):
                if int(state.board[i,j]) == 0:
                    row.append(color.GRAY + "0" + color.END)
                else:
                    row.append(color.BOLD + "%.d" % int(state.board[i,j]) + color.BOLD)
            print("\t", "\t".join(row), "\n")

    def tear_down(self):
        pass


if __name__ == "__main__":
    from snake import SnakeGame

    gui = MatplotlibGui()
    gui.render(SnakeGame(initial_length=7))
    plt.show()
