import string
import random

def get_random_letter():
    return random.choice(string.letters + ' .')

class DNA:
    def __init__(self, gene_size, initial_genes=""):
        if initial_genes == "":
            self.genes = "".join(get_random_letter() for _ in xrange(gene_size))
        else:
            self.genes = initial_genes
        self.gene_size = gene_size
        self.fitness = 0
    def mutate(self, mutation_number):
        genes = list(self.genes) 
        for i in xrange(self.gene_size):
            random_num = random.random()  
            if mutation_number > random_num:
                genes[i] = get_random_letter()
            else:
                genes[i] = self.genes[i]
        self.genes = "".join(genes)
    def crossover(self, dna_b):
        division_a = random.randint(0, self.gene_size - 1)
        #division_b = random.randint(self.gene_size / 2, self.gene_size -1)
        #division = self.gene_size / 2
        return DNA(self.gene_size, initial_genes=self.genes[0:division_a] + dna_b.genes[division_a:])
    
    
    def calculate_fitness(self, target):
        score = 0.0
        for i, c in enumerate(self.genes):
            if c == target[i]:
                score += 1
        self.fitness = int((score / self.gene_size) * 100)
        return self.fitness

class Population:
    def __init__(self, population_size, target):
        self.population_size = population_size
        self.population_a_size = population_size / 2
        self.population_b_size = population_size - self.population_a_size
        self.target = target
        self.population_a = []
        self.population_b = []
        for i in xrange(self.population_a_size):
            self.population_a.append(DNA(len(target)))
        for i in xrange(self.population_b_size):
            self.population_b.append(DNA(len(target)))

    def new_population(self, population_size):
        pop = []
        for i in xrange(population_size):
            pop.append(DNA(len(target)))
        return pop

    def new_generation(self):
        pool_a = []
        pool_b = []
        if self.best_fitted()["a"].fitness == 100 and self.best_fitted()["b"].fitness == 100:
            return True
        for pop in self.population_a:
            for i in xrange(pop.calculate_fitness(self.target)):
                pool_a.append(pop)
        for pop in self.population_b:
            for i in xrange(pop.calculate_fitness(self.target)):
                pool_b.append(pop)

        if len(pool_a) == 0:
            self.population_a = new_population(self.population_a_size)
            return False
        if len(pool_b) == 0:
            self.population_b = new_population(self.population_b_size)
        
        population_a = []
        population_b = []

        for i in xrange(self.population_size):
            pop_a1 = random.choice(pool_a)
            pop_a2 = random.choice(pool_a)

            pop_b1 = random.choice(pool_b)
            pop_b2 = random.choice(pool_b)

            pop_c1 = pop_a1.crossover(pop_a2)
            pop_c2 = pop_b1.crossover(pop_b2)

            pop_c1.mutate(0.01)
            pop_c2.mutate(0.01)


            population_a.append(pop_c1)
            population_b.append(pop_c2)

        self.population_a = population_a
        self.population_b = population_b
        return False

    def best_fitted(self):
        best_a = None
        best_a_fit = 0

        best_b = None
        best_b_fit = 0

        for pop in self.population_a:
            fit = pop.calculate_fitness(self.target)
            if fit > best_a_fit:
                best_a_fit = fit
                best_a = pop
        for pop in self.population_b:
            fit = pop.calculate_fitness(self.target)
            if fit > best_b_fit:
                best_b_fit = fit
                best_b = pop
        return {"a": best_a, "b": best_b}

population = Population(1000, "There was a child named Morty that had a grandpa called Rick.")

while True:
    print ("Phrase: " + str(population.best_fitted()["a"].genes + population.best_fitted()["b"].genes))
    print ("FitnessA: " + str(population.best_fitted()["a"].fitness))
    print ("FitnessB: " + str(population.best_fitted()["b"].fitness))

    if (population.new_generation() == True):
        print("DONE.")
        print(population.best_fitted()["a"].genes + population.best_fitted()["b"].genes)
        break