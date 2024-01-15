import pygame
import os       # helps define path to images
pygame.font.init()     # initialize pygame font library
pygame.mixer.init()      # for sounds

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # X width/2 gets middle of screen//y for top to bottom
# y to 0 to start from top and go down//width 10, height
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VELOCITY = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1    # if these were both +1 they would be the same event
RED_HIT = pygame.USEREVENT + 2       # the +1 makes it a unique event id

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
# resize spaceship. W and H & rotate 90 degrees
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)             # resize spaceship. W and H

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):                # read and yellow rectangle
    WIN.blit(SPACE, (0, 0))     # WIN.fill(WHITE) will display # delete and you will see pygame does not remove last drawing. need to draw background every frame
    pygame.draw.rect(WIN, BLACK, BORDER)      # draw rectangle, black, border = rectangle

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))   # we dont care about width because its already on left wall, and then 10 down

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))       # blit is put things on the screen, draw where H and W
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()                     # update display


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # Left key  if a key does not cross 0 when pressed
        yellow.x -= VELOCITY  # if key is pressed subtract x to get closer to 0
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:  # Right key // don't cross border
        yellow.x += VELOCITY  # add to the x
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # up
        yellow.y -= VELOCITY  # change to y for up and down
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 10:  # down
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:    # arrow keys
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 10:
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red): # move the bullets, handle collision, check if hits screen
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # T or F yellow bullet did collide with red, only works with rectangle
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)  # if collide with character remove bullet
        elif bullet.x > WIDTH:   # if bullet is greater than screen
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) # delay text for 5000 milliseconds


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)       # x 100 y 300 positions for rectangle
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()               # clock object,
    run = True
    while run:
        clock.tick(FPS)                       # run the while loop 60 times per second
        for event in pygame.event.get():      # all different events in game
            if event.type == pygame.QUIT:     # this is for clicking x event
                run = False
                pygame.quit()     # delete if you use it below

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # if bullets doesnt pass max bullets
                    # place bullet at yellow character /2 for middle of image
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)  # // for int division
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:  # if red is hit then subtract health
                red_health -= 1
                BULLET_HIT_SOUND

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND

        winner_text =""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()         # what keys are currently being pressed down
        yellow_handle_movement(keys_pressed, yellow)    # pass to function
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # pygame.quit() will quit the game
    main() # restarts game


# name is name of file, main is hey this main file that was run
if __name__== "__main__":
    main()
