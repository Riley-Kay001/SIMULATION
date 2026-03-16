import random
import matplotlib.pyplot as plt

# Population settings
population = 200
initial_infected = 5

# Disease parameters
infection_rate = 0.05
recovery_rate = 0.01
days = 100

# States
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

# Initialize population
people = [SUSCEPTIBLE] * population

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