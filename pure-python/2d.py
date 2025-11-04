from typing import List
from random import randint
from time import sleep


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


SIZE = int(input("Grid size: "))
INFECTION_DURATION = int(input("Infection duration: "))
IMMUNITY_DURATION = int(input("Immunity duration: "))
INFECTION_CHANCE = int(input("Infection probability: 1/"))
TIME_DURATION = float(input("1 Unit of time (in seconds): "))

grid: List[List[Human]] = [[Human(INFECTION_CHANCE) for __ in range(SIZE)] for _ in range(SIZE)]
current_time = 0
total_infected = 0

grid[1][1].infected_until = INFECTION_DURATION + 1
print()

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

        print(f"\rCurrent time: {current_time}  |  Total infected: {total_infected}    ", end="")
        sleep(TIME_DURATION)
except KeyboardInterrupt:
    exit()