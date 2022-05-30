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
BLACK = (0, 0, 0)
PINK = (255, 128, 128)
LIGHT_BROWN = (150, 150, 0)
DARK_BROWN = (51, 51, 0)
DARK_BLUE = (50, 75, 225)
LIGHT_BLUE = (204, 255, 255)

AU = 149.6e9        # distance of Earth to sun in meters
G = 6.67428e-11     # gravitational constant
scale = 1e-9    
TIMESTEP = 3600*12   # 1/2 day

class Planet:
    def __init__(self, name, x, y, diameter, color, mass, orbital_velocity=0):
        self.name = name
        self.x = x
        self.y = y
        self.radius = diameter / 2
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = orbital_velocity

    def draw(self, win):
        font = pygame.font.SysFont("arial", 22)
        x = self.x * scale + WIDTH / 2
        y = self.y * scale + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * scale + WIDTH / 2
                y = y * scale + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            name_text = font.render(f"{self.name}", 1, WHITE)
            win.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_width()/2))

        pygame.draw.circle(win, self.color, (x, y), self.radius*scale*50000)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance ** 2
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

        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 1392700, YELLOW, 1.988e30)
    sun.sun = True

    mercury = Planet("Mercury", -57.9e9, 0, 4879, DARK_BROWN, .33e24, 47400)
    venus = Planet("Venus", -108.2e9, 0, 12104, PINK, 4.8685e24, 35050)
    earth = Planet("Earth", -149.6e9, 0, 12756, GREEN, 5.9742e24, 29783)
    mars = Planet("Mars", -228e9, 0, 6792, RED, .642e24, 24077)
    jupiter = Planet("Jupiter", -778.5e9, 0, 142984, LIGHT_BROWN, 1898e24, 13000)
    saturn = Planet("Saturn", -1432e9, 0, 120536, LIGHT_YELLOW, 568e24, 9700)
    uranus = Planet("Uranus", -2867e9, 0, 51118, LIGHT_BLUE, 86.8e24, 6800)
    neptune = Planet("Neptune", -4515e9, 0, 49528, DARK_BLUE, 102e24, 5400)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEWHEEL:
                global scale
                if event.y == 1:
                    scale += scale * .1
                elif event.y == -1:
                    scale -= scale * .1

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

main()