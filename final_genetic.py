import math
from genetic import *

def score_funct(q):
    # Parametrs
    l = 5
    T = [[0.7, 0.7, 0, 5],
         [0.7, 0.7, 0, 8],
         [0, 0, 1, 0],
         [0, 0, 0, 1]
         ]
    result = math.sqrt(l * (
                (math.cos(q[0] + q[1] + q[2]) - T[0][0]) ** 2 + (-math.sin(q[0] + q[1] + q[2]) - T[0][1]) ** 2 + (
                    math.cos(q[0] + q[1] + q[2]) - T[1][1]) ** 2 + (math.sin(q[0] + q[1] + q[2]) - T[1][0]) ** 2) + (
                                   l * (math.cos(q[0] + q[1] + q[2]) + math.cos(q[0] + q[1]) + math.cos(q[0])) - T[0][
                               3]) ** 2 + (
                                   l * (math.sin(q[0] + q[1] + q[2]) + math.sin(q[0] + q[1]) + math.sin(q[0])) - T[1][
                               3]) ** 2)
    return result

Q_COUNT=3
POPULATION_SIZE=1000

# Create a random population
pop = Population()
pop.perturb_amount = 0.05
pop.function_crossover = crossover_splice
pop.function_mutate = mutate_perturb
pop.create_population(Q_COUNT,POPULATION_SIZE,0,Q_COUNT,1,1)
pop.goal_maximize = 0

pop.train(score_funct)

# Display results.
print("Final score: " + str(pop.best_genome.score) )
print("Final q_vector: " + str(pop.best_genome.genes))
