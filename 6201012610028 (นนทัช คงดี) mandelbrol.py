#####################################################################
# Name: Nontouch kongdee 
#student code : 6201012610028
# File: threading mandelbrot
# Date: 2020-07-24
#####################################################################

# this code is make from demo-8 and 7
import threading
import time
import cmath
import pygame
from random import randint, randrange, random

print( 'File:', __file__ )
#if N is greater than screen of width
def makespace(N) :
    global scr_w
    if N > scr_w :
        wp = int(scr_w/scr_w/2)
        return wp
    elif scr_w % N != 0 :
        wp = int(scr_w//N + 1)
        return wp
    else :
        wp = int(scr_w/ N)
        return wp
#function for make the mandelbrol solution
def mandelbrot(c,max_iters=100):
    i = 0
    z = complex(0,0)
    while abs(z) <= 2 and i < max_iters:
        z = z*z + c
        i += 1 
    return i
#function for take the mandelbrol by threating
def semandelbrol(surface,i,sem,lock) :
    global w2, h2, N
    wp = makespace(N)
    scale = 0.006
    offset = complex(-0.55,0.0)
    if sem.acquire(timeout=0.1):
        for x in range(i *wp,(i+1)*wp):
            for y in range(scr_h):
                with lock :
                    re = scale*(x-w2) + offset.real
                    im = scale*(y-h2) + offset.imag
                    c = complex( re, im )
                    color = mandelbrot(c, 63)
                    r = (color << 6) & 0xc0
                    g = (color << 4) & 0xc0
                    b = (color << 2) & 0xc0
                    surface.set_at( (x, y), (255-r,255-g,255-b) )

# initialize pygame
pygame.init()

# create a screen of width=500 and height=500
scr_w, scr_h = 500, 500
screen = pygame.display.set_mode( (scr_w, scr_h) )

# set window caption
pygame.display.set_caption('Semandelbrot') 

# create a clock
clock = pygame.time.Clock()

# create a surface for drawing
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

N = int(400)

lock = threading.Lock()
# create a list for semaphore
list_semaphores = [ threading.Semaphore(0) for i in range(N) ]
# create a list for mandelbrol
list_semandelbrol = []
#if N is greater than screen of width
if N > scr_w :
    N = int(scr_w/2)
#built a thread for mandelbrol
for i in range(N) :
    sem = list_semaphores[i]
    tar = threading.Thread(target=semandelbrol, args=(surface,i,sem,lock))
    list_semandelbrol.append(tar)
# start  threads
for tar in list_semandelbrol :
    tar.start()


running = True
w2, h2 = scr_w/2, scr_h/2 # half width, half screen
# running screen
while running:
# clock for speed of drawing
    clock.tick(N)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # for release threads
    for sem in list_semaphores :
        sem.release()

    # draw the surface on the screen
    screen.blit( surface, (0,0) )

    # update the display
    pygame.display.update()

pygame.quit()
print( 'semandelbrol...semandelbrol...semandelbrol...semandelbrol...semandelbrol...semandelbrol...semandelbrol...semandelbrol...semandelbrol...semandelbrol...')
################################################################