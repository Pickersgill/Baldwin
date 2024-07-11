import numpy as np
import random

from player import Player

class Population(list):
    """
    Extension of list class which can produce further populations via reproductive process.
    """
    def __init__(self):
        super().__init__()

    def mutate(self):
        for player in self:
            player.mutate()

    def reproduce(self, competition=20):
        """
        Simulate reproduction based on population rewards and return the new population.
        Competition parameter effects the power of reward/success on reproduction.
        Competition=0 means expected proportion of genes in the next gene pool belonging
        to a player is exactly equal to their proportion of total reward.
        As competition approaches infinity reproductive odds approach uniform distribution.
        """
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
        """
        Merge 2 strategies with a random cutoff.
        """
        if not split:
            split = np.random.randint(0, min(len(p1.strategy),len(p2.strategy))) 
        new_lr = (p1.lr + p2.lr)/2
        return Player(p1.name+"son", np.concatenate([p1.base_strategy[:split], p2.base_strategy[split:]]))

    def reset(self):
        for player in self:
            player.reset()

    def __str__(self):
        return f"[{', '.join(str(l) for l in self)}]"