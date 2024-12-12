

def calculate_score(rocket, on_pad, landing_pad_x):
    score = 10000
    score -= abs((landing_pad_x - rocket.x))
    score -= abs(rocket.r)
    score -= abs(rocket.vy * 5)
    score -= abs(rocket.ticks / 500)
    if on_pad:
        score += 100
    return score
