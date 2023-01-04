import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

nPartikel = 100
dimensionen = 2
Grenze_min = -100.0
Grenze_max = 100.0
maxIt = 30
images = []
w = 0.9

def main():
  gbest, gbest_Z = pso(nPartikel, dimensionen, Grenze_min, Grenze_max, maxIt)
  x_min, y_min, z_min = Optimum()
  print("beste ermittelte Position(x, y):",gbest, "z:",gbest_Z,"\ntatsächliches Optimum:",x_min,"y:",y_min,"z:",z_min)
  psoAnim = animation.ArtistAnimation(fig, images)
  psoAnim.save('./pso-Animation.gif', writer='pillow')

def func(x, y):
  z = 50*x**2 + 50*y**2 + 1.5
  return z

def Optimum():
  x, y = np.array(np.meshgrid(np.linspace(0,5,100), np.linspace(0,5,100)))
  z = func(x, y)
  x_min = x.ravel()[z.argmin()]
  y_min = y.ravel()[z.argmin()] 
  z_min = func(x_min, y_min)
  return x_min, y_min, z_min

def pso(nPartikel, dimensionen, Grenze_min, Grenze_max, maxIt):
  # Initialisierung
  particles = [[random.uniform(Grenze_min, Grenze_max) for _ in range(dimensionen)] for _ in range(nPartikel)]
  pbest = particles
  pbest_Z = [func(p[0],p[1]) for p in particles]  # Tauglichkeit der einzelnen Partikel 
  gbest_Z = np.argmin(pbest_Z)  # Index des besten Wertes in der Liste
  gbest = pbest[gbest_Z]
  velocity = [[0.0 for _ in range(dimensionen)] for _ in range(nPartikel)]
  current_w = w
  # PSO-Loop
  for t in range(maxIt):
    image = ax.scatter3D([particles[n][0] for n in range(nPartikel)],
                         [particles[n][1] for n in range(nPartikel)],
                         [func(particles[n][0],particles[n][1]) for n in range(nPartikel)], color = 'orangered')
    images.append([image])
    for n in range(nPartikel):
        # Update Geschwindigkeit 
        velocity[n] = update_velocity(particles[n], velocity[n], pbest[n], gbest, current_w)
        # update Position 
        particles[n] = update_position(particles[n], velocity[n])
    current_w = (w-0.4)/(t+1)
    pbest_Z = [func(p[0],p[1]) for p in particles]
    gbest_Z = np.argmin(pbest_Z)
    gbest = pbest[gbest_Z]
  return gbest, min(pbest_Z)

def update_velocity(particle, velocity, pbest, gbest, current_w):
  num_particle = len(particle)
  new_velocity = np.array([0.0 for i in range(num_particle)])
  r1 = random.uniform(0, 1)
  r2 = random.uniform(0, 1)
  c1 = c2 = 2
  for i in range(num_particle):
    new_velocity[i] = current_w*velocity[i] + c1*r1*(pbest[i]-particle[i]) + c2*r2*(gbest[i]-particle[i])
  return new_velocity

def update_position(position, velocity):
  new_position  = position + velocity
  return new_position

# Graph 
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection = '3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
x = np.linspace(Grenze_min, Grenze_max, 100)
y = np.linspace(Grenze_min, Grenze_max, 100)
X, Y = np.meshgrid(x, y)
Z = func(X, Y)
ax.plot_wireframe(X, Y, Z, color='steelblue', linewidth = 0.4)

if __name__ == "__main__":
  main()