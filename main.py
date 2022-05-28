import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 204)
GREEN = (0, 128, 0)
RED = (190, 0, 0)
GREY = (80, 80, 80)
BLACK = (0, 0, 0)
PINK = (255, 128, 128)
LIGHT_BROWN = (150, 150, 0)
DARK_BROWN = (51, 51, 0)
DARK_BLUE = (50, 75, 225)
LIGHT_BLUE = (204, 255, 255)

FONT = pygame.font.SysFont("arial", 8)

class Planet:
    AU = 149.6e9        # distance of Earth to sun in meters
    G = 6.67428e-11     # gravitational constant
    SCALE = 15 / AU    
    TIMESTEP = 3600*12   # 1/2 day

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)


        # displays distance from sun in km but is visually noisy
        # if not self.sun:
        #     distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
        #     win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()))

        name_text = FONT.render(f"{self.name}", 1, WHITE)
        win.blit(name_text, (x - name_text.get_width()/2, y - self.radius * 2))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 1.4, YELLOW, 1.988e30 )
    sun.sun = True

    mercury = Planet("Mercury", -57.9e9, 0, .8, DARK_BROWN, .33e24)
    mercury.y_vel = 47400

    venus = Planet("Venus", -108.2e9, 0, 1.4, PINK, 4.8685e24)
    venus.y_vel = 35050

    earth = Planet("Earth", -149.6e9, 0, 1.6, GREEN, 5.9742e24)
    earth.y_vel = 29783

    mars = Planet("Mars", -228e9, 0, 1.2, RED, .642e24)
    mars.y_vel = 24077

    jupiter = Planet("Jupiter", -778.5e9, 0, 16.5, LIGHT_BROWN, 1898e24)
    jupiter.y_vel = 13000

    saturn = Planet("Saturn", -1432e9, 0, 14.0, LIGHT_YELLOW, 568e24)
    saturn.y_vel = 9700

    uranus = Planet("Uranus", -2867e9, 0, 6.4, LIGHT_BLUE, 86.8e24)
    uranus.y_vel = 6800

    neptune = Planet("Neptune", -4515e9, 0, 6.2, DARK_BLUE, 102e24,)
    neptune.y_vel = 5400

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

main()