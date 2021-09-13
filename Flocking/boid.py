import pygame
from pygame.math import Vector2
from Flocking.matrix import *
from constants import *
from random import uniform, randint
from math import pi, cos, sin, atan2, degrees, sqrt
from particle import GetDistanceSQ

def Limit(vec, max_mag):
    magsq = Vector2.magnitude_squared(vec)
    temp = vec
    if magsq > (max_mag * max_mag):
        temp = Vector2.normalize(temp)
        temp *= max_mag

    return temp

#v = Vector2(10, 20)
#v = Limit(v, 5)
#print(v)
def Heading(vec):
    angle = atan2(vec.y, vec.x)
    return angle

class Boid:
    def __init__(self, position, flock=None):
        self.position = position
        self.radius = RADIUS
        self.angle = uniform(0, pi*2)
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(cos(self.angle), sin(self.angle))
        self.maxSpeed = 4
        self.maxForce = 0.03
        self.flock = flock
        self.stroke = 1
        self.hue = 0

        self.trailStroke = 2
        self.trailLimit = 20
        self.trail = []
        self.counter = 0

    def Simulate(self, boids):
        self.Flock(boids)
        self.Update()
        self.Boundary()

    def ApplyForce(self, f):
        self.acceleration += f

    def Flock(self, boids):
        separation  = self.Separate(boids)
        alignment   = self.Align(boids)
        cohesion    = self.Cohesion(boids)

        separation *= self.flock.separation
        alignment  *= self.flock.alignment
        cohesion   *= self.flock.cohesion

        self.ApplyForce(separation)
        self.ApplyForce(alignment)
        self.ApplyForce(cohesion)

    def Update(self):
        self.velocity += self.acceleration
        self.velocity = Limit(self.velocity, self.maxSpeed)
        self.position += self.velocity
        self.acceleration *= 0
        self.angle = Heading(self.velocity) + round(pi/2,2)



    def Separate(self, boids):
        steering = Vector2(0, 0)
        total = 0
        desired_separation = self.flock.separation_value

        for boid in boids:
            dist = Vector2.distance_to(self.position, boid.position)
            if dist > 0 and dist < desired_separation:
                difference = self.position - boid.position
                difference = Vector2.normalize(difference)
                difference /= dist
                steering += difference
                total += 1
                boid.hue = self.flock.HUE

        if total > 0:
            steering /= total

        magnitude = Vector2.magnitude(steering)
        if magnitude > 0:
            steering = Vector2.normalize(steering)
            steering *= self.maxSpeed
            steering -= self.velocity
            steering = Limit(steering, self.maxForce)

        return steering

    def Align(self, boids):
        total = 0
        steering = Vector2(0, 0)
        neighbourDistance = self.flock.alignment_value

        for boid in boids:
            dist = Vector2.distance_to(self.position, boid.position)
            if dist > 0 and dist < neighbourDistance:
                steering += boid.velocity
                total += 1
                boid.hue = self.flock.HUE


        if total > 0:
            steering /= total
            steering = Vector2.normalize(steering)
            steering *= self.maxSpeed
            steering -= self.velocity
            steering = Limit(steering, self.maxForce)
            return steering
        else:
            return Vector2(0, 0)

    def Cohesion(self, boids):
        neighbourDistance = self.flock.cohesion_value
        total = 0
        steering = Vector2(0, 0)

        for boid in boids:
            dist = Vector2.distance_to(self.position, boid.position)
            if dist > 0 and dist < neighbourDistance:
                steering += boid.position
                total += 1
                boid.hue = self.flock.HUE

        if total > 0:
            steering /= total
            return self.Steer(steering)
        else:
            return Vector2(0, 0)
    def Steer(self, target):
        t = target - self.position
        t = Vector2.normalize(t)
        t *= self.maxSpeed
        steer = t - self.velocity
        steer = Limit(steer, self.maxForce)
        return steer


    def Boundary(self):
        if self.position.x < -self.radius:
            self.position.x = Width+self.radius
        if self.position.y < - self.radius:
            self.position.y = Height+self.radius

        if self.position.x > Width + self.radius:
            self.position.x = -self.radius
        if self.position.y > Height+self.radius:
            self.position.y = -self.radius

    def Render(self):
        # hsv color
        c = pygame.Color(0, 0, 0)
        c.hsva = (self.hue%360, 100, 100, 100)
        color = c

        distance = 5
        scale = 30
        ps = []
        points = [None for _ in range(4)]

        points[0] = [[0],[-self.radius],[0]]
        points[1] = [[self.radius//2],[self.radius//2],[0]]
        points[2] = [[-self.radius//2],[self.radius//2],[0]]
        points[3] = [[0],[0],[0]]

        for point in points:
        	rotated = matrix_multiplication(rotationZ(self.angle) , point)
        	z = 1/(distance - rotated[2][0])

        	projection_matrix = [[z, 0, 0], [0, z, 0]]
        	projected_2d = matrix_multiplication(projection_matrix, rotated)

        	x = int(projected_2d[0][0] * scale) + self.position.x
        	y = int(projected_2d[1][0] * scale) + self.position.y
        	ps.append((x, y))

        if len(self.trail) > self.trailLimit:
            self.trail.pop(0)

        window = self.flock.window
        if self.flock.showTrail:
            if len(self.trail) > 0:
                dist = GetDistanceSQ(self.trail[-1], ps[3])
                if dist > 10:
                    self.trail = []
            self.trail.append(ps[3])
            for i in range(len(self.trail)-1):
                pygame.draw.line(window, color, self.trail[i], self.trail[i+1], self.trailStroke)
        pygame.draw.polygon(window, color, ps[:3])
        pygame.draw.polygon(window, color, ps[:3], self.stroke)
