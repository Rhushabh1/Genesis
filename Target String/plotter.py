from match_the_string import *
import matplotlib.pyplot as plt 
from matplotlib import style
style.use("ggplot")


fitness_plot_enabled = True


def main():
	generation = 0
	found = False
	population = initial_generation()
	fitness_level = []

	while not found and generation < limit:

		population.sort(key = sort_fitness)
		fitness_level.append(population[0].fitness)
		# print("Generation: {}\t{}".format(generation, population[0]))

		if fitness_plot_enabled:
			plt.figure("fitness_level")
			plt.plot(list(range(generation + 1)),fitness_level)
			plt.ylim(0, gene_length)
			plt.show(block = False)
			plt.pause(0.005)

			if population[0].fitness == 0:
				found = True
				plt.show(block = True)
				break
			plt.clf()
		else:
			if population[0].fitness == 0:
				found = True
				break

		population = new_generation(population)
		generation += 1

	return generation


def plot_generations():
	global fitness_plot_enabled
	fitness_plot_enabled = False
	x = []
	y = []

	for i in range(iterations):
		x.append(i)
		y.append(main())

		plt.figure("generations")
		plt.plot(x,y,color = 'r')
		m = mean(y)
		mean_line = [m for _ in range(i + 1)]
		plt.plot(x,mean_line, color = 'b', label = "mean")
		plt.legend()
		plt.show(block = False)
		plt.pause(0.005)
		if i != iterations-1:
			plt.clf()
		else:
			plt.show(block = True)


# main() # don't forget the print statement
plot_generations()


