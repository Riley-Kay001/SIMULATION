import pygame
import random
import math


# Infection Spreading 
INFECTION_RADIUS = 10
INFECTION_CHANCE = 0.2  # 20% chance

def spread_infection(people):
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1 = people[i]
            p2 = people[j]

            dx = p1.x - p2.x
            dy = p1.y - p2.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 10:
                if p1.state == "infected" and p2.state == "healthy":
                    if random.random() < 0.2:
                        p2.state = "infected"

                elif p2.state == "infected" and p1.state == "healthy":
                    if random.random() < 0.2:
                        p1.state = "infected"


# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
HEALTHY_COLOR = (0, 200, 0)
INFECTED_COLOR = (200, 0, 0)
RECOVERING_COLOR = (0, 0, 200)

class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.state = "healthy"
        self.infection_time = 0

        # Random movement direction
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH:
            self.dx *= -1
        if self.y <= 0 or self.y >= HEIGHT:
            self.dy *= -1

    def update(self):
        if self.state == "infected":
            self.infection_time += 1

            # After some time, recover
            if self.infection_time > 300:
                self.state = "recovering"

    def draw(self, screen):
        if self.state == "healthy":
            color = HEALTHY_COLOR
        elif self.state == "infected":
            color = INFECTED_COLOR
        else:
            color = RECOVERING_COLOR

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

# Create population
people = [Person(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Infect one person initially
people[0].state = "infected"


# Statistics Class 
class Statistics:
    def __init__(self):
        self.healthy = 0
        self.infected = 0
        self.recovering = 0

        self.font = pygame.font.SysFont(None, 24)

    def update(self, people):
        # Reset counts
        self.healthy = 0
        self.infected = 0
        self.recovering = 0

        # Count states
        for person in people:
            if person.state == "healthy":
                self.healthy += 1
            elif person.state == "infected":
                self.infected += 1
            elif person.state == "recovering":
                self.recovering += 1

    def draw(self, screen):
        text = f"Healthy: {self.healthy}  Infected: {self.infected}  Recovering: {self.recovering}"
        img = self.font.render(text, True, (255, 255, 255))
        screen.blit(img, (10, 10))

        stats = Statistics()

    while running:
        screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for person in people:
        person.move()
        person.update()

    spread_infection(people)

    # ✅ Update stats
    stats.update(people)

    for person in people:
        person.draw(screen)

    # ✅ Draw stats on top
    stats.draw(screen)

    pygame.display.flip()
    clock.tick(60)


# Main loop
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw people
    for person in people:
        person.move()
        person.update()

    spread_infection(people)
    print(spread_infection) 

    for person in people:
        person.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
