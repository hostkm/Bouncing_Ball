import pygame
import random
import time
import math
from pygame import gfxdraw  # For better particle rendering

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Particle colors
PARTICLE_COLORS = [YELLOW, ORANGE, RED, PURPLE]

# Power-up types
POWERUP_TYPES = ['speed_boost', 'time_bonus', 'shield']
POWERUP_COLORS = {
    'speed_boost': GREEN,
    'time_bonus': YELLOW,
    'shield': BLUE
}

# Game variables
ball_radius = 20
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed = 3
ball_dx, ball_dy = 0, 0
ball_shield = False

goal_radius = 25
obstacles = []
powerups = []
particles = []
ball_trail = []
TRAIL_LENGTH = 15

current_level = 1
max_levels = 100
score = 0
start_time = None
paused = False
clock = pygame.time.Clock()

# Sound effects (replace with actual sound files)
try:
    collision_sound = pygame.mixer.Sound('collision.wav')
    goal_sound = pygame.mixer.Sound('goal.wav')
    powerup_sound = pygame.mixer.Sound('powerup.wav')
except:
    # Dummy sound objects if files don't exist
    class DummySound:
        def play(self): pass
    collision_sound = goal_sound = powerup_sound = DummySound()

def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, current_level, score, start_time, paused
    global ball_speed, goal_radius, ball_shield, particles, powerups, ball_trail
    
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 0, 0
    current_level = 1
    score = 0
    start_time = time.time()
    paused = False
    ball_speed = 3
    goal_radius = 25
    ball_shield = False
    particles = []
    powerups = []
    ball_trail = []
    generate_obstacles()
    place_goal()

