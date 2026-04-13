import random
import pygame
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus Simulation")

font = pygame.font.SysFont(None, 24)

# Population settings
population = 200
initial_infected = 10

# Disease parameters
infection_rate = 0.5
recovery_time = 1000  # frames

# -------------------------------------------------
# Person Class
# -------------------------------------------------
class Person:
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = 1

        self.state = Person.SUSCEPTIBLE
        self.infection_time = 0

    def move(self):
        dx = random.uniform(-self.speed, self.speed)
        dy = random.uniform(-self.speed, self.speed)

        # Try moving X
        new_x = self.x + dx
        future_rect = pygame.Rect(new_x, self.y, self.radius * 2, self.radius * 2)

        if not any(wall.colliderect(future_rect) for wall in walls):
            self.x = new_x

        # Try moving Y
        new_y = self.y + dy
        future_rect = pygame.Rect(self.x, new_y, self.radius * 2, self.radius * 2)

        if not any(wall.colliderect(future_rect) for wall in walls):
            self.y = new_y

        # Keep inside screen
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def infect(self):
        if self.state == Person.SUSCEPTIBLE:
            self.state = Person.INFECTED
            self.infection_time = 0

    def update(self):
        if self.state == Person.INFECTED:
            self.infection_time += 1
            if self.infection_time > recovery_time:
                self.state = Person.RECOVERED

    def get_color(self):
        if self.state == Person.SUSCEPTIBLE:
            return (0, 200, 0)
        elif self.state == Person.INFECTED:
            return (200, 0, 0)
        else:
            return (0, 100, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.get_color(), (int(self.x), int(self.y)), self.radius)


# -------------------------------------------------
# Button Class
# -------------------------------------------------
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()


# -------------------------------------------------
# Slider Control
# -------------------------------------------------
class Controls:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        self.knob_x = x + width // 2
        self.dragging = False

        self.min_val = 0.5
        self.max_val = 2.0

    def get_value(self):
        t = (self.knob_x - self.x) / self.width
        return self.min_val + t * (self.max_val - self.min_val)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.knob_x) < 10 and abs(event.pos[1] - self.y) < 10:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_x = max(self.x, min(self.x + self.width, event.pos[0]))

    def draw(self, screen, font):
        pygame.draw.line(screen, (0, 0, 0),
                         (self.x, self.y),
                         (self.x + self.width, self.y), 3)

        pygame.draw.circle(screen, (100, 100, 255),
                           (int(self.knob_x), self.y), 8)

        value = self.get_value()
        text = font.render(f"Population Effect: {value:.2f}", True, (0, 0, 0))
        screen.blit(text, (self.x, self.y - 25))


# -------------------------------------------------
# Button Actions
# -------------------------------------------------
def increase_infection():
    global infection_rate
    infection_rate = min(5.0, infection_rate + 0.1)

def decrease_infection():
    global infection_rate
    infection_rate = max(0.0, infection_rate - 0.1)

def increase_recovery():
    global recovery_time
    recovery_time += 20

def decrease_recovery():
    global recovery_time
    recovery_time = max(20, recovery_time - 20)


# -------------------------------------------------
# Create Buttons & Slider
# -------------------------------------------------
buttons = [
    Button(10, 10, 120, 30, "Inf +", increase_infection),
    Button(10, 50, 120, 30, "Inf -", decrease_infection),
    Button(10, 90, 120, 30, "Rec +", increase_recovery),
    Button(10, 130, 120, 30, "Rec -", decrease_recovery),
]

controls = Controls(10, 200, 150)

# -------------------------------------------------
# Walls
# -------------------------------------------------
walls = [
    pygame.Rect(300, 150, 200, 5),
    pygame.Rect(100, 400, 5, 150),
    pygame.Rect(500, 350, 150, 5),
    pygame.Rect(200, 370, 150, 5),
    pygame.Rect(700, 250, 5, 150),
    pygame.Rect(750, 100, 5, 200),
    pygame.Rect(400, 400, 5, 200)
]

# -------------------------------------------------
# Create Population
# -------------------------------------------------
people = [Person(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(population)]

for i in random.sample(range(population), initial_infected):
    people[i].infect()

# -------------------------------------------------
# Main Loop
# -------------------------------------------------
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.check_click(event.pos)

        controls.handle_event(event)

    # Move + update people
    for person in people:
        person.move()
        person.update()

    # Infection logic
    population_effect = controls.get_value()

    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1 = people[i]
            p2 = people[j]

            if p1.state == Person.INFECTED and p2.state == Person.SUSCEPTIBLE:
                dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
                if dist < 10 and random.random() < infection_rate * population_effect:
                    p2.infect()

            elif p2.state == Person.INFECTED and p1.state == Person.SUSCEPTIBLE:
                dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
                if dist < 10 and random.random() < infection_rate * population_effect:
                    p1.infect()

    # Draw people
    for person in people:
        person.draw(screen)

    # Stats
    susceptible_count = sum(1 for p in people if p.state == Person.SUSCEPTIBLE)
    infected_count = sum(1 for p in people if p.state == Person.INFECTED)
    recovered_count = sum(1 for p in people if p.state == Person.RECOVERED)

    screen.blit(font.render(f"Susceptible: {susceptible_count}", True, (0, 150, 0)), (150, 80))
    screen.blit(font.render(f"Infected: {infected_count}", True, (200, 0, 0)), (150, 110))
    screen.blit(font.render(f"Recovered: {recovered_count}", True, (0, 100, 255)), (150, 140))

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, (50, 50, 50), wall)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Draw slider
    controls.draw(screen, font)

    # Display values
    screen.blit(font.render(f"Infection Rate: {infection_rate:.2f}", True, (0, 0, 0)), (150, 15))
    screen.blit(font.render(f"Recovery Time: {recovery_time}", True, (0, 0, 0)), (150, 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()