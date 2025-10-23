
import pygame

class Flipper:
    def __init__(self, x, y, side='left'):
        """
        플리퍼 객체를 초기화합니다.
        :param x, y: 플리퍼의 회전 중심 좌표
        :param side: 'left' 또는 'right'
        """
        self.side = side
        self.width = 100
        self.height = 20
        self.color = (200, 50, 50) # 붉은색 계열

        # 원본 이미지 생성 (회전으로 인한 왜곡 방지)
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, self.color, (0, 0, self.width, self.height), border_radius=10)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)

        # 회전 관련 속성
        self.angle = 0
        self.rotation_speed = 300  # 플리퍼가 올라가는 속도 (degrees per second)
        self.current_angle_vel = 0 # 현재 각속도
        self.max_angle_vel = 600 # 최대 각속도
        self.is_active = False

        if self.side == 'left':
            self.original_image = pygame.transform.flip(self.original_image, True, False) # 수평 반전
            self.pivot_offset = pygame.math.Vector2(-self.width / 2, 0) # 뒤집힌 이미지의 왼쪽 끝을 회전축으로
            self.start_angle = -20  # 내려간 상태 (오른쪽 아래)
            self.end_angle = 40  # 올라간 상태 (오른쪽 위)
        else: # 'right'
            self.pivot_offset = pygame.math.Vector2(self.width / 2, 0) # 원본 이미지의 오른쪽 끝을 회전축으로
            self.start_angle = 20  # 내려간 상태 (왼쪽 아래)
            self.end_angle = -40  # 올라간 상태 (왼쪽 위)
        
        self.angle = self.start_angle

    def activate(self):
        """ 플리퍼를 활성화합니다. (키를 눌렀을 때) """
        self.is_active = True

    def deactivate(self):
        """ 플리퍼를 비활성화합니다. (키를 뗐을 때) """
        self.is_active = False

    def update(self, dt):
        """ 매 프레임마다 플리퍼의 각도를 업데이트합니다. """
        previous_angle = self.angle

        # 목표 각도 설정
        target_angle = self.start_angle
        if self.is_active:
            target_angle = self.end_angle

        # 목표 각도를 향해 회전
        if self.angle < target_angle:
            self.angle = min(target_angle, self.angle + self.rotation_speed * dt)
        elif self.angle > target_angle:
            self.angle = max(target_angle, self.angle - self.rotation_speed * dt)

        # 현재 각속도 계산
        if dt > 0:
            self.current_angle_vel = (self.angle - previous_angle) / dt
        else:
            self.current_angle_vel = 0

        # 이미지 회전
        self.rotate()

    def get_end_point(self):
        """ 플리퍼의 끝점 (공과 충돌하는 부분)을 반환합니다. """
        # 플리퍼의 회전 중심에서 끝점까지의 벡터
        if self.side == 'left':
            # 왼쪽 플리퍼는 오른쪽 끝이 공과 충돌
            end_offset = pygame.math.Vector2(self.width / 2, 0).rotate(self.angle)
        else:
            # 오른쪽 플리퍼는 왼쪽 끝이 공과 충돌
            end_offset = pygame.math.Vector2(-self.width / 2, 0).rotate(self.angle)
        return self.pos + self.pivot_offset + end_offset

    def rotate(self):
        """ 현재 각도를 기준으로 이미지를 회전시킵니다. """
        # 원본 이미지를 현재 각도로 회전
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        
        # 회전된 pivot 오프셋 계산
        rotated_offset = self.pivot_offset.rotate(self.angle)
        
        # 최종 rect 위치 계산
        self.rect = rotated_image.get_rect(center=self.pos + rotated_offset)
        self.image = rotated_image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        """ 화면에 플리퍼를 그립니다. """
        screen.blit(self.image, self.rect)

    def collide_ball(self, ball):
        """ 공과 플리퍼의 충돌을 처리합니다. """
        # 마스크 기반 충돌 감지
        # ball.rect의 top-left를 기준으로 flipper.rect의 top-left까지의 오프셋
        offset_x = int(self.rect.x - ball.rect.x)
        offset_y = int(self.rect.y - ball.rect.y)

        overlap_point = ball.mask.overlap(self.mask, (offset_x, offset_y))

        if overlap_point:
            # 충돌 발생
            # 충돌 지점 근사 (공의 중심에서 오버랩 지점까지의 벡터)
            # 오버랩 지점은 ball.mask 기준이므로, flipper.rect 기준으로 변환
            collision_point_on_flipper = pygame.math.Vector2(overlap_point[0] + ball.rect.x, overlap_point[1] + ball.rect.y)

            # 플리퍼의 표면 법선 벡터 계산
            # 플리퍼의 현재 각도를 기반으로 법선 벡터를 근사
            # 플리퍼의 긴 변에 수직인 벡터를 사용
            if self.side == 'left':
                # 왼쪽 플리퍼는 시계 반대 방향으로 회전 (각도 증가)
                # 법선은 플리퍼의 표면에서 바깥쪽을 향해야 함
                normal = pygame.math.Vector2(0, -1).rotate(self.angle + 90) # 플리퍼의 긴 변에 수직
            else: # 'right'
                # 오른쪽 플리퍼는 시계 방향으로 회전 (각도 감소)
                # 법선은 플리퍼의 표면에서 바깥쪽을 향해야 함
                normal = pygame.math.Vector2(0, -1).rotate(self.angle - 90) # 플리퍼의 긴 변에 수직

            # 공이 플리퍼 안으로 파고드는 것을 방지 (위치 보정)
            # 간단하게 공을 법선 방향으로 밀어냅니다.
            # 정확한 오버랩 깊이를 알기 어렵기 때문에, 임의의 값으로 밀어냅니다.
            ball.pos += normal * 2 # 임의의 값으로 밀어냄
            ball.rect.center = ball.pos

            # 상대 속도 계산
            # 플리퍼의 접선 속도 (회전으로 인한 속도)
            # 충돌 지점을 플리퍼의 끝점으로 근사
            flipper_start = self.pos + self.pivot_offset
            flipper_end = self.get_end_point()
            
            # 충돌 지점을 플리퍼의 끝점으로 근사
            # 더 정확하게는 collision_point_on_flipper를 사용해야 하지만, 복잡하므로 단순화
            closest_point = flipper_end 

            r = closest_point - flipper_start # 회전 중심에서 충돌 지점까지의 벡터
            tangential_vel = pygame.math.Vector2(0, 0)
            if r.length_squared() > 0:
                # 플리퍼의 각속도 방향에 따라 접선 속도 계산
                # 각속도 방향은 side에 따라 다름
                if self.side == 'left':
                    # 왼쪽 플리퍼는 각도가 증가할 때 위로 올라감 (반시계 방향)
                    # 접선 속도는 r 벡터에 수직이고 각속도 방향
                    tangential_vel = pygame.math.Vector2(-r.y, r.x).normalize() * (self.current_angle_vel * (r.length() / 50))
                else:
                    # 오른쪽 플리퍼는 각도가 감소할 때 위로 올라감 (시계 방향)
                    # 접선 속도는 r 벡터에 수직이고 각속도 방향
                    tangential_vel = pygame.math.Vector2(r.y, -r.x).normalize() * (self.current_angle_vel * (r.length() / 50))

            relative_vel = ball.vel - tangential_vel

            # 충돌 법선에 대한 상대 속도 성분
            vel_along_normal = relative_vel.dot(normal)

            # 이미 멀어지고 있다면 처리하지 않음
            if vel_along_normal > 0:
                return False

            # 반발 계수 (탄성) 적용
            e = 0.9 # 예시 값

            # 충격량 계산
            impulse_magnitude = -(1 + e) * vel_along_normal
            impulse = impulse_magnitude * normal

            # 공의 속도 업데이트
            ball.vel += impulse
            ball.play_collision_sound()
            ball.emit_particles(ball.pos, self.color) # 플리퍼 색상으로 파티클 생성

            # 플리퍼의 움직임으로 인한 추가적인 힘 (각속도 반영)
            # 플리퍼가 올라가는 방향으로 공에 힘을 가함
            # current_angle_vel이 양수일 때만 힘을 가하도록 수정
            if self.is_active and self.current_angle_vel > 0: # 플리퍼가 올라가는 중일 때만
                flipper_boost = self.current_angle_vel * 0.8 # 임의의 스케일 팩터
                ball.vel += normal * flipper_boost

            return True
        return False
