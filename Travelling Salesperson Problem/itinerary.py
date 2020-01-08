from traveller import *
import matplotlib.pyplot as plt 
from matplotlib import style
from math import sin, cos, pi
style.use("ggplot")


fitness_plot_enabled = True
side_len = 1
plot_size = 1.5

coords = [[side_len*cos(2*pi*i/city_count) , side_len*sin(2*pi*i/city_count)] for i in range(city_count)]
xs, ys = map(list, zip(*coords)) 


def intialize_map():
	plt.figure("itinerary")
	plt.scatter(xs,ys)
	plt.xlim(-plot_size,plot_size)
	plt.ylim(-plot_size,plot_size)

	for i in range(len(coords)):
		plt.annotate(i, # this is the text
					(xs[i], ys[i]), # this is the point to label
					textcoords="offset points", # how to position the text
					xytext=(xs[i]*10, ys[i]*10), # distance from text to points (x,y)
					ha='center') # horizontal alignment can be left, right or center
	plt.show(block = False)


def draw_map(individual):
	px = [xs[i] for i in individual.chromosome]
	py = [ys[i] for i in individual.chromosome]
	px.append(px[0])
	py.append(py[0])
	plt.plot(px, py, color = 'b')
	plt.show(block = False)


def main():
	generation = 0
	population = initial_generation()
	fitness_level = []

	while generation < limit:

		population.sort(key = sort_fitness)
		fitness_level.append(population[0].fitness)
		# print("Generation: {}\t{}".format(generation, population[0]))

		if fitness_plot_enabled:
			plt.figure("fitness_level")
			plt.plot(list(range(generation + 1)),fitness_level)
			plt.show(block = False)

			# evolution plot 
			intialize_map()
			draw_map(population[0])
			plt.show(block = False)
			plt.pause(0.001)

			if population[0].fitness == city_count or generation == limit-1:
				plt.show(block = True)
				break
			else:
				plt.clf()

		population = new_generation(population)
		generation += 1

	return generation


main() # don't forget the print statement


