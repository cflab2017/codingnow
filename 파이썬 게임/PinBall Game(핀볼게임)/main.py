import pygame
import sys
from src.keyboard import Keyboard
from src.flipper import Flipper
from src.ball import Ball
from src.spring import Spring
from src.gate import Gate
from src.wall import Wall
from src.bumper import Bumper
from src.particle import ParticleEmitter
from src.blackhole import BlackHole

# --- 상수 정의 ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
FPS = 60
BORDER_WIDTH = 10
PHYSICS_TIME_STEP = 1.0 / 180.0 # 물리 업데이트를 위한 고정 시간 단계 (예: 180 FPS)

# --- 발사 통로 상수 ---
LAUNCH_LANE_WIDTH = 40
# LAUNCH_LANE_X는 화면 오른쪽에서 BORDER_WIDTH만큼 떨어진 곳에 위치
LAUNCH_LANE_X = SCREEN_WIDTH - LAUNCH_LANE_WIDTH - BORDER_WIDTH
LAUNCH_LANE_TOP = SCREEN_HEIGHT // 2 # 화면 중앙까지 올라옴

# --- 색상 정의 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (230, 230, 230)
GATE_COLOR = (200, 200, 0)

def main():
    """ 메인 게임 함수 """
    pygame.init()

    # 화면 설정
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pinball Game")
    clock = pygame.time.Clock()

    # 배경 이미지 로드 및 스케일 조정
    background_image = pygame.image.load("assets/background.png").convert()
    # Scale to fit the inner game area
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH - BORDER_WIDTH * 2, SCREEN_HEIGHT - BORDER_WIDTH * 2))

    # 충돌 효과음 로드
    collision_sound = pygame.mixer.Sound("assets/bounce.wav")

    # 키보드 입력 표시 객체 생성 (우측 상단 위치 지정)
    keyboard = Keyboard(460-10, 10+10)

    # 파티클 이미터 생성
    particle_emitter = ParticleEmitter()

    # 플리퍼 객체 생성 (V자 배치)
    # 플리퍼의 x, y 좌표는 절대 화면 좌표
    left_flipper = Flipper(x=260 + BORDER_WIDTH+20, y=770 + BORDER_WIDTH, side='left')
    right_flipper = Flipper(x=340 + BORDER_WIDTH-20, y=770 + BORDER_WIDTH, side='right')

    # 스프링 객체 생성
    # 스프링의 x, y 좌표는 절대 화면 좌표
    spring = Spring(LAUNCH_LANE_X, SCREEN_HEIGHT - 100, LAUNCH_LANE_WIDTH, 90)

    # 공 객체 생성 (스프링 위에 위치)
    # 공의 x, y 좌표는 절대 화면 좌표
    ball = Ball(LAUNCH_LANE_X + LAUNCH_LANE_WIDTH // 2, spring.rect.y - 10, collision_sound=collision_sound, particle_emitter=particle_emitter)

    # 게이트 객체 생성 (사용자 제공 좌표 사용)
    # 게이트의 x, y 좌표는 절대 화면 좌표
    gate = Gate(x=LAUNCH_LANE_X +20, y=LAUNCH_LANE_TOP - 10, width=LAUNCH_LANE_WIDTH + 10, height=8, angle=25)

    # 벽 객체 생성
    # 벽의 p1, p2 좌표는 절대 화면 좌표
    walls = [
        # 상단 벽
        Wall(pygame.math.Vector2(BORDER_WIDTH-1, BORDER_WIDTH), pygame.math.Vector2(SCREEN_WIDTH - BORDER_WIDTH+2, BORDER_WIDTH)),
        # 좌측 벽
        Wall(pygame.math.Vector2(BORDER_WIDTH, BORDER_WIDTH), pygame.math.Vector2(BORDER_WIDTH, SCREEN_HEIGHT - BORDER_WIDTH)),
        # 우측 벽 (발사 통로 제외)
        Wall(pygame.math.Vector2(SCREEN_WIDTH - BORDER_WIDTH , BORDER_WIDTH), pygame.math.Vector2(SCREEN_WIDTH - BORDER_WIDTH , SCREEN_HEIGHT - BORDER_WIDTH)),
        # 하단 벽 (임시, 나중에 게임 오버 영역으로 대체)
        Wall(pygame.math.Vector2(BORDER_WIDTH-1, SCREEN_HEIGHT - BORDER_WIDTH), pygame.math.Vector2(SCREEN_WIDTH - BORDER_WIDTH+2, SCREEN_HEIGHT - BORDER_WIDTH)),
        # 발사 통로 좌측 벽
        Wall(pygame.math.Vector2(LAUNCH_LANE_X , LAUNCH_LANE_TOP ), pygame.math.Vector2(LAUNCH_LANE_X , SCREEN_HEIGHT - BORDER_WIDTH )),
        # 발사 통로 우측 벽
        Wall(pygame.math.Vector2(LAUNCH_LANE_X + LAUNCH_LANE_WIDTH , LAUNCH_LANE_TOP), pygame.math.Vector2(LAUNCH_LANE_X + LAUNCH_LANE_WIDTH, SCREEN_HEIGHT - BORDER_WIDTH )),
        # 플리퍼 뒤 사선 라인 (좌측)
        Wall(pygame.math.Vector2(BORDER_WIDTH, 700), pygame.math.Vector2(left_flipper.pos.x - 75, left_flipper.pos.y -5 )),
        # 플리퍼 뒤 사선 라인 (우측)
        Wall(pygame.math.Vector2(LAUNCH_LANE_X, 700+20), pygame.math.Vector2(SCREEN_WIDTH - (left_flipper.pos.x - 90), left_flipper.pos.y -5 ))
    ]

    def reset_game():
        nonlocal score, game_over
        score = 0
        game_over = False
        ball.reset(LAUNCH_LANE_X + LAUNCH_LANE_WIDTH // 2, spring.rect.y - 10) # 공 초기 위치로
        spring.reset() # 스프링 초기화
        black_hole.event_triggered = False # 블랙홀 이벤트 초기화
        particle_emitter.particles.clear() # 파티클 초기화
        # 플리퍼 초기화 (각도 초기화)
        left_flipper.angle = left_flipper.start_angle
        left_flipper.is_active = False
        right_flipper.angle = right_flipper.start_angle
        right_flipper.is_active = False

    # --- 메인 게임 루프 ---
    running = True
    accumulator = 0.0
    score = 0 # 게임 점수
    game_over = False # 게임 오버 플래그

    # 범퍼 객체 생성 (10개, 크기 및 점수 다르게)
    # ... (existing bumper creation code)

    # 블랙홀 객체 생성 (플리퍼 아래 중앙)
    black_hole = BlackHole(SCREEN_WIDTH // 2+10, SCREEN_HEIGHT - 50, radius=30)
    bumpers = [
        Bumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, radius=25, score_value=200, planet_type='jupiter'), # Center top
        Bumper(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 3, radius=20, score_value=150, planet_type='saturn'), # Left mid
        Bumper(SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT // 3, radius=20, score_value=150, planet_type='mars'), # Right mid
        Bumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, radius=30, score_value=300, planet_type='earth'), # Center large
        Bumper(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50, radius=15, score_value=100, planet_type='venus'), # Bottom left
        Bumper(SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50, radius=15, score_value=100, planet_type='mercury'), # Bottom right
        Bumper(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 5, radius=18, score_value=120, planet_type='uranus'), # Top left
        Bumper(SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT // 5, radius=18, score_value=120, planet_type='neptune'), # Top right
        Bumper(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5, radius=22, score_value=180, planet_type='pluto'), # Lower left
        Bumper(SCREEN_WIDTH - SCREEN_WIDTH // 3, SCREEN_HEIGHT // 1.5, radius=22, score_value=180, planet_type='jupiter') # Lower right
    ]
    while running:
        dt = clock.tick(FPS) / 1000.0 # Convert milliseconds to seconds

        # 1. 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r: # 'R' 키로 게임 재시작
                    if game_over:
                        reset_game()

            if game_over: # 게임 오버 시에는 ESC 외의 다른 입력 무시
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                continue

            keyboard.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_flipper.activate()
                elif event.key == pygame.K_RIGHT:
                    right_flipper.activate()
                elif event.key == pygame.K_SPACE:
                    if not ball.is_launched:
                        spring.start_charging()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_flipper.deactivate()
                elif event.key == pygame.K_RIGHT:
                    right_flipper.deactivate()
                elif event.key == pygame.K_SPACE:
                    if not ball.is_launched:
                        power = spring.release()
                        ball.launch(power)

        # 2. 게임 상태 업데이트
        if not game_over:
            accumulator += dt

            while accumulator >= PHYSICS_TIME_STEP:
                left_flipper.update(PHYSICS_TIME_STEP)
                right_flipper.update(PHYSICS_TIME_STEP)
                spring.update(PHYSICS_TIME_STEP)
                ball.update(SCREEN_WIDTH, SCREEN_HEIGHT, LAUNCH_LANE_X, LAUNCH_LANE_WIDTH, BORDER_WIDTH, PHYSICS_TIME_STEP)
                particle_emitter.update(PHYSICS_TIME_STEP) # 파티클 업데이트

                # 공이 발사되지 않았을 때, 스프링 위에 위치하도록 조정
                if not ball.is_launched:
                    compression = (spring.power / spring.max_power) * (spring.rect.height / 2)
                    ball.pos.y = spring.rect.y - ball.radius + compression

                # 블랙홀 충돌 체크
                if black_hole.collide_ball(ball):
                    game_over = True

                # 충돌 처리
                left_flipper.collide_ball(ball)
                right_flipper.collide_ball(ball)
                gate.collide_ball(ball)
                for wall in walls:
                    wall.collide_ball(ball)

                # 범퍼 충돌 처리
                for bumper in bumpers:
                    score += bumper.collide_ball(ball)
                    bumper.update(PHYSICS_TIME_STEP)

                # 좌측 경계
                if ball.pos.x - ball.radius < BORDER_WIDTH:
                    ball.pos.x = BORDER_WIDTH + ball.radius
                    ball.vel.x *= -1 * 1.0 # 반발력 적용
                # 우측 경계
                if ball.pos.x + ball.radius > SCREEN_WIDTH - BORDER_WIDTH:
                    ball.pos.x = SCREEN_WIDTH - BORDER_WIDTH - ball.radius
                    ball.vel.x *= -1 * 1.0 # 반발력 적용
                # 상단 경계
                if ball.pos.y - ball.radius < BORDER_WIDTH:
                    ball.pos.y = BORDER_WIDTH + ball.radius
                    ball.vel.y *= -1 * 1.0 # 반발력 적용
                # 하단 경계 (일단 튕기도록 처리, 나중에 게임 오버 영역으로 대체)
                if ball.pos.y + ball.radius > SCREEN_HEIGHT - BORDER_WIDTH:
                    ball.pos.y = SCREEN_HEIGHT - BORDER_WIDTH - ball.radius
                    ball.vel.y *= -1 * 1.0 # 반발력 적용

                accumulator -= PHYSICS_TIME_STEP

        # 3. 화면 그리기
        screen.fill(WHITE) # 전체 화면을 하얀색으로 채움
        # 배경 이미지를 테두리 안쪽에 맞게 그리기
        screen.blit(background_image, (BORDER_WIDTH, BORDER_WIDTH))

        if not game_over:
            left_flipper.draw(screen)
            right_flipper.draw(screen)
            
            # 벽 그리기
            for wall in walls:
                wall.draw(screen)

            for bumper in bumpers:
                bumper.draw(screen)

            spring.draw(screen)
            gate.draw(screen)
            ball.draw(screen)
            particle_emitter.draw(screen) # 파티클 그리기

        # 디버깅 정보 표시 (점수만 남김)
        font = pygame.font.SysFont("malgungothic", 24)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10+10, 50))
        
        if game_over:
            game_over_font = pygame.font.SysFont("malgungothic", 72, bold=True)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0)) # Red color
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

            restart_font = pygame.font.SysFont("malgungothic", 36)
            restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255)) # White color
            restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_text_rect)
        else:        
            black_hole.draw(screen) # 블랙홀 그리기 (게임 오버 시에도 표시)
            keyboard.draw(screen)
                
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()