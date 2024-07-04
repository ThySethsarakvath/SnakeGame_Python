import random # generate random position and color
import pygame # create game window and handling game logic
import tkinter as tk
from tkinter import messagebox # for displaying message to the user

pygame.font.init()
pygame.mixer.init()

# class cude represents each segment of the snake and the snack
class cube(object):
    rows = 20
    w = 800
    
    # initializes the cube with its starting position, direction, and color
    def __init__(self, start, dirnx=1, dirny=0, color=(0,0,255)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    # updates the cube's position based on its direction
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # renders the cube on the given surface
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        

        # draw the eyes for the snake
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

# class snake represents the snake
class snake(object):
    body = []
    turns = {}

    # initializes the snake with its color, starting position, and direction
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    #  handles the snake's movement and direction changes based on user input
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

            keys = pygame.key.get_pressed()

# in here the snake can't be moved in opposite direction
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: 
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: 
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: 
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: 
                    c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx, c.dirny)

    # reset the snake to initial state
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # adds a new segment to the snake at the correct position based on the tail's current direction
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

# draw the line on the game surface
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# display the score while playing
def drawScore(surface, score):
    font = pygame.font.SysFont('comicsans', 35)
    text = font.render('Score: ' + str(score), True, (0, 0, 255))
    surface.blit(text, (10, 10))

# clear the screen , redraw the window,snake,snake
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((255,255,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    drawScore(surface, len(s.body) - 1)  # Subtract 1 to account for the initial segment
    pygame.display.update()


# place random snack and color
def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return (x, y), color

# displays a message box with the given subject and content
# def message_box(subject, content):
#     root = tk.Tk()
#     root.attributes("-topmost", True)
#     root.withdraw()
#     messagebox.showinfo(subject, content)
#     try:
#         root.destroy()
#     except:
#         pass

# displays a message box with the given subject and content
def message_box_choice(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    result = messagebox.askquestion(subject, content)
    try:
        root.destroy()
    except:
        pass
    return result


# function sets up the game window, initializes the snake and snack, and contains the game loop
def main():
    global width, rows, s, snack
    width = 800
    rows = 20
    win = pygame.display.set_mode((width, width))

    pygame.mixer.music.load('music_background.mp3')
    pygame.mixer.music.play(-1)
    eatsound = pygame.mixer.Sound('eat.wav')
    endsound = pygame.mixer.Sound('end.mp3')

    s = snake((0, 0, 255), (10, 10))
    snack_pos, snack_color = randomSnack(rows, s)
    snack = cube(snack_pos, color=snack_color)
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(30)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            eatsound.play()
            s.addCube()
            snack_pos, snack_color = randomSnack(rows, s)
            snack = cube(snack_pos, color=snack_color)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                pygame.mixer.music.stop()
                endsound.play()
                score = len(s.body) -1
                if score < 10:
                    message = 'Better try harder ;)'
                else:
                    message = 'Noiceee!'
                result = message_box_choice('You Lost!', f'Score: {score}. {message} \n Play again?')
                if result == 'yes':
                    s.reset((10, 10))
                    endsound.stop()
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return
                break
        redrawWindow(win)
        
    pass

main()