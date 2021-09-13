import pygame
from random import randint
from pygame.math import Vector2
from constants import *
from Flocking.flock import Flock
from Flocking.boid import *
from quadtree import QuadTree
from range import Rectangle

screen = pygame.display.set_mode(Resolution)

pygame.display.set_caption("Quadtree")
clock = pygame.time.Clock()
fps = 1000

flock = Flock(screen)

for i in range(SIZE):
    offset = 200
    pos = Vector2(randint(offset, Width-offset), randint(offset, Height-offset))
    # pos = Vector2(Width/2, Height/2)

    flock.Append(Boid(pos, flock))

showQuadTree = False
SwitchRange = 1
run = True
while run:
    screen.fill(Color1)
    pygame.display.set_caption("QuadTree Fps: " + str(int(clock.get_fps())))
    clock.tick(fps)

    # create QuadTree
    boundary = Rectangle(Vector2(0, 0), Vector2(Width, Height))

    quadtree = QuadTree(NODE_CAPACITY, boundary)
    quadtree.lineThickness = 1
    quadtree.color = (0,87,146)
    flock.quadTree = quadtree

    # ----- HANDLE EVENTS ------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                flock.ActivateQuadtree = not flock.ActivateQuadtree
                notification = " -Space partitioning is Activated- " if flock.ActivateQuadtree else " -Space partitioning is Deactivated- "
                print(notification)
            if event.key == pygame.K_RETURN or event.key == pygame.K_q:
                showQuadTree = not showQuadTree
            if event.key == pygame.K_r:
                flock.showRange = not flock.showRange
            if event.key == pygame.K_t:
                flock.showTrail = not flock.showTrail
            if event.key == pygame.K_s:
                flock.rangeIndex = (flock.rangeIndex + 1) % 2
    # -----------------------------

    flock.Simulate()

    if showQuadTree:
        quadtree.Show(screen)

    pygame.display.flip()

pygame.quit()
