import pygame

class Gate:
    def __init__(self, x, y, width, height, angle=20):
        """
        경사진 단방향 게이트 객체를 초기화합니다.
        :param x, y: 게이트의 중심 좌표
        :param width, height: 게이트의 크기
        :param angle: 게이트의 경사각
        """
        self.pos = pygame.math.Vector2(x, y)
        self.angle = angle
        self.color = (200, 200, 0) # 노란색 계열

        # 원본 이미지 생성
        self.original_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original_image.fill(self.color)
        
        # 이미지를 회전하고 마스크 생성
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # 충돌 법선 벡터 계산 (오류 수정: rotate(-angle) -> rotate(angle))
        # pygame.transform.rotate는 반시계방향 회전이므로, 법선벡터도 동일하게 반시계방향으로 회전시켜야 함
        self.normal = pygame.math.Vector2(0, -1).rotate(self.angle).normalize()

    def collide_ball(self, ball):
        """
        공과 게이트의 충돌을 처리합니다. (수동 반사 로직)
        """
        offset_x = ball.rect.x - self.rect.x
        offset_y = ball.rect.y - self.rect.y

        if self.mask.overlap(ball.mask, (offset_x, offset_y)):
            # 1. 물리 공식을 이용해 반사 벡터를 직접 계산합니다.
            # v' = v - 2 * (v . n) * n
            dot_product = ball.vel.dot(self.normal)
            
            # 공이 게이트로 "파고드는" 경우에만 반사시킵니다.
            # dot_product < 0 은 두 벡터가 90도 이상 차이남을 의미 (서로 다른 방향)
            if dot_product < 0:
                new_vel = ball.vel - 2 * dot_product * self.normal
                ball.vel = new_vel
                
                # 2. 반발 계수를 적용하여 에너지를 약간 손실시킵니다.
                ball.vel *= 0.8
                ball.play_collision_sound()
                ball.emit_particles(ball.pos, self.color) # 게이트 색상으로 파티클 생성 # Add this line

            # 3. 충돌 해결: 공이 끼이지 않도록 법선 방향으로 확실하게 밀어냅니다.
            ball.pos += self.normal * 3
            ball.rect.center = ball.pos

            return True
        return False

    def draw(self, screen):
        """ 화면에 게이트를 그립니다. """
        screen.blit(self.image, self.rect)