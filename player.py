import numpy as np

class Player:
    """
    A class representing an individual player, their strategy and their reward.
    """
    def __init__(self, name, strat=None, strat_size=10, lp=0.33):
        """
        Produce a new player with a possibly random initial strategy parametrised by size (strat_size)
        and learable proportion (lp).
        """
        self.name = name
        if strat is None:
            self.base_strategy = np.random.randint(0, 2, strat_size)
            for i in range(len(self.base_strategy)):
                if np.random.random() <= lp:
                    self.base_strategy[i] = 2
        else:
            self.base_strategy = strat
        self.lr = lp
        self.reset()

    def reset(self):
        self.strategy = None
        self.mutate()
        self.reward = 0
    
    def mutate(self):
        """
        Apply random learning procedure to assign "?" bits 0 or 1
        """
        self.strategy = [n if n != 2 else np.random.randint(0, 2) for n in self.base_strategy]

    def __str__(self):
        return f"{self.name}: {self.strategy}"
