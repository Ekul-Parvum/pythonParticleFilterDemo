import matplotlib.pyplot as plt
import numpy as np
import random

# Cordinates of the target(Robot)
x = random.uniform(0, 100)
y = random.uniform(0, 100)

# Puts the point on the graph, and stores a variable representing that point
point, = plt.plot(x, y, "ro", markersize = 7)

# Put the guessed point on the graph:
y_estimate = 0
x_estimate = 0
estimated_point, = plt.plot(0, 0, "go", markersize = 5)

# 1. Randomly generate a bunch of particles
particles_x = []
particles_y = []
particles_weight = []
for i in range(1000):
    particles_x.append(random.uniform(0, 100))
    particles_y.append(random.uniform(0, 100))
    particles_weight.append(0)

particles = plt.scatter(particles_x, particles_y, s=2)

def partivle_filter(vel_x, vel_y):
    global particles_x, particles_y

    # Simulate inacuracies in expected vs real position
    # Or inacuracies in sensor data
    vel_x += random.uniform(-1, 1)
    vel_y += random.uniform(-1, 1)

    # -------[ 2. Predict next stage of particles: ]-------
    random_noise_range = 2
    for i in range(len(particles_x)):
        particles_x[i] += vel_x + random.uniform(-random_noise_range, random_noise_range)
        particles_y[i] += vel_y + random.uniform(-random_noise_range, random_noise_range)

    # -------[ 3. Update the weight of the particles ]-------
    # We will just give it the x and y of the target, and pretend its some distance to wall sensors
    for i in range(len(particles_x)):
        particles_weight[i] = 0

        # Calculate weight:
        diff = abs(particles_y[i] - y) + abs(particles_x[i] - x)
        particles_weight[i] += 1 / (diff + 1)

    # Normailse weight:
    weight_sum = sum(particles_weight)
    for i in range(len(particles_weight)):
        particles_weight[i] = particles_weight[i] / weight_sum

    # -------[ 4. Resample - Delete unlikely points ]-------
    # Get a list of indices pointing to indexes in particle_x
    # It randomly chooses indices based on the weight of the particle
    # So, particles weighted heavyer are more likely to be picked
    indexes = np.random.choice(
        len(particles_x),
        size=len(particles_x),
        p=particles_weight
    )

    # Now, going through and updating the
    particles_x = [particles_x[i] for i in indexes]
    particles_y = [particles_y[i] for i in indexes]

    # -------[ 5. Compute Estimate: ]-------
    y_estimate = 0
    x_estimate = 0
    weight_total = 0
    for i in range(len(particles_x)):
        y_estimate += particles_y[i] * particles_weight[i]
        x_estimate += particles_x[i] * particles_weight[i]
        weight_total += particles_weight[i]

    y_estimate = y_estimate / weight_total
    x_estimate = x_estimate / weight_total

    estimated_point.set_data([x_estimate], [y_estimate])

    # Update particles
    particles.set_offsets(list(zip(particles_x, particles_y)))

# Handle when a key is pressed
def key_pressed(event):
    # Grab x and y
    global x, y

    # Store velocity so we can give it to the particle filter
    xVelocity = 0
    yVelocity = 0

    # Handle key input
    if event.key == "up":
        yVelocity += 1
    elif event.key == "down":
        yVelocity -= 1
    elif event.key == "left":
        xVelocity -= 1
    elif event.key == "right":
        xVelocity += 1

    # Move point cords
    x += xVelocity
    y += yVelocity

    # Move the point to the new x, y cords
    point.set_data([x], [y])

    partivle_filter(xVelocity, yVelocity)

    # Redraw screen with new data
    plt.draw()

def main():


    plt.xlim(0, 100)
    plt.ylim(0, 100)

    # Grab an event from the window, and then plug it into our key_pressed
    plt.gcf().canvas.mpl_connect("key_press_event", key_pressed)

    plt.show()

main()