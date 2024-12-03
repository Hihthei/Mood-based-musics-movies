import random
import json

titles = "abcdefghijklmnopqrstuvwxyz"
moods = ["happy", "chill", "sad", "angry", "exciting"]
types = [0, 1]

file_path = "../App/tmp_songs_base.txt"
with open(file_path, "w") as pf:
    for idx in range(50):
        pf.write(f"('{idx}', '{"".join([random.choice(titles) for _ in range(random.randint(5, 10))])}', '{random.choice(types)}'),\n")

