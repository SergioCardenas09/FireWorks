import pygame
import random
import math
import pygame_gui

class Particle:
    def __init__(self, x, y, color, speed, life, angle, main_particle=False, curvature="normal"):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 2
        self.angle = angle
        self.speed = speed
        self.life = life
        self.main_particle = main_particle
        self.curvature = curvature

    def move(self, gravity, wind_force):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed -= gravity  # Simulamos la gravedad
        self.speed += wind_force  # Agregamos la fuerza del viento
        if self.speed < 0:
            self.speed = 0
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


def explode(particles, x, y, color):
    # Determinar el tipo de explosión
    explosion_type = random.choice(["spiral", "star", "random"])
    
    if explosion_type == "spiral":
        generate_spiral_particles(particles, x, y, color)
    elif explosion_type == "star":
        generate_star_particles(particles, x, y, color)
    else:
        for _ in range(random.randint(20, 30)):
            speed = random.uniform(2, 5)
            life = random.randint(30, 60)
            angle = random.uniform(0, math.pi * 2)
            particles.append(Particle(x, y, color, speed, life, angle))


def generate_spiral_particles(particles, x, y, color):
    num_particles = 50
    radius = 10
    angle_increment = math.pi / 20
    for i in range(num_particles):
        angle = i * angle_increment
        speed = 5  
        life = random.randint(30, 60)
        particles.append(Particle(x + radius * math.cos(angle), y + radius * math.sin(angle), color, speed, life, angle))


def generate_star_particles(particles, x, y, color):
    num_points = 5
    radius = 30
    angle_increment = math.pi * 2 / num_points
    star_points = []
    for i in range(num_points * 2):
        angle = i * angle_increment
        if i % 2 == 0:
            length = radius
        else:
            length = radius / 2
        star_points.append((x + length * math.cos(angle), y + length * math.sin(angle)))
    
    for i in range(len(star_points)):
        speed = 3  
        life = random.randint(30, 60)
        angle = math.atan2(star_points[(i + 1) % len(star_points)][1] - star_points[i][1], star_points[(i + 1) % len(star_points)][0] - star_points[i][0])
        particles.append(Particle(star_points[i][0], star_points[i][1], color, speed, life, angle))


def generate_ellipse_particles(particles, x, y, color):
    num_points = 50
    major_axis = 40
    minor_axis = 20
    for i in range(num_points):
        angle = random.uniform(0, math.pi * 2)
        x_offset = major_axis * math.cos(angle)
        y_offset = minor_axis * math.sin(angle)
        speed = 2  
        life = random.randint(30, 60)
        particles.append(Particle(x + x_offset, y + y_offset, color, speed, life, angle))


def generate_smoke_trail(particles, x, y, color):
    num_particles = 50  
    for _ in range(num_particles):
        speed = random.uniform(0.1, 0.5)  
        angle = random.uniform(0, math.pi * 2)  
        life = random.randint(20, 40)  
        x_offset = random.uniform(-5, 5)  
        y_offset = random.uniform(-5, 5)  
        particles.append(Particle(x + x_offset, y + y_offset, color, speed, life, angle))


def update_rocket(rocket, time_delta):
    initial_speed = rocket.speed
    initial_angle = rocket.angle
    
    # Ajustar la velocidad de rotación del ángulo
    if rocket.curvature == "strong":  # Curvatura fuerte
        rocket.angle += time_delta * 0.5  # Ajustar el ángulo para la espiral más rápido
    else:
        rocket.angle += time_delta * 0.1  # Ajustar el ángulo para la espiral
    
    rocket.speed -= time_delta * 0.1  # Disminuir la velocidad gradualmente
    
    rocket.x += math.cos(rocket.angle) * rocket.speed
    rocket.y += math.sin(rocket.angle) * rocket.speed
    
    generate_smoke_trail(particles, rocket.x, rocket.y, (200, 200, 200))
    
    if rocket.life <= 0:
        explode(particles, rocket.x, rocket.y, rocket.color)
        particles.remove(rocket)


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulador de Fuegos Artificiales")

manager = pygame_gui.UIManager((800, 600))

particles = []
gravity = 0.1
wind_force = 0.1

gravity_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 50), (200, 20)),
                                                        start_value=gravity,
                                                        value_range=(0, 1),
                                                        manager=manager)
gravity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 50), (40, 20)),
                                            text='Gravedad',
                                            manager=manager)

wind_force_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 100), (200, 20)),
                                                           start_value=wind_force,
                                                           value_range=(-1, 1),
                                                           manager=manager)
wind_force_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 100), (40, 20)),
                                                text='Fuerza del Viento',
                                                manager=manager)

angle_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 150), (200, 20)),
                                                       start_value=0,
                                                       value_range=(0, math.pi * 2),
                                                       manager=manager)
angle_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 150), (40, 20)),
                                           text='Ángulo',
                                           manager=manager)

speed_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 200), (200, 20)),
                                                       start_value=5,
                                                       value_range=(0, 10),
                                                       manager=manager)
speed_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 200), (40, 20)),
                                           text='Velocidad',
                                           manager=manager)

running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(30) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

    screen.fill((0, 0, 0))

    manager.update(time_delta)
    manager.draw_ui(screen)

    gravity = gravity_slider.get_current_value()
    wind_force = wind_force_slider.get_current_value()
    angle = angle_slider.get_current_value()
    speed = speed_slider.get_current_value()

    if random.randint(0, 20) == 0:
        curvature = random.choice(["strong", "normal"])
        main_particle = Particle(random.randint(100, 700), 600, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), speed, random.randint(30, 60), angle, main_particle=True, curvature=curvature)
        particles.append(main_particle)

    for particle in particles:
        particle.move(gravity, wind_force)
        particle.draw(screen)
        
        if particle.main_particle:
            update_rocket(particle, time_delta)

    particles = [particle for particle in particles if particle.y >= 0 and particle.x >= 0 and particle.x <= 800 and particle.life > 0]

    pygame.display.flip()

pygame.quit()
