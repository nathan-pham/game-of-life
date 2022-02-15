from __future__ import annotations
from typing import List

from random import random
from copy import deepcopy
from time import sleep
from os import system


# prompt for an integer
def input_int(message: str) -> int:
    try:
        return int(input(message))
    except ValueError:
        return input_int(message)


# prompt for a string but enforce a certain list of responses
def input_str(message: str, enforce: List[str]=[]) -> str:
    response = input(message)
    if response in enforce or len(enforce) == 0:
        return response
    else:
        return input_str(message, enforce)


# canvas class
class Canvas:

    # constructor
    def __init__(self, size: int, from_state: List[List[str]] = None):
        self.size = size
        self.state = deepcopy(from_state) if from_state else [
            ["⬛" for j in range(self.size)] for i in range(self.size)]

    
    # seed the canvas
    def seed(self, initial_state: str) -> None:
        if initial_state == "glider":
            self.seed_glider()
        elif initial_state == "random":
            for y in range(self.size):
                for x in range(self.size):
                    if random() < 0.5:
                        self.set(x, y, "🟩")


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
    def copy(self) -> Canvas:
        return Canvas(self.size, self.state)

    # get living neighbors
    def get_living_neighbors(self, x: int, y: int) -> int:
        neighbors = 0

        # loop through each 8 neighboring cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue # skip x, y

                neighbors += self.get(x + i, y + j) == "🟩"

        return neighbors

    # update method
    def update(self) -> None:

        # create a new canvas
        new_canvas = self.copy()

        # loop through each cell
        for y in range(self.size):
            for x in range(self.size):

                # get the number of living neighbors
                neighbors = self.get_living_neighbors(x, y)

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

if __name__ == "__main__":
    # prompt for canvas self.size
    dimensions = input_int("Enter the canvas width or height > ")
    seed = input_str("Enter seed > ", ["glider", "random"])

    # initialize canvas
    canvas = Canvas(dimensions)
    canvas.seed(seed)

    while True:
        canvas.render()
        canvas.update()
        sleep(0.1)