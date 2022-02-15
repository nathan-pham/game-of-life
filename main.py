from __future__ import annotations
from typing import List

from random import random
from copy import deepcopy
from time import sleep
from os import system

# how alive or dead cells should look
ALIVE = "🟩"
DEAD = "⬛"

def input_int(message: str) -> int:
    """
    prompt for an integer 
    if not an integer, then re-prompt for one
    """

    try:
        return int(input(message))
    except ValueError:
        return input_int(message)


# prompt for a string but enforce a certain list of responses
def input_str(message: str, enforce: List[str] = []) -> str:
    """
    prompt for a string
    if response is not in the list of responses, then re-prompt for one
    """

    response = input(message)
    if response in enforce or len(enforce) == 0:
        return response
    else:
        return input_str(message, enforce)


# canvas class
class Canvas:

    # constructor
    def __init__(self, size: int, from_state: List[List[str]] = None):
        """
        create a new canvas with a specified size
        if from_state is specified, then use that as the initial state
        """

        self.size = size

        if(from_state):
            self.state = deepcopy(from_state)
        else:
            self.state = [[DEAD for j in range(self.size)] for i in range(self.size)]

    def seed(self, initial_state: str) -> None:
        """
        seed the canvas with a specified initial state (glider or random)
        """

        if initial_state == "glider":
            self.seed_glider()
        elif initial_state == "random":
            self.seed_random()

    def seed_glider(self):
        """
        create a glider in the top left corner
        """

        self.set(1, 1, ALIVE)
        self.set(2, 2, ALIVE)
        self.set(3, 2, ALIVE)
        self.set(1, 3, ALIVE)
        self.set(2, 3, ALIVE)

    def seed_random(self):
        """
        set a random cell to green based on a 50% chance
        """

        for y in range(self.size):
            for x in range(self.size):
                if random() < 0.5:
                    self.set(x, y, ALIVE)

    def get(self, x: int, y: int) -> str:
        """
        get the value of a cell given an x & y
        """

        return self.state[y % self.size][x % self.size]

    def set(self, x: int, y: int, value: str) -> None:
        """
        set the value of a cell given an x & y
        """
        self.state[y % self.size][x % self.size] = value

    def copy(self) -> Canvas:
        """
        copy the entire canvas
        """

        return Canvas(self.size, self.state)

    def get_living_neighbors(self, x: int, y: int) -> int:
        """
        calculate the living neighbors
        """

        neighbors = 0

        # loop through each neighboring cell (8 total)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # skip self which is at x, y

                neighbors += self.get(x + i, y + j) == ALIVE

        return neighbors

    def update(self) -> None:
        """
        update the canvas each frame
        SEQUENCING: 
            1. create a copy of the canvas to cache the previous state
            2. iterate through each cell
            3. calculate the living neighbors
            4. set the new state of the cell depending on the living neighbors
        """

        # create a new canvas
        new_canvas = self.copy()

        # ITERATION: loop through each cell 
        for y in range(self.size):
            for x in range(self.size):

                # get the number of living neighbors
                neighbors = self.get_living_neighbors(x, y)

                # SELECTION: apply rules described in https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
                # any cell with 2 or 3 living neighbors stays alive
                if new_canvas.get(x, y) == ALIVE and not neighbors in [2, 3]:
                    new_canvas.set(x, y, DEAD)

                # any cell with 3 living neighbors becomes alive
                elif new_canvas.get(x, y) == DEAD and neighbors == 3:
                    new_canvas.set(x, y, ALIVE)

                # otherwise the cell stays the same

        # update the state
        self.state = new_canvas.state

    def render(self) -> None:
        """
        render the canvas to the console each frame
        """

        system("cls")
        print('\n'.join(''.join(row) for row in self.state))

    def animate(self, delay: int = 0.1) -> None:
        """
        run update & render each frame
        """

        while True:
            self.update()
            self.render()
            sleep(delay)


def main():
    """
    main method, called if this file is run directly
    """
    
    # prompt for canvas self.size
    dimensions = input_int("Enter the canvas width or height > ")
    seed = input_str("Enter seed > ", ["glider", "random"])

    # initialize canvas
    canvas = Canvas(dimensions)
    canvas.seed(seed)

    # animate the canvas
    canvas.animate()


if __name__ == "__main__":
    main()