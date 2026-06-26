def save_score(result, score, battle_time):
    with open("DBScore", "a") as file:
        file.write(
            f"{result} | Score: {score} | Time: {battle_time}s\n"
        )


def load_scores():
    try:
        with open("DBScore", "r") as file:
            return file.readlines()
    except:
        return []