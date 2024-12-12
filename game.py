import arcade
import random
import copy
from rocket import rocket_object
from generate_terrain import generate_terrain

ROCKET_AMOUNT = 100

class game(arcade.Window):
    def __init__(self, width=1200, height=800):
        super().__init__(width, height, "Rocket game")
        self.set_update_rate(1 / 60)
        
        self.width = width
        self.height = height
        self.gravity = 10 / 60
        self.rocket_amount = ROCKET_AMOUNT

        arcade.set_background_color(arcade.color.BLACK)

        self.rocket_draw_amount = self.rocket_amount
        self.section_width = 5
        self.terrain = generate_terrain(self.section_width, width)

        #Create rockets
        self.rockets = []
        for x in range(self.rocket_amount):
            new_rocket = rocket_object()
            new_rocket.x = random.randint(50, width-50)
            new_rocket.y = self.height - 50

            #Create sprite for rockets
            new_rocket.sprite = arcade.Sprite("imgs/rocket.png", scale=0.05)
            new_rocket.sprite.center_x = new_rocket.x
            new_rocket.sprite.center_y = new_rocket.y

            self.rockets.append(new_rocket)

        #Create landing pad
        self.obstacle_list = arcade.SpriteList()
        obstacle = arcade.Sprite("imgs/landing_pad.png", 0.05)
        obstacle.center_x = random.randint(50, width-50)
        obstacle.center_y = 10
        self.obstacle_list.append(obstacle)
        self.ticks = 0

    def on_draw(self):
        arcade.start_render()

        for rocket in self.rockets[0:self.rocket_draw_amount]:
            rocket.sprite.draw()

        self.obstacle_list.draw()
        self.goal = self.obstacle_list[0].center_x

        #generate new terrain
        #for x in range(round(self.width/self.section_width)):
        #    height = self.terrain[x]
        #    arcade.draw_rectangle_filled(x*self.section_width, height/2, self.section_width, height, arcade.color.WHITE)
        

    def update(self, delta_time):
        for rocket in self.rockets:
            #Make Ai chose what to do
            if rocket.flying:
                rocket.vy -= self.gravity
                rocket.think()
                rocket.update()

            #update srites
            rocket.sprite.center_x = rocket.x
            rocket.sprite.center_y = rocket.y
            rocket.sprite.angle = -rocket.r
        
            if rocket.y < 20:
                rocket.y = 20
                rocket.landed(False, self.obstacle_list[0].center_x)
            
            if arcade.check_for_collision_with_list(rocket.sprite, self.obstacle_list):
                rocket.y = 40
                rocket.landed(True, self.obstacle_list[0].center_x)

        if(all(not(r.flying) for r in self.rockets) or self.ticks > 400):
            
            self.rockets.sort(key=lambda r: r.score, reverse=True)

            print("scores:")
            for x in range(3):
                print(self.rockets[x].score)

            for x in range(round((len(self.rockets))/2)):
                self.rockets[len(self.rockets)- 1 - x].brain = copy.deepcopy(self.rockets[x].brain)   
                self.rockets[len(self.rockets)- 1 - x].brain.mutate() 

            self.obstacle_list[0].center_x = random.randint(50, self.width-50)
                
            for rocket in self.rockets:
                rocket.x = random.randint(50, self.width-50)
                rocket.y = self.height - 50
                rocket.vy = -random.random()
                rocket.vx = (random.random() - 0.5) *2
                rocket.r = random.randint(-45, 45)
                rocket.rv = 0
                rocket.score = 0
                rocket.flying = True
                rocket.ticks = 0
                self.goal = self.obstacle_list[0].center_x

            self.ticks = 0
            #self.terrain = generate_terrain(10, self.width)

        self.ticks +=1

            
window = game()
arcade.run()
        