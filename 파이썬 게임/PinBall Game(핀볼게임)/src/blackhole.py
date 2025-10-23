import pygame
import math
import random

class BlackHole:
    def __init__(self, x, y, radius):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = radius
        self.color = (10, 10, 10) # Very dark gray/black
        self.event_triggered = False # To ensure game over is triggered only once

    def draw(self, screen):
        # 블랙홀 본체 (가장 어두운 부분)
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

        # 내부 그림자/그라데이션 효과 (더 어둡게)
        for i in range(self.radius // 3):
            alpha = int(255 * (i / (self.radius // 3))) # 점점 투명해지도록
            darker_color = (max(0, self.color[0] - 20), max(0, self.color[1] - 20), max(0, self.color[2] - 20), alpha)
            pygame.draw.circle(screen, darker_color, (int(self.pos.x), int(self.pos.y)), self.radius - i)

        # 외부 광륜/그라데이션 효과 (약간 밝게)
        for i in range(self.radius // 2):
            alpha = int(255 * (1 - (i / (self.radius // 2)))) # 점점 투명해지도록
            light_color = (min(255, self.color[0] + 30), min(255, self.color[1] + 30), min(255, self.color[2] + 30), alpha)
            pygame.draw.circle(screen, light_color, (int(self.pos.x), int(self.pos.y)), self.radius + i, 1)

        # 미묘한 소용돌이 효과 (점들)
        for _ in range(50): # 50개의 작은 점
            angle = random.uniform(0, 2 * 3.14159)
            dist = random.uniform(self.radius * 0.5, self.radius * 1.5) # 블랙홀 주변에 분포
            x_offset = dist * math.cos(angle)
            y_offset = dist * math.sin(angle)
            
            # 시간에 따라 회전하는 것처럼 보이게
            current_time = pygame.time.get_ticks() / 1000.0 # seconds
            rotation_speed = 0.5 # 회전 속도
            rotated_x = x_offset * math.cos(current_time * rotation_speed) - y_offset * math.sin(current_time * rotation_speed)
            rotated_y = x_offset * math.sin(current_time * rotation_speed) + y_offset * math.cos(current_time * rotation_speed)

            point_color = (150, 150, 150, random.randint(50, 150)) # 회색 반투명
            point_radius = random.uniform(0.5, 1.5)
            pygame.draw.circle(screen, point_color, (int(self.pos.x + rotated_x), int(self.pos.y + rotated_y)), int(point_radius))

        # Optional: Add a subtle white outline or inner glow for effect
        # pygame.draw.circle(screen, (50, 50, 50), (int(self.pos.x), int(self.pos.y)), self.radius, 2)

    def collide_ball(self, ball):
        if not self.event_triggered:
            distance = self.pos.distance_to(ball.pos)
            if distance < self.radius + ball.radius:
                self.event_triggered = True
                return True # Collision detected, trigger game over
        return False
