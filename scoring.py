def calculate_score(rocket, on_pad, landing_pad_x):
    score = 10000
    score -= abs((landing_pad_x - rocket.x))
    score -= abs(rocket.r * 10)
    score -= abs(rocket.vy * 10)
    score -= abs(rocket.ticks / 50)
    if on_pad:
        score += 10
    return score
