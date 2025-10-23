import pygame

class Wall:
    def __init__(self, p1, p2, elasticity=1.0):
        """
        벽 객체를 초기화합니다.
        :param p1, p2: 벽을 구성하는 선분의 시작점과 끝점 (pygame.math.Vector2)
        :param elasticity: 벽의 반발 계수
        """
        self.p1 = p1
        self.p2 = p2
        self.elasticity = elasticity
        self.color = (0, 0, 0) # 검은색

        # 벽의 법선 벡터 계산
        self.normal = (self.p2 - self.p1).normalize().rotate(90) # 시계 방향 90도 회전

    def collide_ball(self, ball):
        # 공의 이전 위치와 현재 위치 사이의 이동 벡터
        ball_movement_vector = ball.pos - ball.prev_pos

        # 현재 위치에서 충돌 감지
        line_vec = self.p2 - self.p1
        ball_to_p1 = ball.pos - self.p1

        line_len_sq = line_vec.length_squared()
        if line_len_sq == 0:
            return False

        t_proj = ball_to_p1.dot(line_vec) / line_len_sq
        t_proj = max(0.0, min(1.0, t_proj))

        closest_point_on_wall = self.p1 + t_proj * line_vec
        dist_sq = (ball.pos - closest_point_on_wall).length_squared()

        if dist_sq < ball.radius**2: # 현재 위치에서 충돌 감지
            # 충돌이 감지되면, 공을 이전 위치로 되돌리고 서브 스텝으로 충돌을 해결합니다.
            ball.pos = ball.prev_pos.copy() # 이전 위치로 되돌리기
            ball.rect.center = ball.pos

            SUB_STEPS = 5 # 충돌 해결을 위한 서브 스텝 수
            sub_step_vector = ball_movement_vector / SUB_STEPS

            for _ in range(SUB_STEPS):
                ball.pos += sub_step_vector
                ball.rect.center = ball.pos

                # 서브 스텝마다 충돌 다시 확인
                ball_to_p1_sub = ball.pos - self.p1
                t_proj_sub = ball_to_p1_sub.dot(line_vec) / line_len_sq
                t_proj_sub = max(0.0, min(1.0, t_proj_sub))
                closest_point_on_wall_sub = self.p1 + t_proj_sub * line_vec
                dist_sq_sub = (ball.pos - closest_point_on_wall_sub).length_squared()

                if dist_sq_sub < ball.radius**2:
                    # 충돌 해결 (위치 보정 및 반사)
                    dist = (ball.pos - closest_point_on_wall_sub).length()
                    overlap = ball.radius - dist

                    normal = (ball.pos - closest_point_on_wall_sub).normalize()
                    ball.pos += normal * overlap
                    ball.rect.center = ball.pos

                    vel_along_normal = ball.vel.dot(normal)
                    if vel_along_normal < 0: # 벽을 향해 움직이는 경우에만 반사
                        ball.vel -= (1 + self.elasticity) * vel_along_normal * normal
                        ball.play_collision_sound()
                        ball.emit_particles(ball.pos, self.color) # 벽 색상으로 파티클 생성 # Add this line
                    return True # 충돌 해결 후 종료
            return False # 서브 스텝 후에도 충돌이 해결되지 않은 경우 (드물지만 가능)
        return False

    def draw(self, screen):
        """ 화면에 벽을 그립니다. """
        pygame.draw.line(screen, self.color, self.p1, self.p2, 4)
