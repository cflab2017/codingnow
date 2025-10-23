import pygame

class Ball:
    def __init__(self, x, y, radius=20, collision_sound=None, particle_emitter=None):
        """
        공 객체를 초기화합니다.
        :param x, y: 공의 초기 중심 좌표
        :param radius: 공의 반지름
        :param collision_sound: 충돌 시 재생할 사운드 객체
        :param particle_emitter: 파티클 생성을 위한 ParticleEmitter 객체
        """
        self.pos = pygame.math.Vector2(x, y)
        self.prev_pos = pygame.math.Vector2(x, y) # 이전 위치 저장
        self.vel = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.color = (30, 30, 200)  # 파란색 계열 (이미지 로드 시 사용되지 않을 수 있음)
        self.gravity = pygame.math.Vector2(0, 150) # 중력 값
        self.is_launched = False # 공이 발사되었는지 여부
        self.MAX_SPEED = 1000 # 공의 최대 속도 제한
        self.collision_sound = collision_sound
        self.particle_emitter = particle_emitter

        # 공 이미지 로드 및 스케일 조정

        # 공 이미지 로드 및 스케일 조정
        original_image = pygame.image.load("assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=self.pos)

        # 충돌 마스크 생성 (이미지에서 생성)
        self.mask = pygame.mask.from_surface(self.image)

    def launch(self, power):
        """ 공을 발사합니다. """
        if not self.is_launched:
            # 고정된 높은 발사 속도 (디버깅용)
            launch_speed = 800 
            self.vel = pygame.math.Vector2(0, -launch_speed)
            self.is_launched = True

    def update(self, screen_width, screen_height, launch_lane_x, launch_lane_width, border_width, dt):
        """ 매 프레임마다 공의 상태를 업데이트합니다. """
        if not self.is_launched:
            self.rect.center = self.pos
            return

        self.prev_pos = self.pos.copy() # 현재 위치를 이전 위치로 저장

        # 중력 적용 (현재 0으로 설정됨)
        self.vel += self.gravity * dt

        # 속도 제한 적용
        if self.vel.length() > self.MAX_SPEED:
            self.vel.normalize_ip()
            self.vel *= self.MAX_SPEED
        # 위치 업데이트
        self.pos += self.vel * dt
        self.rect.center = self.pos
        # print(f"Ball.update received dt: {dt}")

    def draw(self, screen):
        """ 화면에 공을 그립니다. """
        screen.blit(self.image, self.rect)

    def reset(self, x, y):
        """ 공의 위치와 상태를 초기화합니다. """
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.is_launched = False

    def play_collision_sound(self):
        """ 충돌 사운드를 재생합니다. """
        if self.collision_sound:
            self.collision_sound.play()

    def emit_particles(self, position, color, count=10, size_range=(4, 10), lifetime_range=(0.2, 0.5), velocity_range=(50, 150)):
        """ 충돌 지점에서 파티클을 생성합니다. """
        if self.particle_emitter:
            self.particle_emitter.emit(position.x, position.y, count, color, size_range, lifetime_range, velocity_range)
