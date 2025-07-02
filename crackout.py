# crackout.py

import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDLE_COLOR = (0, 150, 255) # A nice blue
BALL_COLOR = (255, 255, 0)   # A bright yellow
BRICK_COLORS = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0)]

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 10

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = -5 # Start moving up

# Brick properties
BRICK_WIDTH = 75
BRICK_HEIGHT = 25
BRICK_PADDING = 5
BRICK_ROWS = 5
BRICK_COLS = 10

# --- Game Classes ---

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - 40

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PADDLE_SPEED

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2])
        self.image.set_colorkey(BLACK) # Make background transparent
        pygame.draw.circle(self.image, BALL_COLOR, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.reset()
        
    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
        self.speed_y = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collision
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- Main Game Function ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crackout - The Python Brick Breaker")
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    bricks = pygame.sprite.Group()

    # Create game objects
    paddle = Paddle()
    ball = Ball()
    all_sprites.add(paddle, ball)

    # Create bricks
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_x = col * (BRICK_WIDTH + BRICK_PADDING) + (BRICK_PADDING * 4)
            brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + 50
            brick = Brick(brick_x, brick_y, random.choice(BRICK_COLORS))
            all_sprites.add(brick)
            bricks.add(brick)

    # Game variables
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    game_over = False
    game_won = False

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Quit with 'q'
                    running = False
                if game_over and event.key == pygame.K_r: # Restart with 'r'
                    main() # This restarts the whole game

        if not game_over:
            # Update
            all_sprites.update()

            # Ball collision with paddle
            if pygame.sprite.collide_rect(ball, paddle):
                ball.speed_y *= -1
                # Add slight angle change based on where it hits the paddle
                hit_pos = (ball.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
                ball.speed_x += hit_pos * 2

            # Ball collision with bricks
            hit_bricks = pygame.sprite.spritecollide(ball, bricks, True)
            if hit_bricks:
                ball.speed_y *= -1
                score += 10 * len(hit_bricks)
                if len(bricks) == 0:
                    game_won = True
                    game_over = True

            # Ball goes off bottom of screen
            if ball.rect.top > SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    ball.reset()
                else:
                    game_over = True

        # Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw Score and Lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

        # Game Over / Win Screen
        if game_over:
            over_font = pygame.font.Font(None, 74)
            if game_won:
                msg_text = over_font.render("YOU WIN!", True, (0, 255, 0))
            else:
                msg_text = over_font.render("GAME OVER", True, (255, 0, 0))
            
            restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
            
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40))

            screen.blit(msg_text, msg_rect)
            screen.blit(restart_text, restart_rect)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
