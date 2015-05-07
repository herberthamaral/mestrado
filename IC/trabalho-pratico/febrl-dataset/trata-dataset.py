# encoding utf-8
import jellyfish
dataset = [linha.split(',') for linha in open('dataset1.csv', 'r').read().split('\n')]
