# encoding: utf-8

#Exercícios da página 68 do arquivo AG.pdf
import sys
import math
import random
import matplotlib.pyplot as plt

random.seed(123456)

def fitness_ex2(x): #max x = 1.85, y=8.85
    return x*math.sin(10*math.pi*x)+2.0

def popgen_ex2(size):
    return [random.uniform(-1, 2) for i in range(size)]

def valid_ex2(i):
    return i >= -1 and i <= 2

def cost_ex3(x):
    y = 7-x
    return math.pow(x, 2)+math.pow(y, 2)

def popgen_ex3(size):
    # 1 <= x <= 5
    # y >= 3
    # x + y = 7, ou seja: 1 <= x <= 4, y = 7-x é suficiente
    return [random.uniform(1,4) for i in range(size)]

def valid_ex3(x):
    return x>=1 and x<=4

def cost_ex4(x):
    A=10
    n=10
    return A*n+sum([pow(xi, 2)-A*math.cos(2*math.pi*xi) for xi in x])

def popgen_ex4(size):
    return [[random.uniform(-5.12, 5.12) for n in range(10)] for i in range(size)]

def valid_ex4(x):
    return all([(xi >= -5.12 and xi<= 5.12) for xi in x])

def mutation(pop, chance):
    rpop = []
    for p in pop:
        if chance > random.random():
            if type(p) == list:
                p[random.randint(0, len(p)-1)] += random.uniform(-0.5, 0.5)
            else:
                p += random.uniform(-0.2, 0.2)
            rpop.append(p)
        else:
            rpop.append(p)
    return rpop

def order_by_desc(pop, objective_function):
    fpop = sorted([(objective_function(p), p) for p in pop], reverse=True)
    return [p[1] for p in fpop]

def order_by_asc(pop, objective_function):
    fpop = sorted([(objective_function(p), p) for p in pop])
    return [p[1] for p in fpop]

def selection(pop, objective_function, direction):
    pop_fitness = [objective_function(i) for i in pop]
    fitness_pop = float(sum(pop_fitness))
    mean_fitness_pop = fitness_pop/len(pop)
    if direction == 'minimization':
        pop = order_by_desc(pop, objective_function)
    else:
        pop = order_by_asc(pop, objective_function)
    def select():
        p = 0
        for f in pop[::-1]:
            p += objective_function(f)/(fitness_pop*mean_fitness_pop)
            if random.random() <= p:
                break
        return f
    selected = [select(), select()]
    return selected

def crossover(parents):
    if type(parents[0]) in (float, int):
        return (parents[0]+parents[1])/2.0
    else:
        child1, child2 = [], []
        for i, _ in enumerate(parents[0]):
            if random.random() > 0.5:
                child1.append(parents[0][i])
                child2.append(parents[1][i])
            else:
                child2.append(parents[0][i])
                child1.append(parents[1][i])
        return [child1, child2]

def substitution(pop, children, popsize, objective_function, direction, validity_function):
    pop += children
    pop = [p for p in pop if validity_function(p)]
    if direction == 'minimization':
        return order_by_asc(pop, objective_function)[:popsize]
    else:
        return order_by_desc(pop, objective_function)[:popsize]

def evolve(popgen=popgen_ex2, objective_function=fitness_ex2, popsize=10, maxgen=50, pc=0.8, pm=0.1, direction='maximization', validity_function=valid_ex2):
    pop = popgen(popsize)
    better_fit = [pop[0]] if direction=='minimization' else [pop[-1]]
    for g in range(maxgen):
        parents = [selection(pop, objective_function, direction) for p in pop if pc>random.random()]
        children = []
        for p in parents:
            c = crossover(p)
            children.extend(c) if type(c) == list else children.append(c)
        generations_with_no_change = better_fit.count(better_fit[-1])
        children = mutation(children, pm*generations_with_no_change)
        pop = substitution(pop, children, popsize, objective_function, direction, validity_function)
        best_fit = pop[0] if direction=='minimization' else pop[-1]
        better_fit.append(best_fit)
    print u'Melhor indivíduo: {} (fitness: {})'.format(better_fit[-1], objective_function(better_fit[-1]))
    plt.plot(range(maxgen+1), map(objective_function, better_fit))
    plt.ylabel('Fitness')
    plt.xlabel(u'Geração')
    plt.show()

def ex2():
    evolve()

def ex3():
    evolve(popgen_ex3, objective_function=cost_ex3, direction='minimization', validity_function=valid_ex3)

def ex4():
    evolve(popgen_ex4, objective_function=cost_ex4, direction='minimization', validity_function=valid_ex4, maxgen=50)

if __name__ == '__main__':
    functions = dict(ex2=ex2, ex3=ex3, ex4=ex4)
    functions[sys.argv[1]]()
