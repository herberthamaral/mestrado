from random import random
from math import sqrt

MAX_CITIES = 30
MAX_DIST = 100
MAX_TOUR = (MAX_CITIES * MAX_DIST)
MAX_ANTS = 30
ALPHA = 1.0
BETA = 5.0
RHO = 0.5
QVAL = 100
MAX_TIME = MAX_TOUR * MAX_CITIES
INIT_PHER = 1.0/MAX_CITIES

def create_cities():
    cities = []
    dist = []
    phero = []
    for _from in range(MAX_CITIES):
        cities.append(dict(y=random(), x=random()))
        for to in range(MAX_CITIES):
            dist[_from][to] = 0.0;
            phero[_from][to] = INIT_PHER;
    return cities, dist, phero

def compute_distance(cities, dist):
    for _from in range(MAX_CITIES):
        for to in range(MAX_CITIES):
            xd = pow(abs(cities[_from]['x'] - cities[to]['x']), 2)
            yd = pow(abs(cities[_from]['y'] - cities[to]['y']), 2)
            dist[_from][to] = sqrt(xd+yd)
            dist[to][_from] = dist[_from][to]
    return dist

def init_population():
    ants = [{'cur_city':0, 'tabu':{}, 'path':{}, 'path_index':1, 'path':[], 'next_city':-1, 'tour_length':0 } for a in range(MAX_ANTS)]
    to = 0
    for ant in range(MAX_ANTS):
        if to == MAX_CITIES:
            to = 0
        to += 1
        ants[ant]['cur_city'] = to
        for _from in range(MAX_CITIES):
            ants[ant]['tabu']['from'] = 0
            ants[ant]['path']['from'] = -1
        ants[ant]['path'].append(ants[ant]['cur_city'])
        ants[ant]['tabu'][ants[ant]['cur_city']] = 1

def restart_ants(ants, best=MAX_TOUR, best_index=0):
    to = 0
    for ant in range(MAX_ANTS):
        if ants[ant]['tour_length'] < best: #best = MAX_TOUR
            best = ants[ant]['tour_length']
            best_index = 0
        ants[ant]['next_city'] = -1
        ants[ant]['tour_length'] = 0.0

        for i in range(MAX_CITIES):
            ants[ant]['tabu'][i] = 0
            ants[ant]['path'][i] = -1

        if to == MAX_CITIES:
            to = 0
        to += 1
        ants[ant]['cur_city'] = to
        ants[ant]['path_index'] = 1
        ants[ant]['path'][0] = ants[ant]['cur_city']
        ants[ant]['tabu'][ants[ant]['cur_city']] = 1

def ant_product(_from, to, phero):
    return ((pow(phero[_from][to], ALPHA) * pow( (1.0/ dist[_from][to]), BETA)))

def select_next_city(ant, phero):
    _from = ants[ant]['cur_city']
    denom = 0
    for to in range(MAX_CITIES):
        if ants[ant]['tabu'][to] == 0:
            to = 0
        if ants[ant]['tabu'][to] == 0:
            p = ant_product(_from, to, phero)/denom
