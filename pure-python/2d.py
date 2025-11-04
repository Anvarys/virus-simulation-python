from typing import List
from random import randint
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class Human:
    """
    'infection_chance' is invert of the probability, for example if infection probability is 1% then infection_chance = 100
    """
    def __init__(self, infection_chance=100):
        self.infected_until = 0
        self.immune_until = 0
        self.infection_chance = infection_chance

    def infect(self, current_time, infection_duration, immunity_duration):
        if self.immune_until < current_time and self.immune_until != -1 and randint(1, self.infection_chance) == 1:
            self.infected_until = current_time + infection_duration
            self.immune_until = current_time + infection_duration + immunity_duration

    @classmethod
    def infect_neighbours(cls, x, y, current_time, infection_duration, immunity_duration):
        if y-1 >= 0:
            grid[y-1][x].infect(current_time, infection_duration, immunity_duration)
        if y+1 < SIZE:
            grid[y+1][x].infect(current_time, infection_duration, immunity_duration)
        if x-1 >= 0:
            grid[y][x-1].infect(current_time, infection_duration, immunity_duration)
        if x+1 < SIZE:
            grid[y][x+1].infect(current_time, infection_duration, immunity_duration)

    def step(self, x, y, current_time, infection_duration, immunity_duration):
        if self.infected_until >= current_time and self.infected_until != current_time + infection_duration:
            Human.infect_neighbours(x, y, current_time, infection_duration, immunity_duration)

    def __int__(self):
        return int(self.infected_until >= current_time)


SIZE = int(input("Grid size: "))
INFECTION_DURATION = int(input("Infection duration: "))
IMMUNITY_DURATION = int(input("Immunity duration: "))
INFECTION_CHANCE = int(input("Infection probability: 1/"))
TIME_DURATION = float(input("1 Unit of time (in seconds): "))

grid: List[List[Human]] = [[Human(INFECTION_CHANCE) for __ in range(SIZE)] for _ in range(SIZE)]
current_time = 0
total_infected = 0

grid[randint(0,SIZE-1)][randint(0,SIZE-1)].infected_until = INFECTION_DURATION + 1
print()

fig, ax = plt.subplots()
cmap = ListedColormap(["green", "red"])
im = ax.imshow([[0]], cmap=cmap, vmin=0, vmax=2)
text = fig.text(0.2, 0.9, "Current time: 0\nTotal infected: 0")
plt.axis('off')
plt.ion()
plt.show()

try:
    while True:
        current_time += 1

        for x in range(SIZE):
            for y in range(SIZE):
                grid[y][x].step(x, y, current_time, INFECTION_DURATION, IMMUNITY_DURATION)

        total_infected = 0
        for x in range(SIZE):
            for y in range(SIZE):
                if grid[y][x].infected_until >= current_time:
                    total_infected += 1

        n_grid = [[int(human) for human in column] for column in grid]
        im.set_data(n_grid)
        text.set_text(f"Current time: {current_time}\nTotal infected: {total_infected}")
        plt.pause(TIME_DURATION)
except KeyboardInterrupt:
    exit()