import random
import matplotlib.pyplot as plt
import pygame
import math

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus Simulator")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)      # Susceptible
RED = (255, 50, 50)       # Infected
GREEN = (50, 200, 50)     # Recovered

# Population settings
population = 200 
initial_infected = 5

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

# Disease parameters
infection_rate = 0.05
recovery_rate = 0.01
days = 100

# Simulation settings
NUM_PEOPLE = 60
INFECTION_RADIUS = 10
INFECTION_CHANCE = 0.2
RECOVERY_CHANCE = 0.002
SPEED = 2

clock = pygame.time.Clock()

# Main Game Loop
people = [SUSCEPTIBLE] * 50

# start with one infected
people[0] = INFECTED

steps = 20

for step in range(steps):
    people = simulate_step(people)

    infected_count = people.count(INFECTED)
    print(f"Step {step}: {infected_count} infected")

running = True
while running:
    # handle events here

    people = simulate_step(people)

    # draw people here

#Person Class 
class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 5
        self.speed = 1

        self.state = Person.SUSCEPTIBLE
        self.infection_time = 0

    def move(self, width, height):

        dx = random.uniform(-self.speed, self.speed)
        dy = random.uniform(-self.speed, self.speed)

        self.x += dx
        self.y += dy

        # keep inside screen
        self.x = max(0, min(width, self.x))
        self.y = max(0, min(height, self.y))

    def infect(self):
        if self.state == Person.SUSCEPTIBLE:
            self.state = Person.INFECTED
            self.infection_time = 0

    def update(self, recovery_time):

        if self.state == Person.INFECTED:
            self.infection_time += 1

            if self.infection_time > recovery_time:
                self.state = Person.RECOVERED

    def get_color(self):

        if self.state == Person.SUSCEPTIBLE:
            return (0, 200, 0)     # green

        if self.state == Person.INFECTED:
            return (200, 0, 0)     # red

        if self.state == Person.RECOVERED:
            return (0, 100, 255)   # blue

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            self.get_color(),
            (int(self.x), int(self.y)),
            self.radius
        )

# Infect some people initially
for i in random.sample(range(population), initial_infected):
    people[i] = INFECTED

susceptible_history = []
infected_history = []
recovered_history = []

for day in range(days):
    new_people = people.copy()

    for i in range(population):
        if people[i] == INFECTED:

            # Try infecting others
            for j in range(population):
                if people[j] == SUSCEPTIBLE and random.random() < infection_rate:
                    new_people[j] = INFECTED

            # Try recovery
            if random.random() < recovery_rate:
                new_people[i] = RECOVERED

    people = new_people

    # Count states
    s = people.count(SUSCEPTIBLE)
    i = people.count(INFECTED)
    r = people.count(RECOVERED)

    susceptible_history.append(s)
    infected_history.append(i)
    recovered_history.append(r)

# Plot results
plt.plot(susceptible_history, label="Susceptible")
plt.plot(infected_history, label="Infected")
plt.plot(recovered_history, label="Recovered")

plt.xlabel("Days")
plt.ylabel("People")
plt.title("Virus Spread Simulation")
plt.legend()
plt.show()
