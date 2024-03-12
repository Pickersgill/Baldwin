import numpy as np
from matplotlib import pyplot as plt
import random

class Population(list):
    def __init__(self):
        super().__init__()

    def mutate(self):
        for player in self:
            player.mutate()

    def reproduce(self):
        odds = np.zeros(len(self))
        for i, player in enumerate(self):
            odds[i] = player.reward
        odds = (1 + odds) / sum(1 + odds)
        new_pop = Population()
        for i in range(len(self)):
            p1, p2 = random.choices(self, weights=odds, k=2)
            new_pop.append(self.merge(p1, p2))

        return new_pop

    def merge(self, p1, p2, split=None):
        if not split:
            split = np.random.randint(0, min(len(p1.strategy),len(p2.strategy))) 
        return Player(p1.name+"son", np.concatenate([p1.base_strategy[:split], p2.base_strategy[split:]]))

    def reset(self):
        for player in self:
            player.reset()

    def __str__(self):
        return f"[{', '.join(str(l) for l in self)}]"


class Player:
    def __init__(self, name, strat=None):
        self.name = name
        if strat is None:
            self.base_strategy = np.random.randint(0, 3, 10)
        else:
            self.base_strategy = strat
        self.reset()

    def reset(self):
        self.strategy = None
        self.mutate()
        self.reward = 0
    
    def mutate(self):
        self.strategy = [n if n != 2 else np.random.randint(0, 2) for n in self.base_strategy]

    def __str__(self):
        return f"{self.name}: {self.strategy}"


class Environment:
    def __init__(self, population):
        self.population = population

    def score(self, strat):
        return int(all([s for s in strat]))

    def do_generation(self, steps=100):
        for i in range(steps):
            for player in self.population:
                score = self.score(player.strategy)
                player.reward += score
                if score == 0:
                    player.mutate()

    def do_game(self, rounds=100, round_len=100):
        rewards = np.zeros((rounds, len(self.population)))
        for i in range(rounds):
            self.do_generation(round_len)
            rewards[i] = [p.reward for p in self.population]
            self.population = self.population.reproduce()
        return rewards
    
    def reset(self):
        self.population.reset()

population = Population()
N = 100
for i in range(N):
    population.append(Player(f"Player {i}"))

env = Environment(population)
round_lens = [1, 2, 3, 4, 5]

for rl in round_lens:
    rs = env.do_game(rounds=10, round_len=rl) / (np.ones(len(env.population)) / len(env.population))
    xs = np.sum(rs, axis=1)
    plt.plot(xs, label=f"Round Len: {rl}")
    env.reset()

plt.legend()
plt.show()


