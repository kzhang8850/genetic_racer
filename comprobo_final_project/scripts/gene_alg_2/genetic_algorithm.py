#!usr/bin/env python


import csv
import numpy as np
from .generation import Generation


class GeneticAlgorithm(object):

    def __init__(
        self,
        fitness_func,
        log_location,
        gen_size=1024,
        num_genes=4,
        num_organisms=2,
        train_thresh=10000,
        fitness_thresh=0.25,
        elitism_thresh=0.1,
        crossover_thresh=0.8,
        mutation_thresh=0.05):

        self.log_location = log_location

        # Used for training
        self.train_thresh = train_thresh
        self.fitness_thresh = fitness_thresh

        # Rest of the hyperparams are used for evolution
        self._generation = Generation(
            gen_size=gen_size,
            num_genes=num_genes,
            num_organisms=num_organisms,
            elitism_thresh=elitism_thresh,
            crossover_thresh=crossover_thresh,
            mutation_thresh=mutation_thresh,
            fitness_func=fitness_func)


    def train(self):
        """
        Train the algorith and save results to a set location. Results include
        the most fit gene as well as its fitness per generation.
        """

        print "Starting the training session."

        with open(self.log_location,'wb') as file_obj:

            writer = csv.writer(file_obj, delimiter = ',')
            gen_idx = 0
            found = False

            while gen_idx < self.train_thresh:

                # Evaluate the fitness for one generation
                self._generation.evaluate_fitness()
                best_organisms, best_fitnesses = self._generation.get_zeroths()

                # Print out the bests
                for i in range(len(best_organisms)):
                    print"Generation %d: %s" % (gen_idx, best_organisms[i]), \
                            best_fitnesses[i]

                # Save to the log
                row = [gen_idx, np.array(best_organisms).tolist(), best_fitnesses]
                writer.writerow(row)
                file_obj.flush()

                self._generation.evolve()

                gen_idx += 1

        if not found:
            print "Maximum generations reached without success."
