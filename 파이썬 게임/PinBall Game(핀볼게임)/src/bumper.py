import pygame

class Bumper:
    def __init__(self, x, y, radius=20, score_value=100, elasticity=1.5, planet_type=None):
        self.pos = pygame.math.Vector2(x, y)
        self.original_radius = radius
        self.radius = radius # Current radius, will change with scaling
        self.color = (255, 215, 0)  # Gold color (default, will be overridden by image)
        self.score_value = score_value
        self.elasticity = elasticity
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.is_flashing = False
        self.flash_timer = 0.0
        self.flash_duration = 0.5 # seconds

        self.current_scale = 1.0
        self.target_scale = 1.0
        self.scale_speed = 10.0 # How fast it scales up/down

        self.planet_image = None
        if planet_type:
            try:
                image_path = f"assets/{planet_type}.png"
                original_image = pygame.image.load(image_path).convert_alpha()
                self.planet_image = pygame.transform.scale(original_image, (self.original_radius * 2, self.original_radius * 2))
            except pygame.error:
                print(f"Warning: Could not load image for {planet_type}. Using default circle.")
                self.planet_image = None

    def collide_ball(self, ball):
        # 공의 이전 위치와 현재 위치 사이의 이동 벡터
        ball_movement_vector = ball.pos - ball.prev_pos

        # 현재 위치에서 충돌 감지
        distance = self.pos.distance_to(ball.pos)

        if distance < self.radius + ball.radius: # 현재 위치에서 충돌 감지
            # 충돌이 감지되면, 공을 이전 위치로 되돌리고 서브 스텝으로 충돌을 해결합니다.
            ball.pos = ball.prev_pos.copy() # 이전 위치로 되돌리기
            ball.rect.center = ball.pos

            SUB_STEPS = 5 # 충돌 해결을 위한 서브 스텝 수
            sub_step_vector = ball_movement_vector / SUB_STEPS

            score_awarded = 0

            for _ in range(SUB_STEPS):
                ball.pos += sub_step_vector
                ball.rect.center = ball.pos

                # 서브 스텝마다 충돌 다시 확인
                distance_sub = self.pos.distance_to(ball.pos)

                if distance_sub < self.radius + ball.radius:
                    # 충돌 해결 (위치 보정 및 반사)
                    normal = (ball.pos - self.pos).normalize()

                    overlap = (self.radius + ball.radius) - distance_sub
                    ball.pos += normal * overlap
                    ball.rect.center = ball.pos

                    relative_velocity = ball.vel
                    vel_along_normal = relative_velocity.dot(normal)

                    if vel_along_normal > 0:
                        return score_awarded # 이미 멀어지고 있다면 점수 반환

                    impulse_scalar = -(1 + self.elasticity) * vel_along_normal
                    ball.vel += impulse_scalar * normal
                    ball.play_collision_sound()
                    ball.emit_particles(ball.pos, self.color, count=20, size_range=(5, 12), lifetime_range=(0.3, 0.6), velocity_range=(100, 250)) # 범퍼 색상으로 파티클 생성

                    self.is_flashing = True
                    self.flash_timer = self.flash_duration
                    self.target_scale = 1.5 # 충돌 시 1.5배 확대 (increased from 1.2)

                    score_awarded = self.score_value # 충돌 시 점수 부여
                    return score_awarded # 충돌 해결 후 종료
            return score_awarded # 서브 스텝 후에도 충돌이 해결되지 않은 경우 (드물지만 가능)
        return 0

    def update(self, dt):
        # print(f"Bumper update: is_flashing={self.is_flashing}, flash_timer={self.flash_timer:.2f}, current_scale={self.current_scale:.2f}, target_scale={self.target_scale:.2f}")
        # 플래싱 효과 업데이트
        if self.is_flashing:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.is_flashing = False
                # print("is_flashing set to False")

        # 스케일링 효과 업데이트
        if self.current_scale < self.target_scale:
            self.current_scale += self.scale_speed * dt
            if self.current_scale >= self.target_scale:
                self.current_scale = self.target_scale
                if self.current_scale >= 1.5: # 확대 완료 시
                    self.target_scale = 0.95 # 오버슈트 시작
                    # print(f"Scale up complete, setting target_scale to {self.target_scale}")
                elif self.current_scale <= 0.95: # 오버슈트 완료 시
                    self.target_scale = 1.0 # 최종 크기로 복귀
                    # print(f"Overshoot complete, setting target_scale to {self.target_scale}")
        elif self.current_scale > self.target_scale:
            self.current_scale -= self.scale_speed * dt
            if self.current_scale <= self.target_scale:
                self.current_scale = self.target_scale
                if self.current_scale <= 0.95: # 오버슈트 완료 시
                    self.target_scale = 1.0 # 최종 크기로 복귀
                    # print(f"Overshoot complete (down), setting target_scale to {self.target_scale}")
        
        self.radius = int(self.original_radius * self.current_scale)
        self.rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self, screen):
        current_color = self.color
        if self.is_flashing:
            current_color = (255, 255, 255) # 흰색으로 플래시

        if self.planet_image:
            # 외곽선 그리기 (검은색)
            outline_radius = self.radius + 2 # 행성보다 약간 크게
            pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), outline_radius, 2)

            # 현재 스케일에 맞춰 이미지 크기 조정
            scaled_image = pygame.transform.scale(self.planet_image, (self.radius * 2, self.radius * 2))
            scaled_rect = scaled_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            screen.blit(scaled_image, scaled_rect)
            if self.is_flashing:
                # 플래싱 효과를 위해 흰색 원을 그립니다.
                flash_alpha = int(180 * (self.flash_timer / self.flash_duration)) # 시간에 따라 알파값 조절 (최대 180)
                # if self.is_flashing: print(f"Drawing flash: flash_alpha={flash_alpha}")
                if flash_alpha > 0:
                    flash_surface = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)
                    pygame.draw.circle(flash_surface, (255, 255, 255, flash_alpha), (flash_surface.get_width() // 2, flash_surface.get_height() // 2), self.radius + 5)
                    flash_rect = flash_surface.get_rect(center=(int(self.pos.x), int(self.pos.y)))
                    screen.blit(flash_surface, flash_rect)
        else:
            pygame.draw.circle(screen, current_color, (int(self.pos.x), int(self.pos.y)), self.radius)
            pygame.draw.circle(screen, (0, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius, 2) # Outline