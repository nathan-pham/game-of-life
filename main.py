from copy import deepcopy
from random import random
from time import sleep
from os import system

from typing import List


# prompt for an integer
def prompt(message: str) -> int:
    try:
        return int(input(message))
    except ValueError:
        return prompt(message)


# canvas class
class Canvas:

    # constructor
    def __init__(self, size: int, from_state: List[List[str]] = None):
        self.size = size
        self.state = deepcopy(from_state) if from_state else [
            ["⬛" for j in range(self.size)] for i in range(self.size)]

    # set some default cells
    def seed_glider(self):
        self.set(1, 1, "🟩")
        self.set(2, 2, "🟩")
        self.set(3, 2, "🟩")
        self.set(1, 3, "🟩")
        self.set(2, 3, "🟩")

    # get a cell given an x & y
    def get(self, x: int, y: int) -> str:
        return self.state[y % self.size][x % self.size]

    # set a cell given an x & y
    def set(self, x: int, y: int, value: str) -> None:
        self.state[y % self.size][x % self.size] = value

    # return a deep copy of the canvas
    def copy(self) -> "Canvas":
        return Canvas(self.size, self.state)

    # update method
    def update(self) -> None:

        # create a new canvas
        new_canvas = self.copy()

        # loop through each cell
        for y in range(self.size):
            for x in range(self.size):

                # get the number of living neighbors
                neighbors = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0: continue
                        neighbors += self.get(x + i, y + j) == "🟩"
                        
                # apply rules
                if new_canvas.get(x, y) == "🟩" and not neighbors in [2, 3]:
                    new_canvas.set(x, y, "⬛")
                elif new_canvas.get(x, y) == "⬛" and neighbors == 3:
                    new_canvas.set(x, y, "🟩")

        # update the state
        self.state = new_canvas.state

    # render method
    def render(self) -> None:
        system("cls")

        print('\n'.join(''.join(row) for row in self.state))
        self.update()

        # recursively call render
        sleep(0.1)
        self.render()

if __name__ == "__main__":
    # prompt for canvas self.size
    dimensions = prompt("Enter the canvas dimensions: ")

    # initialize canvas
    canvas = Canvas(dimensions)
    canvas.seed_glider()
    canvas.render()