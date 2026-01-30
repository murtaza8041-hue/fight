import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 60, 100
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 60, 60
LANE_WIDTH = WIDTH // 3
ROAD_MARK_HEIGHT = 50
ROAD_MARK_WIDTH = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
ROAD_COLOR = (50, 50, 50)
ROAD_MARK_COLOR = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

class Car:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = WIDTH // 2 - CAR_WIDTH // 2
        self.y = HEIGHT - 150
        self.speed = 5
        self.lane = 1  # 0: left, 1: center, 2: right
        self.update_position()
        
    def update_position(self):
        self.x = LANE_WIDTH * self.lane + (LANE_WIDTH - CAR_WIDTH) // 2
        
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.update_position()
            
    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            self.update_position()
            
    def draw(self):
        # Car body
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        
        # Windows
        pygame.draw.rect(screen, BLUE, (self.x + 5, self.y + 5, self.width - 10, 30))
        
        # Wheels
        pygame.draw.rect(screen, BLACK, (self.x - 5, self.y + 15, 10, 25))
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 5, self.y + 15, 10, 25))
        pygame.draw.rect(screen, BLACK, (self.x - 5, self.y + self.height - 40, 10, 25))
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 5, self.y + self.height - 40, 10, 25))
        
        # Headlights
        pygame.draw.rect(screen, YELLOW, (self.x + 5, self.y, 10, 5))
        pygame.draw.rect(screen, YELLOW, (self.x + self.width - 15, self.y, 10, 5))

class Obstacle:
    def __init__(self):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.lane = random.randint(0, 2)
        self.x = LANE_WIDTH * self.lane + (LANE_WIDTH - OBSTACLE_WIDTH) // 2
        self.y = -OBSTACLE_HEIGHT
        self.speed = random.randint(3, 7)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        
    def move(self):
        self.y += self.speed
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def collide(self, car):
        car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return car_rect.colliderect(obstacle_rect)

class Game:
    def __init__(self):
        self.car = Car()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between obstacle spawns
        self.speed_increase_timer = 0
        
    def spawn_obstacle(self):
        if self.spawn_timer >= self.spawn_delay:
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0
            
    def update(self):
        if self.game_over:
            return
            
        # Spawn obstacles
        self.spawn_timer += 1
        self.spawn_obstacle()
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.y > HEIGHT:
                self.obstacles.remove(obstacle)
                self.score += 10
                
            # Check collision
            if obstacle.collide(self.car):
                self.game_over = True
                
        # Increase speed over time
        self.speed_increase_timer += 1
        if self.speed_increase_timer >= 300:  # Every 5 seconds
            for obstacle in self.obstacles:
                obstacle.speed += 0.5
            self.spawn_delay = max(20, self.spawn_delay - 5)  # Faster spawning
            self.speed_increase_timer = 0
            
    def draw(self):
        # Draw road
        screen.fill(ROAD_COLOR)
        
        # Draw lane markings
        for i in range(1, 3):
            for j in range(0, HEIGHT, ROAD_MARK_HEIGHT * 2):
                pygame.draw.rect(screen, ROAD_MARK_COLOR, 
                               (i * LANE_WIDTH - ROAD_MARK_WIDTH // 2, j, 
                                ROAD_MARK_WIDTH, ROAD_MARK_HEIGHT))
        
        # Draw car
        self.car.draw()
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw()
            
        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over
        if self.game_over:
            font_large = pygame.font.SysFont(None, 72)
            game_over_text = font_large.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to restart", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
            
    def restart(self):
        self.__init__()

def main():
    game = Game()
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.car.move_left()
                    elif event.key == pygame.K_RIGHT:
                        game.car.move_right()
                elif event.key == pygame.K_r:
                    game.restart()
                    
        # Continuous movement with held keys
        if not game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.car.move_left()
            if keys[pygame.K_RIGHT]:
                game.car.move_right()
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()