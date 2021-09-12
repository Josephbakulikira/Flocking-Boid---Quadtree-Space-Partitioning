from pygame.math import Vector2
from range import Rectangle, Circle
from constants import *

class Flock:
    def __init__(self, screen, boids=[]):
        self.boids = boids
        self.separation = 1.2
        self.alignment = 3
        self.cohesion = 1
        self.separation_value = 25
        self.alignment_value = 50
        self.cohesion_value = 50
        self.window = screen
        self.quadTree = None
        self.ActivateQuadtree = True
        self.showRange = False
        self.showTrail = False
        self.HUE = 0

    def Simulate(self):
        if self.ActivateQuadtree:
            for boid in self.boids:
                if self.quadTree:
                    self.quadTree.insert(boid)
                boid.Render()

            for boid in self.boids:
                xx, yy = boid.position
                r = self.alignment_value + self.cohesion_value

                # circle range
                rangeCircle = Circle(Vector2(xx, yy), r)
                rangeCircle.color = (0, 255 ,255)
                rangeCircle.lineThickness = 1

                # rectange range
                rangeRect = Rectangle(Vector2(xx - r/2, yy - r/2), Vector2(r, r))
                rangeRect.color = (190, 210, 55)
                rangeRect.lineThickness = 1

                # rangeRect or rangeCircle
                range = rangeRect
                if self.showRange:
                    range.Draw(self.window)
                others = self.quadTree.queryRange(range)

                boid.Simulate(others)
        else:
            for boid in self.boids:
                boid.Simulate(self.boids)
                boid.Render()

        self.HUE += 0.4

    def Append(self, boid):
        self.boids.append(boid)
