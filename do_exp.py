import numpy as np
from matplotlib import pyplot as plt
from population import Population
from player import Player
from environment import Environment

N = 100 # Number of players
GENERATIONS = 20 # Number of generations
ROUNDS= 10 # Number of rounds in a generation
STRAT_SIZE = 10 # Number of "bits" in each strategy
COMPETITION = 1 # Reduces the effect of performance on reproductive odds, see Population.reproduce
LEARNABLE_PROP = 0.75 # Proportion of learnable "bits" in a strategy

def exp_avg_strategy_over_T_trials(T, output_file):
    multi_trial_avg = None
    for t in range(T):
        population = Population()
        for i in range(N):
            population.append(Player(f"Player {i}", lp=LEARNABLE_PROP, strat_size=STRAT_SIZE))
        env = Environment(population)

        rs = np.zeros((GENERATIONS, N))
        _, strats = env.do_game(gens=GENERATIONS, gen_len=ROUNDS, competition=COMPETITION)
        strats = np.mean(strats.T, axis=1)
        multi_trial_avg = strats/T if multi_trial_avg is None else multi_trial_avg + strats/T

    plt.imshow(multi_trial_avg, vmin=0, vmax=1)
    plt.xlabel("Rounds")
    plt.ylabel("Average Strategy")
    plt.colorbar()
    plt.savefig(output_file)


if __name__ == "__main__":
    exp_avg_strategy_over_T_trials(10, "demo_fig.png")
