import numpy as np
from matplotlib import pyplot as plt
from population import Population
from player import Player
from environment import Environment

N = 800 # Number of players
GENERATIONS = 30 # Number of generations
ROUNDS = 800 # Number of rounds in a generation
STRAT_SIZE = 20 # Number of "bits" in each strategy
COMPETITION = 1 # Reduces the effect of performance on reproductive odds, see Population.reproduce
LEARNABLE_PROP = 0.5 # Proportion of learnable "bits" in a strategy

def exp_hinton_nowlan():
    population = Population()
    for i in range(N):
        population.append(Player(f"Player {i}", lp=LEARNABLE_PROP, strat_size=STRAT_SIZE))
    env = Environment(population)
    _, strats = env.do_game(gens=GENERATIONS, gen_len=ROUNDS, competition=COMPETITION)
    print(strats[0].shape)
    zero_genes = [np.count_nonzero(strats[i] == 0)/(N*STRAT_SIZE) for i in range(len(strats))]
    one_genes = [np.count_nonzero(strats[i] == 1)/(N*STRAT_SIZE) for i in range(len(strats))]
    question_genes = [np.count_nonzero(strats[i] == 2)/(N*STRAT_SIZE) for i in range(len(strats))]
    
    plt.plot(zero_genes, color="red", label="Incorrect (0) genes")
    plt.plot(one_genes, color="green", label="Correct (1) genes")
    plt.plot(question_genes, color="orange", label="Undecided (?) genes")
    plt.title("Proportions of Gene Types Across Generations.")
    plt.ylabel("Proportion of All Genes")
    plt.xlabel("Generations")
    plt.ylim((0,1))
    plt.legend()
    plt.savefig("out.png")



if __name__ == "__main__":
    #exp_avg_strategy_over_T_trials(10, "demo_fig.png")
    exp_hinton_nowlan()