# encoding: utf-8
import time
import math
from random import random, randint
import numpy as np

def es(fitness, bounds_min, bounds_max, mu, lambda_, dimension, sigma_init=1, sigma_min=float('-inf'), tau=None, maxiter=float('inf'), max_execution_time=float('inf')):
    if not tau:
        tau = 1/math.sqrt(2*dimension)
    population_x = np.random.uniform(bounds_min, bounds_max, size=(1, mu, dimension))[0]
    population = [(xi, sigma_init, fitness(xi)) for xi in population_x] 
    iterations = 0
    start_time = time.time()
    fitness_evolution = []
    while True:
        for l in range(lambda_):
            recombinant = recombine(population, mu, fitness)
            offspring_individual_sigma = recombinant[1] * math.exp(tau*random())
            mutation = offspring_individual_sigma*np.random.randn(1,dimension)[0]
            offspring_individual_x = recombinant[0]+mutation
            #print mutation
            offspring_individual_fitness = fitness(offspring_individual_x)
            population.append((offspring_individual_x, offspring_individual_sigma, offspring_individual_fitness))
        population = sort_poulation(population, mu)
        iterations += 1
        fitness_evolution.append(population[0][2])
        if population[0][1] < sigma_min or maxiter < iterations or start_time+max_execution_time < time.time():
            return population[0], fitness_evolution

def recombine(population, mu, fitness):
    population = sort_poulation(population, mu)
    dimension = len(population[0][0])
    x = []
    sigma = 0
    for i in range(dimension):
        individual = population[randint(0, mu-1)]
        x.append(individual[0][i])
        sigma += individual[1]
    return (x, sigma/mu, fitness(x))

def sort_poulation(population, mu):
    return sorted(population, key=lambda x: x[2])[:mu]

if __name__ == '__main__':
    def rastrigin(x):
        n = len(x)
        value = 10*n + sum([x[i]**2 - 10*math.cos(2*math.pi*x[i]) for i in range(n)])
        return value
    result = es(fitness=rastrigin, bounds_min=-5.12, bounds_max=5.12, mu=20, lambda_=5, dimension=5, maxiter=200, sigma_init=20)
    import matplotlib.pyplot as plt
    plt.plot(range(len(result[1])), result[1])
    print result[0]
    plt.savefig('es.png')
