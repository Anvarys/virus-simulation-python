from typing import List
import matplotlib.pyplot as plt
import numpy as np


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
    def infect_neighbours(cls, x, y, z, current_time, infection_duration, immunity_duration):
        if y-1 >= 0:
            grid[y-1][x][z].infect(current_time, infection_duration, immunity_duration)
        if y+1 < SIZE:
            grid[y+1][x][z].infect(current_time, infection_duration, immunity_duration)
        if x-1 >= 0:
            grid[y][x-1][z].infect(current_time, infection_duration, immunity_duration)
        if x+1 < SIZE:
            grid[y][x+1][z].infect(current_time, infection_duration, immunity_duration)
        if z-1 >= 0:
            grid[y][x][z-1].infect(current_time, infection_duration, immunity_duration)
        if z+1 < SIZE:
            grid[y][x][z+1].infect(current_time, infection_duration, immunity_duration)

    def step(self, x, y, z, current_time, infection_duration, immunity_duration):
        if self.dead:
            return
        if self.infected_until >= current_time and self.infected_until != current_time + infection_duration:
            Human.infect_neighbours(x, y, z, current_time, infection_duration, immunity_duration)

    def __int__(self):
        return int(self.infected_until >= current_time) if not self.dead else 2


print("Warning! This 3d simulation might lag substantially")
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

grid: List[List[List[Human]]] = [[[Human(INFECTION_CHANCE, DEATH_CHANCE) for ___ in range(SIZE)] for __ in range(SIZE)] for _ in range(SIZE)]
current_time = 0
total_infected = 0

grid[np.random.randint(SIZE)][np.random.randint(SIZE)][np.random.randint(SIZE)].infected_until = INFECTION_DURATION + 1

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
plt.ion()
plt.show()

text = fig.text(0.02, 0.9, "")

try:
    while True:
        current_time += 1

        for x in range(SIZE):
            for y in range(SIZE):
                for z in range(SIZE):
                    grid[y][x][z].step(x, y, z, current_time, INFECTION_DURATION, IMMUNITY_DURATION)

        total_infected = 0
        dead = 0
        voxel_array = np.full((SIZE, SIZE, SIZE), False, dtype=bool)
        colors = np.empty(voxel_array.shape, dtype=object)
        for x in range(SIZE):
            for y in range(SIZE):
                for z in range(SIZE):
                    if grid[y][x][z].dead:
                        dead += 1
                        colors[(x, y, z)] = '#0000003F'
                        voxel_array[(x, y, z)] = True
                    elif grid[y][x][z].infected_until >= current_time:
                        colors[(x, y, z)] = '#FF00003F'
                        total_infected += 1
                        voxel_array[(x, y, z)] = True
        n_grid = [[[int(human) for human in column] for column in layer] for layer in grid]
        ax.voxels(voxel_array, facecolors=colors, edgecolor='#FFFFFF8F')
        text.set_text(f"Current time: {current_time} | Infected: {total_infected} | Dead: {dead} | Alive-uninfected: {SIZE*SIZE*SIZE-total_infected-dead}")
        plt.pause(TIME_DURATION)
except KeyboardInterrupt:
    exit()