import random

from statistics import mean

import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame


def scenario(value, bid_size, multiplier, chance):
    result = random.choices((True, False), weights=[chance, 1 - chance], k=1)[0]
    value = value - (bid_size * value) + (multiplier[result] * bid_size * value)
    return {True: (1, 0), False: (0, 1)}[result], value


def run(
    instance: int, bid_size, multiplier={True: 1.25, False: 0.6}, chance=0.5, rolls=50
):
    s = []
    value = 1000.0
    results = (0, 0)
    sequence = [((0, 0), value)]
    for instances in range(1, rolls + 1):
        result, value = scenario(value, bid_size, multiplier, chance)
        results = results[0] + result[0], results[1] + result[1]
        sequence.append((result, value, instance))
        if instances % 3:
            s.append(
                {
                    "Rolls": instances,
                    "Money": value,
                    "Instance": instance,
                    "WinLose": result,
                }
            )
        if not round(value):
            s.append(
                {
                    "Rolls": instances,
                    "Money": value,
                    "Instance": instance,
                    "WinLose": result,
                }
            )
            break
    return sequence, s


if __name__ == "__main__":
    multiplier = {True: 1.15, False: 0.7}
    chance = 0.85
    bid_size = 0.05
    runs = 2000
    rolls = 300
    all_results = []
    for instance in range(runs):
        all_results.append({"Rolls": 0, "Money": 1000, "Instance": instance})
    for instance in range(runs):
        _, result = run(instance, bid_size, multiplier, chance, rolls)
        all_results.extend(result)
    df = DataFrame(all_results, columns=["Rolls", "Money", "Instance"])
    print(
        f"""
    Max: {max([v["Money"] for v in all_results])}
    Min: {min([v["Money"] for v in all_results])}
    Mean: {mean([v["Money"] for v in all_results])}
    """
    )
    sns.lineplot(data=df, x="Rolls", y="Money", hue="Instance", size=0)
    plt.show()
