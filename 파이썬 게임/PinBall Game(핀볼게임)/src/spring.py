import pygame

class Spring:
    def __init__(self, x, y, width, height):
        """
        스프링 객체를 초기화합니다.
        :param x, y: 스프링의 초기 위치 (상단 좌표)
        :param width, height: 스프링의 크기
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (150, 150, 150) # 회색
        self.power = 0
        self.max_power = 100
        self.is_charging = False
        self.charge_speed = 200 # Increased charge speed

    def start_charging(self):
        """ 파워 충전을 시작합니다. """
        self.is_charging = True

    def release(self):
        """ 스프링을 발사하고 현재 파워를 반환합니다. """
        launch_power = self.power
        self.power = 0
        self.is_charging = False
        return launch_power

    def update(self, dt):
        """ 매 프레임마다 스프링의 상태를 업데이트합니다. """
        if self.is_charging:
            self.power = min(self.max_power, self.power + self.charge_speed * dt)

    def reset(self):
        """ 스프링의 상태를 초기화합니다. """
        self.power = 0
        self.is_charging = False

    def draw(self, screen):
        """ 화면에 스프링과 파워 게이지를 그립니다. """
        # 스프링 그리기 (압축 효과)
        compression = (self.power / self.max_power) * (self.rect.height / 2)
        spring_rect = pygame.Rect(self.rect.x, self.rect.y + compression, self.rect.width, self.rect.height - compression)
        pygame.draw.rect(screen, self.color, spring_rect)
        pygame.draw.rect(screen, (0,0,0), spring_rect, 2) # 테두리

        # 파워 게이지 그리기
        if self.is_charging or self.power > 0:
            gauge_bg_rect = pygame.Rect(self.rect.x - 25, self.rect.y, 20, self.rect.height)
            pygame.draw.rect(screen, (200, 200, 200), gauge_bg_rect) # 배경

            gauge_height = (self.power / self.max_power) * self.rect.height
            gauge_rect = pygame.Rect(self.rect.x - 25, self.rect.y + self.rect.height - gauge_height, 20, gauge_height)
            
            # 파워에 따라 색상 변경 (초록 -> 노랑 -> 빨강)
            gauge_color = (0, 255, 0)
            if self.power > self.max_power * 0.5:
                gauge_color = (255, 255, 0)
            if self.power > self.max_power * 0.8:
                gauge_color = (255, 0, 0)

            pygame.draw.rect(screen, gauge_color, gauge_rect)
            pygame.draw.rect(screen, (0,0,0), gauge_bg_rect, 2) # 테두리