def generate_obstacles():
    global obstacles
    obstacles = []
    for _ in range(current_level):
        while True:
            rect = pygame.Rect(
                random.randint(50, WIDTH - 90),
                random.randint(50, HEIGHT - 90),
                40, 40
            )
            # Ensure obstacle doesn't overlap with starting position
            if ((rect.right < WIDTH//2 - 50 or rect.left > WIDTH//2 + 50) or
                (rect.bottom < HEIGHT//2 - 50 or rect.top > HEIGHT//2 + 50)):
                obstacles.append(rect)
                break

def place_goal():
    global goal_x, goal_y
    for _ in range(100):  # Try placing goal safely within 100 attempts
        goal_x, goal_y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        # Check if goal is not too close to any obstacle
        if all((goal_x - obstacle.centerx)**2 + (goal_y - obstacle.centery)**2 > 2500 for obstacle in obstacles):
            return
    goal_x, goal_y = WIDTH // 2, HEIGHT // 2  # Fallback placement

def spawn_powerup():
    if random.random() < 0.3:  # 30% chance per level
        powerups.append({
            'x': random.randint(50, WIDTH-50),
            'y': random.randint(50, HEIGHT-50),
            'type': random.choice(POWERUP_TYPES),
            'radius': 15,
            'active_time': 0
        })

def create_particles(x, y, count=20, max_speed=2):
    new_particles = []
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, max_speed)
        new_particles.append({
            'x': x,
            'y': y,
            'dx': math.cos(angle) * speed,
            'dy': math.sin(angle) * speed,
            'size': random.randint(2, 5),
            'color': random.choice(PARTICLE_COLORS),
            'life': random.randint(20, 40)
        })
    return new_particles

def display_message(text, size, color, y_offset=0):
    font = pygame.font.Font(None, size)
    message = font.render(text, True, color)
    rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(message, rect)

def check_circle_rect_collision(circle_x, circle_y, radius, rect):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    return (distance_x * distance_x + distance_y * distance_y) < (radius * radius)

def check_circle_circle_collision(x1, y1, r1, x2, y2, r2):
    distance_sq = (x1 - x2)**2 + (y1 - y2)**2
    return distance_sq < (r1 + r2)**2

def show_level_transition():
    screen.fill(WHITE)
    display_message(f"Level {current_level}", 60, BLUE, -20)
    display_message("Ready?", 40, BLACK, 30)
    pygame.display.update()
    pygame.time.delay(1500)  # 1.5 second delay

def save_high_score(score):
    try:
        with open('highscore.txt', 'w') as f:
            f.write(str(score))
    except:
        pass

def load_high_score():
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def show_intro_screen():
    screen.fill(BLACK)
    
    # Animation variables - simplified without fade
    title_y = -100
    tag_y = HEIGHT + 50
    
    # Fonts
    title_font = pygame.font.Font(None, 80)
    tag_font = pygame.font.Font(None, 40)
    
    # Animation loop
    clock = pygame.time.Clock()
    animation_complete = False
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        
        # Update positions only until they reach their final spots
        if not animation_complete:
            if title_y < HEIGHT//3:
                title_y += 3
            if tag_y > HEIGHT//2:
                tag_y -= 2
            
            # Check if animation is complete
            if title_y >= HEIGHT//3 and tag_y <= HEIGHT//2:
                animation_complete = True
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw title
        title_text = title_font.render("Bouncing Ball", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, title_y))
        screen.blit(title_text, title_rect)
        
        # Draw tag
        tag_text = tag_font.render("by KasunMK", True, (150, 150, 255))
        tag_rect = tag_text.get_rect(center=(WIDTH//2, tag_y))
        screen.blit(tag_text, tag_rect)
        
        # Draw "Press any key" prompt when animation completes
        if animation_complete:
            prompt_font = pygame.font.Font(None, 30)
            prompt_text = prompt_font.render("Press any key to start", True, (200, 200, 200))
            prompt_rect = prompt_text.get_rect(center=(WIDTH//2, HEIGHT*3//4))
            
            # Blinking effect
            if pygame.time.get_ticks() % 1000 < 500:  # Blink every second
                screen.blit(prompt_text, prompt_rect)
        
        pygame.display.flip()
        clock.tick(60)

# Keep all other functions exactly the same as in your previous code
# Only replace the show_intro_screen() function with this new version

def game_loop():
    global ball_x, ball_y, ball_dx, ball_dy, current_level, score, start_time, paused
    global ball_speed, goal_radius, ball_shield, particles, powerups, ball_trail
    
    running = True
    start_time = time.time()
    generate_obstacles()
    place_goal()
    spawn_powerup()
    bg_color = random_color()
    high_score = load_high_score()
    
    while running:
        screen.fill(bg_color)
        elapsed_time = max(int(time.time() - start_time), 0) if not paused else elapsed_time
        
        # Display game info
        font = pygame.font.Font(None, 30)
        screen.blit(font.render(f"Time: {elapsed_time}s", True, BLACK), (10, 10))
        screen.blit(font.render(f"Level: {current_level}", True, BLACK), (250, 10))
        screen.blit(font.render(f"Score: {score}", True, BLACK), (WIDTH - 100, 10))
        screen.blit(font.render(f"High Score: {high_score}", True, BLACK), (WIDTH - 150, 40))
        
        if ball_shield:
            shield_time = font.render(f"Shield: {max(0, 10 - int(time.time() - ball_shield))}s", True, BLUE)
            screen.blit(shield_time, (10, 40))
        
        if not paused:
            # Update ball position
            ball_x += ball_dx
            ball_y += ball_dy
            
            # Boundary collision
            if ball_x - ball_radius <= 0:
                ball_x = ball_radius
                ball_dx = -ball_dx
            elif ball_x + ball_radius >= WIDTH:
                ball_x = WIDTH - ball_radius
                ball_dx = -ball_dx
            if ball_y - ball_radius <= 0:
                ball_y = ball_radius
                ball_dy = -ball_dy
            elif ball_y + ball_radius >= HEIGHT:
                ball_y = HEIGHT - ball_radius
                ball_dy = -ball_dy
            
            # Update trail
            ball_trail.append((ball_x, ball_y))
            if len(ball_trail) > TRAIL_LENGTH:
                ball_trail.pop(0)
        
        # Draw goal
        pygame.draw.circle(screen, GREEN, (goal_x, goal_y), goal_radius)
        
        # Draw obstacles and check for collisions
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLUE, obstacle)
            if not ball_shield and check_circle_rect_collision(ball_x, ball_y, ball_radius, obstacle):
                collision_sound.play()
                show_game_over_screen()
                return
        
        # Draw and update particles
        for p in particles[:]:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)
        
        # Draw and check power-ups
        for powerup in powerups[:]:
            pygame.draw.circle(screen, POWERUP_COLORS[powerup['type']], 
                             (int(powerup['x']), int(powerup['y'])), powerup['radius'])
            
            if check_circle_circle_collision(ball_x, ball_y, ball_radius, 
                                           powerup['x'], powerup['y'], powerup['radius']):
                powerup_sound.play()
                if powerup['type'] == 'speed_boost':
                    ball_speed += 0.5
                elif powerup['type'] == 'time_bonus':
                    start_time -= 5  # Add 5 seconds
                elif powerup['type'] == 'shield':
                    ball_shield = time.time()
                powerups.remove(powerup)
                particles.extend(create_particles(powerup['x'], powerup['y']))
        
        # Draw ball trail
        for i, (tx, ty) in enumerate(ball_trail):
            alpha = int(255 * (i/len(ball_trail)))
            size = int(ball_radius * (i/len(ball_trail)))
            if size > 0:
                s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 0, 0, alpha), (size, size), size)
                screen.blit(s, (tx - size, ty - size))
        
        # Draw ball (with shield if active)
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
        if ball_shield and time.time() - ball_shield < 10:  # Shield lasts 10 seconds
            pygame.draw.circle(screen, (0, 0, 255, 100), (int(ball_x), int(ball_y)), 
                             ball_radius + 5, 2)
        else:
            ball_shield = False
        
        # Check goal collision
        if check_circle_circle_collision(ball_x, ball_y, ball_radius, goal_x, goal_y, goal_radius):
            goal_sound.play()
            particles.extend(create_particles(goal_x, goal_y, 30, 3))
            score += max(100 - elapsed_time, 0)
            current_level += 1
            
            if current_level > max_levels:
                if score > high_score:
                    save_high_score(score)
                show_win_screen()
                return
            else:
                # Progressive difficulty
                ball_speed += 0.1
                if current_level % 5 == 0:
                    goal_radius = max(15, goal_radius - 2)
                
                show_level_transition()
                generate_obstacles()
                place_goal()
                spawn_powerup()
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx, ball_dy = 0, 0
                start_time = time.time()
                bg_color = random_color()
                if score > high_score:
                    high_score = score
                    save_high_score(score)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_LEFT:
                    ball_dx = -ball_speed
                elif event.key == pygame.K_RIGHT:
                    ball_dx = ball_speed
                elif event.key == pygame.K_UP:
                    ball_dy = -ball_speed
                elif event.key == pygame.K_DOWN:
                    ball_dy = ball_speed
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    ball_dx = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    ball_dy = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - ball_x
                dy = mouse_y - ball_y
                length = max(1, (dx**2 + dy**2)**0.5)
                ball_dx = (dx/length) * ball_speed
                ball_dy = (dy/length) * ball_speed
        
        if paused:
            display_message("Paused - Press P to Resume", 40, BLACK, 0)
        
        pygame.display.update()
        clock.tick(60)

def show_game_over_screen():
    screen.fill(WHITE)
    display_message("Game Over", 50, RED, -20)
    display_message(f"Final Score: {score}", 36, BLACK, 20)
    display_message("Press ENTER to Try Again", 30, BLACK, 60)
    display_message("KasunMK", 20, BLUE, 100)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    reset_game()
    game_loop()

def show_win_screen():
    screen.fill(WHITE)
    display_message("YOU WON!", 50, GREEN, -20)
    display_message(f"Final Score: {score}", 36, BLACK, 20)
    display_message("Press ENTER to Play Again", 30, BLACK, 60)
    display_message("KasunMK", 20, BLUE, 100)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    reset_game()
    game_loop()

# Start the game
if __name__ == "__main__":
    # Show intro screen first
    show_intro_screen()
    
    # Then start the main game
    reset_game()
    game_loop()
    pygame.quit()