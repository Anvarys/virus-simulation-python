import time
from typing import List
import numpy as np
from numpy.f2py.auxfuncs import throw_error


class Human:
    """
    'infection_chance' is invert of the probability, for example if infection probability is 1% then infection_chance = 100
    'death_chance' is invert of the probability, for example if death probability is 1% then death_chance = 100
    """
    def __init__(self, infection_chance: int = 100, death_chance: int = 100):
        self.infected_until = 0
        self.immune_until = 0
        self.dead = False
        self.infection_chance = infection_chance
        self.death_chance = death_chance

    def infect(self, current_time, infection_duration, immunity_duration):
        if self.dead:
            return
        if self.immune_until < current_time and self.immune_until != -1 and np.random.randint(self.infection_chance) == 0:
            self.infected_until = current_time + infection_duration
            self.immune_until = current_time + infection_duration + immunity_duration
            if self.death_chance > 0 and np.random.randint(self.death_chance) == 0:
                self.dead = True

    @classmethod
    def infect_neighbours(cls, coords, current_time, infection_duration, immunity_duration):
        for dim in range(len(coords)):
            l_coords = list(coords)
            l_coords[dim] += 1
            if l_coords[dim] < SIZE:
                grid[tuple(l_coords)].infect(current_time, infection_duration, immunity_duration)

            l_coords[dim] -= 2
            if l_coords[dim] >= 0:
                grid[tuple(l_coords)].infect(current_time, infection_duration, immunity_duration)

    def step(self, coords, current_time, infection_duration, immunity_duration):
        if self.dead:
            return
        if self.infected_until >= current_time and self.infected_until != current_time + infection_duration:
            Human.infect_neighbours(coords, current_time, infection_duration, immunity_duration)

    def __int__(self):
        return int(self.infected_until >= current_time) if not self.dead else 2


DIMENSIONS = int(input("Dimensions (> 0): "))
if DIMENSIONS < 1:
    raise ValueError("Number of dimensions < 1")
SIZE = int(input("Grid size: "))
if SIZE < 1:
    raise ValueError("Size < 1")
INFECTION_DURATION = int(input("Infection duration: "))
if INFECTION_DURATION < 0:
    raise ValueError("Infection duration < 0")
IMMUNITY_DURATION = int(input("Immunity duration: "))
if IMMUNITY_DURATION < 0:
    raise ValueError("Immunity duration < 0")
INFECTION_CHANCE = int(input("Infection probability: 1/"))
if INFECTION_CHANCE < 1:
    raise ValueError("Infection chance < 1")
_DEATH_CHANCE = input("Death probability (Press Enter to skip): 1/")
TIME_DURATION = float(input("1 Unit of time (in seconds): "))
if TIME_DURATION < 0:
    raise ValueError("Time duration < 0")

if len(_DEATH_CHANCE) == 0:
    DEATH_CHANCE = 0
else:
    DEATH_CHANCE = int(_DEATH_CHANCE)
    if DEATH_CHANCE < 0:
        raise ValueError("Death chance < 0")

shape = tuple([SIZE for _ in range(DIMENSIONS)])

grid = np.empty(shape, dtype=object)

for index, _ in np.ndenumerate(grid):
    grid[index] = Human(INFECTION_CHANCE, DEATH_CHANCE)

current_time = 0
total_infected = 0
dead = 0

grid.flat[np.random.randint(SIZE**DIMENSIONS)].infected_until = INFECTION_DURATION + 1
print(f"Total amount of people: {SIZE**DIMENSIONS}")


try:
    while True:
        current_time += 1

        for index, value in np.ndenumerate(grid):
            value.step(index, current_time, INFECTION_DURATION, IMMUNITY_DURATION)

        total_infected = 0
        dead = 0
        for index, value in np.ndenumerate(grid):
            if value.dead:
                dead += 1
            elif value.infected_until >= current_time:
                total_infected += 1
        time.sleep(TIME_DURATION)
        print(f"\rCurrent time: {current_time} | Infected: {total_infected} | Dead: {dead} | Alive: {SIZE**DIMENSIONS-dead} | Alive-not-infected: {SIZE**DIMENSIONS-total_infected-dead}              ", end="")
except KeyboardInterrupt:
    pass