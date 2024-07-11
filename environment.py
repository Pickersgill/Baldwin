
import numpy as np

class Environment:
    """
    A class for handling the simulation of a population of players.
    """
    def __init__(self, population):
        self.population = population

    def smooth_score(self, strat):
        """
        Scores a strategy in proportion to the number of "1" bits it contains
        """
        s = sum(strat) / len(strat)
        return s

    def score(self, strat):
        """
        Scores a strategy discretely, all strategies receive a score of 0 unless they contain only 1s
        """
        s = np.floor(self.smooth_score(strat))
        return s

    def do_generation(self, rounds=100):
        """
        Simulates a generation of play for given number of rounds.
        Score is awarded to each player after each round.
        Mutation occurs in each round.
        """
        for i in range(rounds):
            for player in self.population:
                score = self.score(player.strategy)
                player.reward += score
                if score == 0:
                    player.mutate()

    def do_game(self, gens=100, gen_len=100, competition=20):
        """
        Simulates a game consisting of many generations of play for given number of generations.
        Strategies and scores are recorded during each round.
        """
        rewards = np.zeros((gens, len(self.population)))
        strat_size = len(self.population[0].strategy)
        strats = np.zeros((gens, len(self.population), strat_size))
        for i in range(gens):
            print(f"Round {i}", end="\r")
            self.do_generation(gen_len)
            rewards[i] = [p.reward for p in self.population]
            strats[i] = np.array([p.strategy for p in self.population])
            self.population = self.population.reproduce(competition=competition)
            self.reset()
        return rewards, strats
    
    def reset(self):
        """
        Reset the population to the initial configuration.
        """
        self.population.reset()