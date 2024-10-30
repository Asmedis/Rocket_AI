import arcade
import math
import random
from brain import brain, neuron
from scoring import calculate_score
import copy

ROCKET_AMOUNT = 50

class rocket_object:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vy = 0
        self.vx = 0
        self.r = 0
        self.rv = 0
        self.brain = brain()

        self.thrust_power = -15 / 60
        self.thrust_level = 100
        self.rcs_power = 2 / 60

        self.score = 0
        self.ticks = 0

        self.flying = True
        self.on_pad = False


    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.r += self.rv
    
    def thrust(self):
        thrust_y = math.sin(math.radians(self.r+90)) 
        thrust_x = math.cos(math.radians(self.r+90))

        self.vx += (self.thrust_power * thrust_x * (self.thrust_level/100))
        self.vy -= (self.thrust_power * thrust_y * (self.thrust_level/100))
    
    def rotate_left(self):
        self.rv -= self.rcs_power
    
    def rotate_right(self):
        self.rv += self.rcs_power

    def think(self):
        inputs = [self.x, self.y, self.vx, self.vy, self.r, self.rv]
        actions = self.brain.think(inputs, 4)
        self.thrust_level = actions[3]
        self.ticks += 1
        if actions[0] > 50:
            self.thrust()
        if actions[1] > 50:
            self.rotate_right()
        if actions[2] > 50:
            self.rotate_left()

    def landed(self, on_pad, goal_location):
        self.score = calculate_score(self, on_pad, goal_location)
        self.vx = 0
        self.vy = 0
                
        self.r = 0
        self.rv = 0
        self.flying = False



class game(arcade.Window):
    def __init__(self, width=1200, height=800):
        super().__init__(width, height, "Rocket game")
        self.set_update_rate(1 / 60)
        
        self.width = width
        self.height = height
        self.gravity = 10 / 60
        self.rocket_amount = ROCKET_AMOUNT

        arcade.set_background_color(arcade.color.BLACK)

        #Create rockets
        self.rockets = []
        for x in range(self.rocket_amount):
            new_rocket = rocket_object()
            new_rocket.x = 50 #random.randint(50, width-50)
            new_rocket.y = self.height - 50

            #Create sprite for rockets
            new_rocket.sprite = arcade.Sprite("imgs/rocket.png", scale=0.05)
            new_rocket.sprite.center_x = new_rocket.x
            new_rocket.sprite.center_y = new_rocket.y

            self.rockets.append(new_rocket)

        #Create landing pad
        self.obstacle_list = arcade.SpriteList()
        obstacle = arcade.Sprite("imgs/landing_pad.png", 0.05)
        obstacle.center_x = 1000
        obstacle.center_y = 10
        self.obstacle_list.append(obstacle)
        
        self.ticks = 0

    def on_draw(self):
        arcade.start_render()

        for rocket in self.rockets:
            rocket.sprite.draw()
        
        self.obstacle_list.draw()

    def update(self, delta_time):
        for rocket in self.rockets:
            if rocket.x < 0:
                rocket.x = 0
                rocket.flying = False
                self.vx = 0
                self.vy = 0
                self.rv = 0

            #if rocket.x > self.width:
            #    rocket.x = self.width
            #    rocket.flying = False
            #    self.vx = 0
            #    self.vy = 0
            #    self.rv = 0

            if rocket.y > self.height - 20:
                rocket.y = self.height - 20
                rocket.flying = False
                self.vx = 0
                self.vy = 0
                self.rv = 0
                
            if rocket.y < 20:
                rocket.y = 20
                rocket.landed(False, self.obstacle_list[0].center_x)
            
            if arcade.check_for_collision_with_list(rocket.sprite, self.obstacle_list):
                rocket.y = 40
                rocket.landed(True, self.obstacle_list[0].center_x)


            #Make Ai chose what to do
            if rocket.flying:
                rocket.vy -= self.gravity
                rocket.think()
                rocket.update()

            

            #update srites
            rocket.sprite.center_x = rocket.x
            rocket.sprite.center_y = rocket.y
            rocket.sprite.angle = -rocket.r

        if(all(not(r.flying) for r in self.rockets) or self.ticks > 1000):
            
            self.rockets.sort(key=lambda r: r.score, reverse=True)

            print("scores:")
            for x in range(3):
                print(self.rockets[x].score)

            for x in range(round((len(self.rockets))/2)-1):
                self.rockets[len(self.rockets)- 1 - x].brain = copy.deepcopy(self.rockets[x].brain)   
                self.rockets[len(self.rockets)- 1 - x].brain.mutate() 


            for rocket in self.rockets:
                rocket.x = 50
                rocket.y = self.height - 50
                rocket.vy = 0
                rocket.vx = 0
                rocket.r = 0
                rocket.rv = 0
                rocket.score = 0
                rocket.flying = True
                rocket.ticks = 0
            self.ticks = 0

        self.ticks +=1
            


window = game()
arcade.run()
        