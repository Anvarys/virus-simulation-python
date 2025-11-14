import time
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
GRAPH = input("Do you want to have graphics to be shown (statistics) [y]es or [n]o: ")
if GRAPH == "y" or GRAPH == "yes":
    GRAPH = True
else:
    GRAPH = False

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
infected = 0
dead = 0

grid.flat[np.random.randint(SIZE**DIMENSIONS)].infected_until = INFECTION_DURATION + 1
total = SIZE**DIMENSIONS
print(f"Total amount of people: {total} | Use Ctrl + C to stop the simulation")


if GRAPH:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    x_data = []

    y_infected = []
    y_alive = []
    y_dead = []
    y_alive_not_infected = []

    infected_line, = ax.plot([], [], label="Infected", lw=2, color="red")
    alive_line, = ax.plot([], [], label="Alive", lw=2, color="green")
    dead_line, = ax.plot([], [], label="Dead", lw=2, color="black")
    alive_not_infected_line, = ax.plot([], [], label="Alive Not Infected", lw=2, color="blue")

    ax.set_xlim(0, 200)
    ax.set_ylim(0, total)

    ax.set_xlabel("Time step")
    ax.set_ylabel("Count")

    ax.legend()

    plt.ion()
    plt.show()

    if TIME_DURATION <= 0:
        TIME_DURATION = 0.000001

try:
    while True:
        current_time += 1

        for index, value in np.ndenumerate(grid):
            value.step(index, current_time, INFECTION_DURATION, IMMUNITY_DURATION)

        infected = 0
        dead = 0
        for index, value in np.ndenumerate(grid):
            if value.dead:
                dead += 1
            elif value.infected_until >= current_time:
                infected += 1
        time.sleep(TIME_DURATION)
        print(f"\rCurrent time: {current_time} | Infected: {infected} | Dead: {dead} | Alive: {total-dead} | Alive-not-infected: {total-infected-dead}              ", end="")

        if GRAPH:
            x_data.append(current_time)

            y_infected.append(infected)
            y_alive.append(total-dead)
            y_dead.append(dead)
            y_alive_not_infected.append(total-dead-infected)

            infected_line.set_data(x_data, y_infected)
            alive_line.set_data(x_data, y_alive)
            dead_line.set_data(x_data, y_dead)
            alive_not_infected_line.set_data(x_data, y_alive_not_infected)

            ax.set_xlim(0, max(200, current_time))

            plt.pause(TIME_DURATION)

except KeyboardInterrupt:
    plt.close('all')