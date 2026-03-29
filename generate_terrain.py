import random

def generate_terrain(section_width, screen_width):
    spread = 10
    terrain_list = []
    terrain_list.append(random.randint(1,50))
    for x in range(int(screen_width/section_width/spread)+1):
        second_point = random.randint(1,50)
        current_point = terrain_list[x*spread]
        for i in range(spread):
            if current_point < second_point:
                current_point += round((random.random()+0.5) * (abs(second_point - terrain_list[x*spread])/spread) /2)
            else:
                current_point -= round((random.random()+0.5) * (abs(second_point - terrain_list[x*spread])/spread) /2)
            terrain_list.append(current_point)
        terrain_list.append(second_point)

    return terrain_list

