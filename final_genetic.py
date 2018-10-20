import math
import random

def random_q(number_q):
    out_vector=[]
    for i in range(0,number_q):
        out_vector.append(random.random()*2*math.pi)
    return out_vector

def random_X(number_q, num_of_select):
    out_vector = []
    for i in range(num_of_select):
        out_vector.append(random_q(number_q))
    return out_vector


def score_funct(member,T):
    # Parametrs
    l = 5
    #then add to function
    q = member
    result = math.sqrt(l * (
                (math.cos(q[0] + q[1] + q[2]) - T[0][0]) ** 2 + (-math.sin(q[0] + q[1] + q[2]) - T[0][1]) ** 2 + (
                    math.cos(q[0] + q[1] + q[2]) - T[1][1]) ** 2 + (
                            math.sin(q[0] + q[1] + q[2]) - T[1][0]) ** 2) + (
                                    l * (math.cos(q[0] + q[1] + q[2]) + math.cos(q[0] + q[1]) + math.cos(q[0])) -
                                    T[0][3]) ** 2 + (
                                    l * (math.sin(q[0] + q[1] + q[2]) + math.sin(q[0] + q[1]) + math.sin(q[0])) -
                                    T[1][3]) ** 2)
    return result

def mutate(member):
    T=member
    mutated = []

    for i in range(len(T)):
        input_vector=list(T[i])
        max_index=len(input_vector)
        mutated_index = random.choice(range(0, max_index))
        mutation_scalar=4*random.random()*input_vector[mutated_index]
        output_vector = input_vector[:]
        output_vector[mutated_index] = mutation_scalar
        mutated.append(output_vector)
    return mutated

def reproduce(member, k):
    output = []
    for i in range(0, k):
        mut=mutate(member)
        for j in range(len(mut)):
            vec=mut[j]
            output.append(vec)

    return output

def select(offsprings, size,T):
    survival_value = map(lambda x: (score_funct(x,T), x), offsprings)
    select = list(map(lambda xy: xy[1], sorted(survival_value)[:size]))
    return select

def next_generation(generation, offspring_size,T):
    survival_size=len(generation)
    offsprings = []
    offsprings.append(generation[0])
    offsprings += reproduce(generation, offspring_size)
    next_generation = select(offsprings, survival_size,T)
    return next_generation

def evolution(number_q,T,num_of_select,max_num_generations=2000):
    generation=random_X(number_q, num_of_select)
    num_of_offsprings = 100
    generation_index = 1
    while True:
        generation = next_generation(generation, num_of_offsprings,T)
        generation_index += 1
        if generation_index > max_num_generations:
            break
    q=generation[0]
    result=score_funct(q,T)

    return q, result
