import pygame
import random

class Particle:
    def __init__(self, x, y, color, size, lifetime, velocity_range):
        self.pos = pygame.math.Vector2(x, y)
        self.color = color
        self.size = size
        self.lifetime = lifetime # in seconds
        self.current_lifetime = lifetime

        # Random velocity within a range
        angle = random.uniform(0, 2 * 3.14159) # Full circle
        speed = random.uniform(velocity_range[0], velocity_range[1])
        self.vel = pygame.math.Vector2(speed * pygame.math.Vector2(1, 0).rotate(angle))

    def update(self, dt):
        self.pos += self.vel * dt
        self.current_lifetime -= dt
        # Gradually shrink the particle
        self.size = max(0, self.size - (self.size / self.lifetime) * dt)

    def draw(self, screen):
        if self.current_lifetime > 0 and self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), int(self.size))

    def is_alive(self):
        return self.current_lifetime > 0 and self.size > 0

class ParticleEmitter:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count, color, size_range, lifetime_range, velocity_range):
        for _ in range(count):
            size = random.uniform(size_range[0], size_range[1])
            lifetime = random.uniform(lifetime_range[0], lifetime_range[1])
            self.particles.append(Particle(x, y, color, size, lifetime, velocity_range))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.is_alive()]
        for p in self.particles:
            p.update(dt)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
