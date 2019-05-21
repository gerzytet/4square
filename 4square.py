import random
import sys
import pygame

##### CONFIG #####

#important
DISPLAY_HEIGHT = 500
DISPLAY_WIDTH = 500
FRAMERATE = 40
CLICK_BUTTON = 1 #left click by default.  2 = right click
FLASH_MS = 500
WAIT_MS = 300
STARTUP_WAIT = 2000
SUCCESS_WAIT = 300

#colors
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 128)
#order:
##01
##23
COLOR_ORDER = (GREEN, ORANGE, PINK, BLUE)

#display
VERTICAL_MARGIN = 50
HORIZONTAL_MARGIN = 50
INNER_VERTICAL_MARGIN = 30
INNER_HORIZONTAL_MARGIN = 30

#unimportant
WINDOW_TITLE = 'Planet: Code challenge program'

#internal
ALLOWED_EVENTS = [pygame.QUIT, pygame.MOUSEBUTTONDOWN]
ALLOWED_EVENT_DURING_FLASH = [pygame.QUIT]
SQUARE_WIDTH = (DISPLAY_WIDTH - INNER_HORIZONTAL_MARGIN - HORIZONTAL_MARGIN*2) // 2
SQUARE_HEIGHT = (DISPLAY_HEIGHT - INNER_VERTICAL_MARGIN - VERTICAL_MARGIN*2) // 2
CORNERS = [
    (HORIZONTAL_MARGIN, VERTICAL_MARGIN),
    (HORIZONTAL_MARGIN + INNER_HORIZONTAL_MARGIN + SQUARE_WIDTH, VERTICAL_MARGIN),
    (HORIZONTAL_MARGIN, VERTICAL_MARGIN + INNER_VERTICAL_MARGIN + SQUARE_HEIGHT),
    (HORIZONTAL_MARGIN + INNER_HORIZONTAL_MARGIN + SQUARE_WIDTH,
     VERTICAL_MARGIN + INNER_VERTICAL_MARGIN + SQUARE_HEIGHT)
]

##### CODE #####

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

pygame.event.set_allowed(ALLOWED_EVENTS)
mousex, mousey = 0, 0

def lighten(color):
    return tuple((i // 2 for i in color))

def quit():
    pygame.display.quit()
    print('\nGame Over!')
    print('Score: ' + str(score))
    sys.exit(0)

def draw_corner(corner, light = False):
    position = CORNERS[corner]
    color = COLOR_ORDER[corner]
    if light:
        color = lighten(color)
    pygame.draw.rect(screen, color, position + (SQUARE_WIDTH, SQUARE_HEIGHT))

def initial_render():
    for i in range(4):
        draw_corner(i)

def check_hitbox(corner1, corner2, pos):
    return pos[0] in range(corner1[0], corner2[0]) and pos[1] in range(corner1[1], corner2[1])

#returns the button clicked, None if it hit a margin
def check_hitboxes(pos):
    for index, corner in enumerate(CORNERS):
        corner2 = (corner[0] + SQUARE_WIDTH, corner[1] + SQUARE_HEIGHT)
        if check_hitbox(corner, corner2, pos):
            return index
    return None

def flash(corner):
    draw_corner(corner, light = True)
    pygame.display.flip()
    pygame.time.wait(FLASH_MS)
    
    draw_corner(corner)
    pygame.display.flip()
    pygame.time.wait(WAIT_MS)

def get_quit():
    events = pygame.event.get(pygame.QUIT)
    return bool(events)

initial_render()
pygame.display.flip()
pattern = []
pygame.time.wait(STARTUP_WAIT)
clock = pygame.time.Clock()
score = 0

while 1:
    pygame.event.set_allowed(ALLOWED_EVENT_DURING_FLASH)
    for i in pattern:
        if get_quit():
            quit()
        flash(i)

    pygame.event.set_allowed(ALLOWED_EVENTS)
    corner_progress = 0
    while corner_progress < len(pattern):
        clock.tick(FRAMERATE)
        click = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == CLICK_BUTTON:
                    click = True
                    mousex, mousey = event.pos

        if click:
            hit = check_hitboxes((mousex, mousey))
            if hit is not None:
                if hit == pattern[corner_progress]:
                    corner_progress += 1
                    score += 1
                else:
                    quit()
                hit = None

    pattern.append(random.randint(0, 3))
    pygame.time.wait(SUCCESS_WAIT)
