import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_GAP = 10

# Define paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 5

# Define ball radius
BALL_RADIUS = 10
BALL_SPEED = 3

# Define power-up types
POWERUP_SIZE = 20
POWERUP_SPEED = 2
POWERUP_TYPES = ["expand", "shrink"]

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Brick Game")

clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Function to draw bricks on the screen
def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(window, BLUE, brick)

# Function to draw the paddle
def draw_paddle(paddle_x):
    pygame.draw.rect(window, RED, (paddle_x, WINDOW_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the ball
def draw_ball(ball_x, ball_y):
    pygame.draw.circle(window, WHITE, (ball_x, ball_y), BALL_RADIUS)

# Function to draw power-ups
def draw_powerups(powerups):
    for powerup in powerups:
        pygame.draw.rect(window, YELLOW, powerup[0])

# Function to update the game screen
def update_screen(bricks, paddle_x, ball_x, ball_y, powerups, score, level):
    window.fill(BLACK)
    draw_bricks(bricks)
    draw_paddle(paddle_x)
    draw_ball(ball_x, ball_y)
    draw_powerups(powerups)
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Level: {level}", WINDOW_WIDTH - 150, 10)
    pygame.display.update()

# Function to display text on the screen
def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    window.blit(text_surface, (x, y))

# Function to handle collisions between the ball and bricks
def handle_brick_collisions(bricks, ball_x, ball_y, ball_dx, ball_dy, powerups, score):
    for brick in bricks:
        if brick.collidepoint(ball_x, ball_y + BALL_RADIUS) or brick.collidepoint(ball_x, ball_y - BALL_RADIUS):
            bricks.remove(brick)
            ball_dy *= -1
            score += 10
            if random.random() < 0.1:  # 10% chance of generating a power-up
                generate_powerup(brick, powerups)
            break
        elif brick.collidepoint(ball_x + BALL_RADIUS, ball_y) or brick.collidepoint(ball_x - BALL_RADIUS, ball_y):
            bricks.remove(brick)
            ball_dx *= -1
            score += 10
            if random.random() < 0.1:  # 10% chance of generating a power-up
                generate_powerup(brick, powerups)
            break
    return ball_dx, ball_dy, score

# Function to handle collisions between the ball and paddle
def handle_paddle_collision(paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy):
    if ball_y + BALL_RADIUS >= paddle_y and paddle_x - BALL_RADIUS <= ball_x <= paddle_x + PADDLE_WIDTH + BALL_RADIUS:
        ball_dy *= -1
        if ball_x < paddle_x or ball_x > paddle_x + PADDLE_WIDTH:
            ball_dx *= -1
    return ball_dx, ball_dy

# Function to handle collisions between the ball and power-ups
def handle_powerup_collision(powerups, paddle_x, paddle_y, paddle_width):
    for powerup in powerups:
        if powerup[0].colliderect(pygame.Rect(paddle_x, paddle_y, paddle_width, PADDLE_HEIGHT)):
            powerups.remove(powerup)
            return True
    return False

# Function to generate a power-up
def generate_powerup(brick, powerups):
    powerup_x = brick.x + brick.width // 2 - POWERUP_SIZE // 2
    powerup_y = brick.y + brick.height // 2 - POWERUP_SIZE // 2
    powerup_type = random.choice(POWERUP_TYPES)
    powerup = pygame.Rect(powerup_x, powerup_y, POWERUP_SIZE, POWERUP_SIZE)
    powerups.append((powerup, powerup_type))

# Function to move and update power-ups
def move_powerups(powerups):
    for powerup in powerups:
        powerup[0].y += POWERUP_SPEED

# Function to check if a power-up has reached the bottom of the screen
def check_powerup_bottom(powerups):
    for powerup in powerups:
        if powerup[0].y >= WINDOW_HEIGHT:
            powerups.remove(powerup)

# Function to run the game
def run_game():
    global PADDLE_WIDTH  # Declare PADDLE_WIDTH as a global variable

    # Create initial paddle position
    paddle_x = WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = WINDOW_HEIGHT - PADDLE_HEIGHT

    # Create initial ball position and direction
    ball_x = random.randint(BALL_RADIUS, WINDOW_WIDTH - BALL_RADIUS)
    ball_y = WINDOW_HEIGHT // 2
    ball_dx = random.choice([-2, 2])
    ball_dy = -BALL_SPEED

    # Create bricks
    bricks = []
    for row in range(5):
        for col in range(0, WINDOW_WIDTH, BRICK_WIDTH + BRICK_GAP):
            brick_rect = pygame.Rect(col, 50 + row * (BRICK_HEIGHT + BRICK_GAP), BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick_rect)

    # Create power-ups
    powerups = []

    # Game variables
    score = 0
    level = 1

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_x < WINDOW_WIDTH - PADDLE_WIDTH:
            paddle_x += PADDLE_SPEED

        # Move the ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Handle ball collisions with walls
        if ball_x <= BALL_RADIUS or ball_x >= WINDOW_WIDTH - BALL_RADIUS:
            ball_dx *= -1
        if ball_y <= BALL_RADIUS:
            ball_dy *= -1

        # Handle ball collision with paddle
        ball_dx, ball_dy = handle_paddle_collision(paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy)

        # Handle ball collision with bricks and power-ups
        ball_dx, ball_dy, score = handle_brick_collisions(bricks, ball_x, ball_y, ball_dx, ball_dy, powerups, score)

        # Move and update power-ups
        move_powerups(powerups)
        check_powerup_bottom(powerups)

        # Check if the ball has reached the bottom of the screen
        if ball_y >= WINDOW_HEIGHT:
            running = False

        # Check if all bricks are destroyed to advance to the next level
        if len(bricks) == 0:
            level += 1
            ball_x = random.randint(BALL_RADIUS, WINDOW_WIDTH - BALL_RADIUS)
            ball_y = WINDOW_HEIGHT // 2
            ball_dx = random.choice([-2, 2])
            ball_dy = -BALL_SPEED
            for row in range(5):
                for col in range(0, WINDOW_WIDTH, BRICK_WIDTH + BRICK_GAP):
                    brick_rect = pygame.Rect(col, 50 + row * (BRICK_HEIGHT + BRICK_GAP), BRICK_WIDTH, BRICK_HEIGHT)
                    bricks.append(brick_rect)

        # Check if the ball has collided with a power-up
        if handle_powerup_collision(powerups, paddle_x, paddle_y, PADDLE_WIDTH):
            powerup_type = random.choice(POWERUP_TYPES)
            if powerup_type == "expand" and PADDLE_WIDTH < 200:
                PADDLE_WIDTH += 20
            elif powerup_type == "shrink" and PADDLE_WIDTH > 60:
                PADDLE_WIDTH -= 20

        # Update the game screen
        update_screen(bricks, paddle_x, ball_x, ball_y, powerups, score, level)
        clock.tick(60)

    pygame.quit()

# Run the game
run_game()

# Add an infinite loop to keep the window open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()