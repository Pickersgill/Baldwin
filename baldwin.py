import numpy as np
from matplotlib import pyplot as plt
import random

class Population(list):
    def __init__(self):
        super().__init__()

    def mutate(self):
        for player in self:
            player.mutate()

    def reproduce(self, competition=20):
        odds = np.zeros(len(self))
        for i, player in enumerate(self):
            odds[i] = player.reward
        odds = (competition + odds) / sum(competition + odds)
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
    def __init__(self, name, strat=None, strat_size=10, lr=0.33):
        self.name = name
        if strat is None:
            self.base_strategy = np.random.randint(0, 2, strat_size)
            for i in range(len(self.base_strategy)):
                if np.random.random() <= lr:
                    self.base_strategy[i] = 2
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

    def smooth_score(self, strat):
        s = sum(strat) / len(strat)
        return s

    def score(self, strat):
        s = np.floor(self.smooth_score(strat))
        return s

    def do_generation(self, steps=100):
        for i in range(steps):
            for player in self.population:
                score = self.score(player.strategy)
                player.reward += score
                if score == 0:
                    player.mutate()

    def do_game(self, rounds=100, round_len=100, competition=20):
        rewards = np.zeros((rounds, len(self.population)))
        for i in range(rounds):
            print(f"Round {i}", end="\r")
            self.do_generation(round_len)
            rewards[i] = [p.reward for p in self.population]
            self.population = self.population.reproduce(competition=competition)
            self.reset()
        return rewards
    
    def reset(self):
        self.population.reset()

N = 50
ROUNDS = 20
#ROUND_LENS = [10, 20, 30, 40, 50]
ROUND_LEN = 50
STRAT_SIZE = 10

population = Population()
for i in range(N):
    population.append(Player(f"Player {i}", lr=0.2, strat_size=STRAT_SIZE))
env = Environment(population)

tests = 1
rs = np.zeros((ROUNDS, N))

for t in range(tests):
    print(f"\n{t}")
    rs += env.do_game(rounds=ROUNDS, round_len=ROUND_LEN, competition=25)/ROUND_LEN

plt.imshow(rs.T, vmin=0, vmax=1)
plt.xlabel("Rounds")
plt.ylabel("Players")
plt.colorbar()
plt.show()


