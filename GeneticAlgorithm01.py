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
        division = random.randint(0, self.gene_size-1)
        #division = self.gene_size / 2
        return DNA(self.gene_size, initial_genes=self.genes[0:division] + dna_b.genes[division:])
    
    
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
        self.target = target
        self.population = []
        for i in xrange(population_size):
            self.population.append(DNA(len(target)))
    def new_generation(self):
        pool = []
        if self.best_fitted().fitness == 100:
            return True
        for pop in self.population:
            for i in xrange(pop.calculate_fitness(self.target)):
                pool.append(pop)
        population = []


        if len(pool) == 0:
            self = Population(self.population_size, self.target)
            return False
        
        for i in xrange(self.population_size):
            pop_a = random.choice(pool)
            pop_b = random.choice(pool)
            
            pop_c = pop_a.crossover(pop_b)
            pop_c.mutate(0.01)
            
            population.append(pop_c)
        self.population = population
        return False

    def best_fitted(self):
        best = None
        best_fit = 0
        for pop in self.population:
            fit = pop.calculate_fitness(self.target)
            if fit > best_fit:
                best_fit = fit
                best = pop
        return pop

population = Population(150, "Once upon a time.")

while True:
    for pop in population.population:
        print ("Phrase: " + str(pop.genes))
        print ("Fitness: " + str(pop.calculate_fitness(population.target)))
    if (population.new_generation() == True):
        print("DONE.")
        print(population.best_fitted().genes)
        break