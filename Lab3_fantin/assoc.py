from random import random
import argparse
import json


def check_property(rep):
    equal_count = 0

    for _ in range(rep):
        x = random()
        y = random()
        z = random()
        if (x + y) + z == x + (y + z):
            equal_count += 1

    return equal_count / rep * 100
    


parser = argparse.ArgumentParser()
parser.add_argument("--repetitions", type=int, default=1000)
args = parser.parse_args()
percentage = check_property(args.repetitions)
print(json.dumps({"repetitions": args.repetitions, "percentage": percentage}))

