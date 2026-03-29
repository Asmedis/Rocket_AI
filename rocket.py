import math
from brain import Brain
from scoring import calculate_score

class Rocket:
    def __init__(self):
        # Initialize rocket parameters
        self.goal = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.r = 0
        self.rv = 0
        self.brain = Brain()
        self.thrust_power = -15 / 60
        self.thrust_level = 100
        self.rcs_power = 2 / 60
        self.score = 0
        self.ticks = 0
        self.flying = True
        self.on_pad = False

    def update(self):
        # Update rocket position and rotation
        self.x += self.vx
        self.y += self.vy
        self.r += self.rv
    
    def thrust(self):
        # Calculate thrust components
        thrust_y = math.sin(math.radians(self.r + 90))
        thrust_x = math.cos(math.radians(self.r + 90))

        # Apply thrust to velocity
        self.vx += self.thrust_power * thrust_x * (self.thrust_level / 100)
        self.vy -= self.thrust_power * thrust_y * (self.thrust_level / 100)
    
    def rotate_left(self):
        # Rotate rocket left
        self.rv -= self.rcs_power
    
    def rotate_right(self):
        # Rotate rocket right
        self.rv += self.rcs_power

    def think(self):
        # Gather inputs for the brain
        inputs = [self.x, self.y, self.vx, self.vy, self.r, self.rv, self.goal]
        actions = self.brain.think(inputs, 4)
        
        # Update thrust level and ticks
        self.thrust_level = actions[3]
        self.ticks += 1
        
        # Perform actions based on brain output
        if actions[0] > 50:
            self.thrust()
        if actions[1] > 50:
            self.rotate_right()
        if actions[2] > 50:
            self.rotate_left()

    def landed(self, on_pad, goal_location):
        # Calculate score and reset rocket parameters upon landing
        if self.starting_position < goal_location:
            travel_distance = self.starting_position - self.x
        else:
            travel_distance = self.x - self.starting_position

        travel_distance = self.x - self.starting_position
        self.score = calculate_score(self, on_pad, travel_distance)
        self.vx = 0
        self.vy = 0
        self.r = 0
        self.rv = 0
        self.flying = False