import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

#text colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

#gameplay techs
clock = pygame.time.Clock()
score = 0
pipe_gap = 200
pipe_width = 60
bird_width = 50
bird_height = 40
bird_velocity = 0
bird_y = HEIGHT // 2
gravity = 0.5
flap_strength = -10
scroll_speed = 4
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
game_over = False
highest_score = 0

# Load images used
bird_image = pygame.image.load('images/bird.jpg')
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))  

pipe_image = pygame.image.load('images/pipe.png')
pipe_image = pygame.transform.scale(pipe_image, (pipe_width, HEIGHT))  

bg_image = pygame.image.load('images/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  

restart_button_image = pygame.image.load('images/start.png')
restart_button_image = pygame.transform.scale(restart_button_image, (200, 50))  

#Font size for tracker
font = pygame.font.SysFont('Arial', 36)

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        if is_top:
            self.rect.bottom = y - pipe_gap // 2
        else:
            self.rect.top = y + pipe_gap // 2
        self.passed = False  

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = bird_y

    def update(self):
        global bird_velocity
        bird_velocity += gravity  # Apply gravity
        self.rect.y += bird_velocity  
        
        #Screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def flap(self):
        global bird_velocity
        bird_velocity = flap_strength  # Set the bird's velocity to a negative value to simulate jumping


# Button 
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False


# Initialize sprites
bird = Bird()
bird_group = pygame.sprite.Group()
bird_group.add(bird)

pipe_group = pygame.sprite.Group()

# Initialize the restart button
restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 25, restart_button_image)

#main 
running = True
while running:
    clock.tick(60)
    
    screen.blit(bg_image, (0, 0))
    
    #event for pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                bird.flap()  
            elif restart_button.is_clicked():
                game_over = False
                bird.rect.y = bird_y
                bird_velocity = 0
                score = 0
                pipe_group.empty()
                last_pipe = pygame.time.get_ticks() - pipe_frequency

    #pipes
    if not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(100, 300)
            top_pipe = Pipe(WIDTH, pipe_height, is_top=True)
            bottom_pipe = Pipe(WIDTH, pipe_height, is_top=False)
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)
            last_pipe = current_time

    #game
    if not game_over:
        bird_group.update()
        pipe_group.update()

    #collision
    for pipe in pipe_group:
        if pipe.rect.colliderect(bird.rect):
            game_over = True  

        if not pipe.passed and pipe.rect.right < bird.rect.left:
            pipe.passed = True
            score += 1  

    #high score tracker
    if score > highest_score:
        highest_score = score

    bird_group.draw(screen)
    pipe_group.draw(screen)

    
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


    highest_score_text = font.render(f"Highest Score: {highest_score}", True, BLACK)
    screen.blit(highest_score_text, (10, 50))

    
    if game_over:
        restart_button.draw()
        

    pygame.display.flip()

pygame.quit()
