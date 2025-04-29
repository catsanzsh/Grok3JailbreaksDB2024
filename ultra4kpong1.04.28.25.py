import pygame
import random
import asyncio
import platform

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Create paddles and ball
left_paddle = pygame.Rect(20, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Initial velocities
ball_vel_x = -BALL_SPEED_X  # Start moving left
ball_vel_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

# Scores
score1 = 0
score2 = 0

# Font for scores
font = pygame.font.SysFont(None, 36)

def setup():
    global running
    running = True

def update_loop():
    global running, score1, score2, ball_vel_x, ball_vel_y

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s]:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP]:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        right_paddle.y += PADDLE_SPEED

    # Clamp paddle positions
    left_paddle.y = max(0, min(left_paddle.y, SCREEN_HEIGHT - left_paddle.height))
    right_paddle.y = max(0, min(right_paddle.y, SCREEN_HEIGHT - right_paddle.height))

    # Update ball position
    ball.x += ball_vel_x
    ball.y += ball_vel_y

    # Check collisions with top and bottom
    if ball.top < 0 or ball.bottom > SCREEN_HEIGHT:
        ball_vel_y = -ball_vel_y

    # Check collisions with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_vel_x = -ball_vel_x

    # Check if ball goes out of bounds
    if ball.right < 0:
        score2 += 1
        ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        ball_vel_x = BALL_SPEED_X  # to the right
        ball_vel_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
    elif ball.left > SCREEN_WIDTH:
        score1 += 1
        ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        ball_vel_x = -BALL_SPEED_X  # to the left
        ball_vel_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.rect(screen, WHITE, ball)
    # Draw center line
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 2)
    # Draw scores
    score1_text = font.render(str(score1), True, WHITE)
    score2_text = font.render(str(score2), True, WHITE)
    screen.blit(score1_text, (50, 50))
    screen.blit(score2_text, (SCREEN_WIDTH - 50 - score2_text.get_width(), 50))

    pygame.display.flip()
    clock.tick(FPS)

async def main():
    setup()
    while running:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())

pygame.quit()
