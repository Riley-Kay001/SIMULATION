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
infection_radius = 10
infection_rate = 0.5
recovery_time = 1000

# Movement
speed_multiplier = 1.0

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
        self.speed = random.uniform(0.5, 1.5)
        self.state = Person.SUSCEPTIBLE
        self.infection_time = 0

    def move(self):
        dx = random.uniform(-self.speed, self.speed) * speed_multiplier
        dy = random.uniform(-self.speed, self.speed) * speed_multiplier

        new_x = self.x + dx
        future_rect = pygame.Rect(new_x, self.y, self.radius * 2, self.radius * 2)
        if not any(wall.colliderect(future_rect) for wall in walls):
            self.x = new_x

        new_y = self.y + dy
        future_rect = pygame.Rect(self.x, new_y, self.radius * 2, self.radius * 2)
        if not any(wall.colliderect(future_rect) for wall in walls):
            self.y = new_y

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
# Buttons
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
# Controls (Slider)
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

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x + self.width, self.y), 3)
        pygame.draw.circle(screen, (100, 100, 255), (int(self.knob_x), self.y), 8)
        value = self.get_value()
        text = font.render(f"Population Effect: {value:.2f}", True, (0, 0, 0))
        screen.blit(text, (self.x, self.y - 25))

# -------------------------------------------------
# Button Actions
# -------------------------------------------------
def increase_infection():
    global infection_rate
    infection_rate += 0.1

def decrease_infection():
    global infection_rate
    infection_rate = max(0, infection_rate - 0.1)

def increase_recovery():
    global recovery_time
    recovery_time += 20

def decrease_recovery():
    global recovery_time
    recovery_time = max(20, recovery_time - 20)

def increase_radius():
    global infection_radius
    infection_radius += 2

def decrease_radius():
    global infection_radius
    infection_radius = max(2, infection_radius - 2)

def increase_speed():
    global speed_multiplier
    speed_multiplier += 0.2

def decrease_speed():
    global speed_multiplier
    speed_multiplier = max(0.2, speed_multiplier - 0.2)

# -------------------------------------------------
# UI Setup
# -------------------------------------------------
buttons = [
    Button(10, 10, 120, 30, "Inf +", increase_infection),
    Button(10, 50, 120, 30, "Inf -", decrease_infection),
    Button(10, 90, 120, 30, "Rec +", increase_recovery),
    Button(10, 130, 120, 30, "Rec -", decrease_recovery),
    Button(10, 170, 120, 30, "Rad +", increase_radius),
    Button(10, 210, 120, 30, "Rad -", decrease_radius),
    Button(10, 250, 120, 30, "Speed +", increase_speed),
    Button(10, 290, 120, 30, "Speed -", decrease_speed),
]

controls = Controls(10, 340, 150)

# Walls
walls = [
    pygame.Rect(300, 150, 200, 5),
    pygame.Rect(100, 400, 5, 150),
    pygame.Rect(200, 100, 5, 200),
    pygame.Rect(400, 300, 200, 5),
    pygame.Rect(600, 100, 5, 250),
    pygame.Rect(150, 250, 150, 5),
    pygame.Rect(500, 450, 200, 5),
]

# Population
people = [Person(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(population)]
for i in random.sample(range(population), initial_infected):
    people[i].infect()

# Stats history
history_infected = []
history_susceptible = []
history_recovered = []

# -------------------------------------------------
# Graph
# -------------------------------------------------
def draw_graph():
    graph_width = 200
    graph_height = 120
    base_x = WIDTH - graph_width - 10
    base_y = 10

        # Background box
    pygame.draw.rect(screen, (240, 240, 240), (base_x, base_y, graph_width, graph_height))
    pygame.draw.rect(screen, (0, 0, 0), (base_x, base_y, graph_width, graph_height), 2)

    max_points = min(len(history_infected), graph_width)

    for i in range(1, max_points):
        x1 = base_x + i - 1
        x2 = base_x + i

            # Scale values to fit graph height
        scale = graph_height / population

        pygame.draw.line(screen, (200, 0, 0),
            (x1, base_y + graph_height - history_infected[-max_points + i - 1] * scale),
            (x2, base_y + graph_height - history_infected[-max_points + i] * scale), 1)

        pygame.draw.line(screen, (0, 200, 0),
            (x1, base_y + graph_height - history_susceptible[-max_points + i - 1] * scale),
            (x2, base_y + graph_height - history_susceptible[-max_points + i] * scale), 1)

        pygame.draw.line(screen, (0, 100, 255),
            (x1, base_y + graph_height - history_recovered[-max_points + i - 1] * scale),
            (x2, base_y + graph_height - history_recovered[-max_points + i] * scale), 1)

        # Labels
    screen.blit(font.render("S", True, (0,200,0)), (base_x + 5, base_y + 5))
    screen.blit(font.render("I", True, (200,0,0)), (base_x + 25, base_y + 5))
    screen.blit(font.render("R", True, (0,100,255)), (base_x + 45, base_y + 5))

# -------------------------------------------------
# Main Loop
# -------------------------------------------------
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.check_click(event.pos)
        controls.handle_event(event)

    for p in people:
        p.move()
        p.update()

    population_effect = controls.get_value()

    for i in range(len(people)):
        for j in range(i+1, len(people)):
            p1, p2 = people[i], people[j]
            dist = math.hypot(p1.x - p2.x, p1.y - p2.y)

            if dist < infection_radius:
                if p1.state == Person.INFECTED and p2.state == Person.SUSCEPTIBLE:
                    if random.random() < infection_rate * population_effect:
                        p2.infect()
                elif p2.state == Person.INFECTED and p1.state == Person.SUSCEPTIBLE:
                    if random.random() < infection_rate * population_effect:
                        p1.infect()

    # Stats
    s = sum(1 for p in people if p.state == Person.SUSCEPTIBLE)
    i = sum(1 for p in people if p.state == Person.INFECTED)
    r = sum(1 for p in people if p.state == Person.RECOVERED)

    history_susceptible.append(s)
    history_infected.append(i)
    history_recovered.append(r)

    if len(history_infected) > 200:
        history_infected.pop(0)
        history_susceptible.pop(0)
        history_recovered.pop(0)

    for p in people:
        p.draw(screen)

    draw_graph()

    screen.blit(font.render(f"S: {s}", True, (0,200,0)), (150,80))
    screen.blit(font.render(f"I: {i}", True, (200,0,0)), (150,110))
    screen.blit(font.render(f"R: {r}", True, (0,100,255)), (150,140))

    screen.blit(font.render(f"Radius: {infection_radius}", True, (0,0,0)), (150,170))
    screen.blit(font.render(f"Speed: {speed_multiplier:.2f}", True, (0,0,0)), (150,200))

    for wall in walls:
        pygame.draw.rect(screen, (50,50,50), wall)

    for b in buttons:
        b.draw(screen)

    controls.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()