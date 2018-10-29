import math
import random
import time

time.process_time()

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

def find_xyz(num_q, q, par_l,  par_q):
    x=0
    y=0
    z=0
    q_x=0
    q_y1=0
    q_y0=0
    q_z=0

    for i in range(num_q):
        if par_q[i]:
            q_x += q[i]
            q_y1 += q[i]
            x += par_l[i] * math.cos(q_y1)
            y += par_l[i] * math.sin(q_z)
        else:
            q_y0 += q[i]
            q_z += q[i]
            y += par_l[i] * math.cos(q_y0)
            z += par_l[i] * math.sin(q_z)
    return x, y, z

def score_funct(member, T, par_l, par_q):
    num_q=len(member)
    x, y, z = find_xyz(num_q, member, par_l, par_q)
    result = math.sqrt((x - T[0]) ** 2 + (y - T[1]) ** 2 + (z - T[2]) ** 2)
    return result

def mutate(member):
    T = member
    mutated = []

    for i in range(len(T)):
        input_vector=list(T[i])
        max_index=len(input_vector)
        mutated_index = random.choice(range(0, max_index))
        mutation_scalar=2*random.random()*input_vector[mutated_index]
        output_vector = input_vector[:]
        output_vector[mutated_index] = mutation_scalar
        mutated.append(output_vector)
    return mutated

def reproduce(member, k):
    output = []
    for i in range(0, k):
        mut = mutate(member)
        for j in range(len(mut)):
            vec = mut[j]
            output.append(vec)

    return output

def select(offsprings, size, T, par_l, par_q):
    survival_value = map(lambda x: (score_funct(x, T, par_l, par_q), x), offsprings)
    select = list(map(lambda xy: xy[1], sorted(survival_value)[:size]))
    return select

def next_generation(generation, offspring_size,T, par_l, par_q):
    survival_size = len(generation)
    offsprings = []
    offsprings.append(generation[0])
    offsprings += reproduce(generation, offspring_size)
    next_generation = select(offsprings, survival_size, T, par_l, par_q)
    return next_generation

def evolution(number_q, T, par_l, par_q, num_of_select=20, num_of_offsprings = 40, max_num_generations=1000):
    generation = random_X(number_q, num_of_select)
    generation_index = 1
    while True:
        generation = next_generation(generation, num_of_offsprings, T, par_l, par_q)
        generation_index += 1
        if generation_index > max_num_generations:
            break
    q=generation[0]
    result=score_funct(q, T, par_l, par_q)
    return q, result

T = [0, 10, 8]
par_l=[5, 5, 5]
par_q=[0, 0, 0]

print(evolution(3, T, par_l, par_q))
print(time.process_time())
