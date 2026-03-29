import arcade
import random
import copy
from rocket import Rocket
from generate_terrain import generate_terrain

ROCKET_AMOUNT = 100


def get_default_window_size():
    """Choose a large default window size based on the active display."""
    try:
        screen_w, screen_h = arcade.get_display_size()
    except Exception:
        # Safe fallback if display size cannot be detected.
        return 1200, 800

    # Keep a small margin so desktop bars and window borders don't clip content.
    return max(800, int(screen_w * 0.9)), max(600, int(screen_h * 0.9))

class Game(arcade.Window):
    def __init__(self, width=None, height=None):
        if width is None or height is None:
            width, height = get_default_window_size()

        super().__init__(width, height, "Rocket Game", resizable=True)
        self.set_update_rate(1 / 60)
        
        self.generations = 1
        self.width = width
        self.height = height
        self.gravity = 10 / 60
        self.rocket_amount = ROCKET_AMOUNT

        arcade.set_background_color(arcade.color.BLACK)

        self.rocket_draw_amount = self.rocket_amount
        self.section_width = 5
        #self.terrain = generate_terrain(self.section_width, width)

        # Create rockets
        self.rockets = []
        self.rocket_sprites = arcade.SpriteList()
        for _ in range(self.rocket_amount):
            new_rocket = Rocket()
            new_rocket.x = self._randint_clamped_to_window(50, width - 850)
            new_rocket.y = self.height - 50
            new_rocket.starting_position = new_rocket.x

            # Create sprite for rockets
            new_rocket.sprite = arcade.Sprite("imgs/rocket.png", scale=0.01)
            new_rocket.sprite.center_x = new_rocket.x
            new_rocket.sprite.center_y = new_rocket.y

            self.rockets.append(new_rocket)
            self.rocket_sprites.append(new_rocket.sprite)

        # Create landing pad
        self.obstacle_list = arcade.SpriteList()
        obstacle = arcade.Sprite("imgs/landing_pad.png", 0.01)
        obstacle.center_x = self._randint_clamped_to_window(300, width - 50)
        obstacle.center_y = 10
        self.obstacle_list.append(obstacle)
        self.ticks = 0

    def _randint_clamped_to_window(self, start, stop):
        """Return a valid random X position even when requested bounds invert."""
        max_x = max(0, int(self.width - 1))
        start = max(0, min(int(start), max_x))
        stop = max(0, min(int(stop), max_x))

        if stop < start:
            start, stop = stop, start

        return random.randint(start, stop)

    def on_draw(self):
        # In modern arcade, call clear() inside on_draw instead of start_render()
        self.clear()

        # Draw rockets (Sprite.draw is unavailable in current arcade; use SpriteList)
        self.rocket_sprites.draw()

        # Draw landing pad
        self.obstacle_list.draw()
        self.goal = self.obstacle_list[0].center_x

    def on_update(self, delta_time):
        for rocket in self.rockets:
            if rocket.flying:
                rocket.vy -= self.gravity
                rocket.think()
                rocket.update()

            # Update rocket sprites
            rocket.sprite.center_x = rocket.x
            rocket.sprite.center_y = rocket.y
            rocket.sprite.angle = -rocket.r
        
            # Check if rocket has landed or crashed
            if rocket.y < 20:
                rocket.y = 20
                rocket.landed(False, self.obstacle_list[0].center_x)
            
            if arcade.check_for_collision_with_list(rocket.sprite, self.obstacle_list):
                rocket.y = 40
                rocket.landed(True, self.obstacle_list[0].center_x)

        # Check if all rockets have landed or time limit reached
        if all(not rocket.flying for rocket in self.rockets) or self.ticks > 400:
            self.rockets.sort(key=lambda r: r.score, reverse=True)

            print("Generation: " + str(self.generations) + " - " + 
            str(sum(rocket.score for rocket in self.rockets) / len(self.rockets)))
            for i in range(3):
                print(self.rockets[i].score)

            # Breed new generation of rockets
            for i in range(len(self.rockets) // 2):
                self.rockets[-1 - i].brain = copy.deepcopy(self.rockets[i].brain)
                self.rockets[-1 - i].brain.mutate()

            # Reset landing pad position
            self.obstacle_list[0].center_x = self._randint_clamped_to_window(600, self.width - 50)
                
            # Reset rockets
            for rocket in self.rockets:
                rocket.x = self._randint_clamped_to_window(50, self.width - 650)
                rocket.starting_position = rocket.x
                rocket.y = self.height - 50
                rocket.vy = 0 #-random.random()
                rocket.vx = 0 #(random.random() - 0.5) * 2
                rocket.r = random.randint(-45, 45)
                rocket.rv = 0
                rocket.score = 0
                rocket.flying = True
                rocket.ticks = 0
                self.goal = self.obstacle_list[0].center_x

            self.ticks = 0
            self.generations += 1

        self.ticks += 1

# Run the game
window = Game()
arcade.run()
