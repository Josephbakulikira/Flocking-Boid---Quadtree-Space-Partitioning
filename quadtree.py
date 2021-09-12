import pygame
from pygame.math import Vector2
from range import *

class QuadTree:
    def __init__(self, capacity, boundary, color = (140, 255, 160), thickness=1):
        self.capacity = capacity
        self.boundary = boundary
        self.particles = []
        self.color = color
        self.lineThickness = thickness
        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

    def subdivide(self):
        parent = self.boundary

        boundary_nw = Rectangle(
                Vector2(
                parent.position.x ,
                parent.position.y
                ),
            parent.scale/2
            )
        boundary_ne = Rectangle(
                Vector2(
                parent.position.x + parent.scale.x/2,
                parent.position.y
                ),
                parent.scale/2
            )
        boundary_sw = Rectangle(
                Vector2(
                parent.position.x,
                parent.position.y + parent.scale.y/2
                ),
                parent.scale/2
            )
        boundary_se = Rectangle(
                Vector2(
                parent.position.x + parent.scale.x/2,
                parent.position.y + parent.scale.y/2
                ),
                parent.scale/2
            )

        self.northWest = QuadTree(self.capacity, boundary_nw, self.color, self.lineThickness)
        self.northEast = QuadTree(self.capacity, boundary_ne, self.color, self.lineThickness)
        self.southWest = QuadTree(self.capacity, boundary_sw, self.color, self.lineThickness)
        self.southEast = QuadTree(self.capacity, boundary_se, self.color, self.lineThickness)

        for i in range(len(self.particles)):
            self.northWest.insert(self.particles[i])
            self.northEast.insert(self.particles[i])
            self.southWest.insert(self.particles[i])
            self.southEast.insert(self.particles[i])
    def insert(self, particle):
        if self.boundary.containsParticle(particle) == False:
            return False

        if len(self.particles) < self.capacity and self.northWest == None:
            self.particles.append(particle)
            return True
        else:
            if self.northWest == None:
                self.subdivide()

            if self.northWest.insert(particle):
                return True
            if self.northEast.insert(particle):
                return True
            if self.southWest.insert(particle):
                return True
            if self.southEast.insert(particle):
                return True
            return False

    def queryRange(self, _range):
        particlesInRange = []

        if type(_range) == Circle:
            if _range.intersects(self.boundary)==False:
                return particlesInRange
        elif type(_range) == Rectangle:
            if _range.intersects(self.boundary)==True:
                return particlesInRange

        for particle in self.particles:
            if _range.containsParticle(particle):
                particlesInRange.append(particle)
        if self.northWest != None:
            particlesInRange += self.northWest.queryRange(_range)
            particlesInRange += self.northEast.queryRange(_range)
            particlesInRange += self.southWest.queryRange(_range)
            particlesInRange += self.southEast.queryRange(_range)

        # if self.boundary.intersects(_range):
        #     return particlesInRange
        # else:
        #     for particle in self.particles:
        #         if _range.containsParticle(particle):
        #             particlesInRange.append(particle)
        #
        #     if self.northWest != None:
        #         particlesInRange += self.northWest.queryRange(_range)
        #         particlesInRange += self.northEast.queryRange(_range)
        #         particlesInRange += self.southWest.queryRange(_range)
        #         particlesInRange += self.southEast.queryRange(_range)
        #
        #     return particlesInRange
        return particlesInRange

    def Show(self, screen):
        self.boundary.color = self.color
        self.boundary.lineThickness = self.lineThickness
        self.boundary.Draw(screen)
        if self.northWest != None:
            self.northWest.Show(screen)
            self.northEast.Show(screen)
            self.southWest.Show(screen)
            self.southEast.Show(screen)
