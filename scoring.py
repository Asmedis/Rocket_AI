def calculate_score(rocket, on_pad, travel_distance):
    score = 10000
    score += (travel_distance * 5)
    score -= abs(rocket.r * 80)
    score -= abs(rocket.vy * 500)
    score -= abs(rocket.ticks / 50)
    if not on_pad:
        score -= 10
    return score
