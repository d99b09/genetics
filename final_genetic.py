import numpy as np
import time
import random
import math



def random_q(par):

    number_q = par[0]
    min_q = par[4]
    max_q = par[5]

    out_vector = []
    for i in range(number_q):
        out_vector.append(random.uniform(min_q[i], max_q[i]))
    return out_vector

def random_X(par, num_of_select):
    out_vector = []
    for i in range(num_of_select):
        out_vector.append(random_q(par))
    return out_vector

def find_xyz(par, q):
    
    time.process_time()

    number_q = par[0]
    a = par[1]
    alf = par[2]
    d = par[3]

    T=np.identity(4)
    for i in range(number_q):
        r11=math.cos(q[i])
        r12=-math.sin(q[i])
        r21=math.sin(q[i])*math.cos(alf[i])
        r22=math.cos(q[i])*math.cos(alf[i])
        r23=-math.sin(alf[i])
        r31=math.sin(q[i])*math.sin(alf[i])
        r32=math.cos(q[i])*math.sin(alf[i])
        r33=math.cos(alf[i])
        x0=a[i]
        y0=-math.sin(alf[i])*d[i]
        z0=math.cos(alf[i])*d[i]
        T0=np.array([[r11,r12,0,x0],
            [r21,r22,r23,y0],
            [r31, r32, r33, z0],
            [0,0,0,1]])
        T = np.dot(T, T0)
    x=T[0][3]
    y=T[1][3]
    z=T[2][3]
    return x, y, z

def score_funct(par, member, T):
    x, y, z = find_xyz(par, member)
    result = math.sqrt((x - T[0]) ** 2 + (y - T[1]) ** 2 + (z - T[2]) ** 2)
    return result

def mutate(member, par):
    min_q = par[4]
    max_q = par[5]
    T = member
    mutated = []

    for i in range(len(T)):
        input_vector=list(T[i])
        max_index=len(input_vector)
        mutated_index = random.choice(range(0, max_index))
        mutation_scalar=2*random.random()*input_vector[mutated_index]
        while True:
            if ((mutation_scalar < min_q[mutated_index]) and (mutation_scalar > max_q[mutated_index])):
                break
            else:
                mutation_scalar = 2 * random.random() * input_vector[mutated_index]

        output_vector = input_vector[:]
        output_vector[mutated_index] = mutation_scalar
        mutated.append(output_vector)
    return mutated

def reproduce(par, member, k):
    output = []
    for i in range(k):
        mut = mutate(member, par)
        for j in range(len(mut)):
            vec = mut[j]
            output.append(vec)
    return output

def select(par, offsprings, size, T):
    survival_value = map(lambda x: (score_funct(par, x, T), x), offsprings)
    select = list(map(lambda xy: xy[1], sorted(survival_value)[:size]))
    return select

def next_generation(par, generation, offspring_size, T):
    survival_size = len(generation)
    offsprings = []
    offsprings.append(generation[0])
    offsprings += reproduce(par, generation, offspring_size)
    next_generation = select(par, offsprings, survival_size, T)
    return next_generation

def is_approximate(par, generation, T):

    if (score_funct(par, generation[0], T))<0.01:
        return True
    else:
        return False

def evolution(par, T, num_of_select=20, num_of_offsprings = 40, max_num_generations=1000):

    generation = random_X(par, num_of_select)
    generation_index = 1
    while True:
        generation = next_generation(par, generation, num_of_offsprings, T)
        generation_index += 1
        if generation_index > max_num_generations:
            break
        elif is_approximate(par, generation, T):
            break
    q = generation[0]
    result = score_funct(q, T, par)
    return q, result

par=[3,[3,2,1],[0,0,0],[0,0,0],[0, -math.pi , math.pi], [math.pi/2,math.pi,math.pi]]
T=[4.8,2.8,0]



print(evolution(par, T))
print(time.process_time())
