iimport math
import random

class Creature:

    def __init__(self, appearance, genes):
        self.appearance = appearance
        self.genes = genes

    def __lt__(self, other):
        if self.appearance < other.appearance:
            return True
        return False


    def get_appearance(self):
        return self.appearance

    def get_genes(self):
        return self.genes[:]




#Input: number_q(0D matrix) - число углов в манипуляторе
#Output: out_vector(1D matrix) - случайный список размера number_q со элементами в диапазоне от 0 до 2*pi
def random_q(number_q):
    out_vector=[]
    for i in range(0,number_q):
        out_vector.append(random.random()*2*math.pi)
    return out_vector



#Input: member(1D matrix) - список углов
#Output: result (0D matrix)- "расстояние" до требуемого результата
def score_funct(member):
    # Parametrs
    l = 5
    #then add to function
    T = [[-0.25, -0.96, 0, 10.62],
         [0.96, 0.25, 0, 7.33],
         [0, 0, 1, 0],
         [0, 0, 0, 1]
        ]
    q = member.get_appearance()
    result = math.sqrt(l * (
                (math.cos(q[0] + q[1] + q[2]) - T[0][0]) ** 2 + (-math.sin(q[0] + q[1] + q[2]) - T[0][1]) ** 2 + (
                    math.cos(q[0] + q[1] + q[2]) - T[1][1]) ** 2 + (
                            math.sin(q[0] + q[1] + q[2]) - T[1][0]) ** 2) + (
                                    l * (math.cos(q[0] + q[1] + q[2]) + math.cos(q[0] + q[1]) + math.cos(q[0])) -
                                    T[0][3]) ** 2 + (
                                    l * (math.sin(q[0] + q[1] + q[2]) + math.sin(q[0] + q[1]) + math.sin(q[0])) -
                                    T[1][3]) ** 2)
    return result


#Input: member(2D matrix) - список списков углов
#Output: mutated(2D matrix) - изменённый список списков углов
def mutate(member):
    input_vector=member.get_appearance()
    genes=member.get_genes()
    genes.append(input_vector)

    input_vector=list(input_vector)
    max_index=len(input_vector)
    mutated_index = random.choice(range(0, max_index))
    mutation_scalar=4*random.random()*input_vector[mutated_index]

    output_vector = input_vector[:]
    output_vector[mutated_index] = mutation_scalar

     # create a new mutated creature
    mutated = Creature(output_vector, genes)
    return mutated

#Input: member(1D matrix) - список углов; k(0D matrix) - число, требуемое количество списков
#Output: output(2D matrix) - список состоящий из k списков углов member
def reproduce(member, k):
    output = []
    for i in range(0, k):
        output.append(mutate(member))
    return output

#Input: offsprings(1D matrix) - список углов; size(0D matrix) - число, требуемое количество списков
#Output: select(2D matrix) - сортированный от меньшего к большему список списков размера size

def select(offsprings, size):
    survival_value = map(lambda x: (score_funct(x), x), offsprings)
    select = list(map(lambda xy: xy[1], sorted(survival_value)[:size]))
    return select


#Input: generation(2D matrix) - исходный список списка углов, offspring_size(0D matrix) - число, требуемое количество списков1; survival_size(0D matrix) - число, требуемое количество списков2
#Output: next_generation(2D matrix) - следующий (улучшенный) список списков углов
def next_generation(generation, offspring_size, survival_size):
    offsprings = []
    for member in generation:
        offsprings += reproduce(member, offspring_size)
    next_generation = select(offsprings, survival_size)
    return next_generation

#Input: generation(2D matrix) - список списков углов
#Output: True, если достигнута конечная цель
def is_aproximate(generation):

    if score_funct(generation[0]) < 5:
        return True
    else:
        return False

#Input: number_q(2D matrix) - число углов манипулятора; max_num_generations - максимальное число генераций
#Output: q(1D matrix) - требуемые задачей углы
def evolution(number_q,max_num_generations=2000):
    random=random_q(number_q)
    root = Creature(random, [])
    generation=[root]
    num_of_offsprings = 100
    num_of_select = 10
    generation_index = 1
    while True:
        generation = next_generation(generation, num_of_offsprings, num_of_select)
        if is_aproximate(generation):
            break
        generation_index += 1
        if generation_index > max_num_generations:
            raise Exception("Not reached in the maximal number of generations")
    q=generation[0]

    return q

