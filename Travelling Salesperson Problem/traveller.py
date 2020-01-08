import random


city_count = 15
gene_length = city_count
population_size = 20
iterations = 100 # number of times algorithm is tested
limit = 300
survival_rate = 0.1 # top fraction to be passed on as it is
mating_rate = 0.5 # fraction of population that mate with each other
gene_mutation_rate = 0.2
gene_transfer_rate = (1-gene_mutation_rate)/2
adj = [] # adjacency matrix


# grid should be a closed path
def generate_grid():
	def shortest_path(x,y):
		return min(abs(x-y) , city_count - abs(x-y))

	grid = [[shortest_path(i,j) for j in range(city_count)] for i in range(city_count)]
	return grid	

adj = generate_grid()


def random_gene():
	gene = list(range(gene_length))
	random.shuffle(gene)
	return gene


def initial_generation():
	colony = [Individual(random_gene()) for _ in range(population_size)]
	return colony 


def cal_fitness(gene):
	fitness = adj[gene[0]][gene[-1]]
	for i in range(len(gene)-1):
		fitness += adj[gene[i]][gene[i+1]]

	return fitness


def sort_fitness(individual):
	return individual.fitness


class Individual:

	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.fitness = cal_fitness(chromosome)

	def __str__(self):
		return "Gene: {}\tFitness: {}".format(self.chromosome, self.fitness)

	def mate(self, partner):
		child = self.chromosome[:]
		front = random.randrange(len(child))
		rear = (int(front + gene_length*0.5 - 1))%gene_length

		# find strand of self.chromosome
		if front < rear:
			t = child[front:rear+1]
		else:
			t = child[front:]
			t.extend(child[:rear+1])

		# copy the rest of partner.chromosome
		x = (rear+1)%gene_length
		ptr = partner.chromosome.index(child[rear])
		while x != front:
			if partner.chromosome[ptr] not in t:
				child[x] = partner.chromosome[ptr]
				x = (x+1)%gene_length
			ptr = (ptr+1)%gene_length

		# introduce mutations by swapping the 1st half with 2nd half
		labels = random.sample(list(range(gene_length)), int(gene_length*gene_mutation_rate))
		random.shuffle(labels)
		sorted_labels = labels[::-1]
		# 	if population[0].fitness == 0:
		# 		found = True
		# 		break
		vals = [child[i] for i in labels]
		for i in range(len(labels)):
			child[sorted_labels[i]] = vals[i]

		return Individual(child)


def new_generation(population):
	# get top 10% of the fittest as they are
	top_10 = [population[i] for i in range(int(population_size*survival_rate))]

	# get rest 90% by mating top 50% of the fittest
	first_parents = [random.choice(population[:int(population_size*mating_rate)]) for _ in range(int(population_size*(1-survival_rate))) ]
	second_parents = [random.choice(population[:int(population_size*mating_rate)]) for _ in range(int(population_size*(1-survival_rate))) ]
	rest_90 = [ first_parents[i].mate(second_parents[i]) for i in range(int(population_size*(1-survival_rate))) ]

	top_10.extend(rest_90)
	return top_10


