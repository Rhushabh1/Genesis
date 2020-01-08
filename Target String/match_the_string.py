import random
from statistics import mean
import string


target_gene = "rhushabh" # string to be made
gene_length = len(target_gene) 
population_size = 20 
iterations = 100 # number of times algorithm is tested
limit = 1000
survival_rate = 0.1 # top fraction to be passed on as it is
mating_rate = 0.5 # fraction of population that mate with each other
gene_mutation_rate = 0.1 
gene_transfer_rate = (1-gene_mutation_rate)/2


# generates a random gene
def random_gene():
	return "".join([ random.choice(string.ascii_letters) for _ in range(gene_length) ])


# generates a random population
def initial_generation():
	colony = [Individual(random_gene()) for _ in range(population_size)]
	return colony


def sort_fitness(individual):
	return individual.fitness


# low fitness value => best match
def cal_fitness(chromosome):
	fitness = 0
	for i in range(gene_length):
		if chromosome[i] != target_gene[i]:
			fitness += 1

	return fitness


class Individual:

	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.fitness = cal_fitness(chromosome)

	def __str__(self):
		return "Chromosome: {}\tFitness: {}".format(self.chromosome, self.fitness)

	def mate(self, partner):
		source = [self.chromosome, partner.chromosome, random_gene()]
		labels = random.choices(population = [0, 1, 2],
								weights = [gene_transfer_rate, gene_transfer_rate, gene_mutation_rate],
								k = gene_length)

		child = "".join([ source[labels[i]][i] for i in range(gene_length) ])
		return Individual(child)


# populate the new generation 
def new_generation(population):
	# get top 10% of the fittest as they are
	top_10 = [population[i] for i in range(int(population_size*survival_rate))]

	# get rest 90% by mating top 50% of the fittest
	first_parents = [random.choice(population[:int(population_size*mating_rate)]) for _ in range(int(population_size*(1-survival_rate))) ]
	second_parents = [random.choice(population[:int(population_size*mating_rate)]) for _ in range(int(population_size*(1-survival_rate))) ]
	rest_90 = [ first_parents[i].mate(second_parents[i]) for i in range(int(population_size*(1-survival_rate))) ]

	top_10.extend(rest_90)
	return top_10


