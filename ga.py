from random import randint, random
from math import sqrt
from numpy.random import normal

class Solution:
    def __init__(self, limit=10000):
        self.f0 = random() * limit
        self.f1 = random() * limit
        self.f2 = random() * limit
        self.generation = 0
        self.score = None
        
    def print(self):
        s = self.f0 + self.f1 + self.f2 # f0 + f1 + f2 has to be close to 10,000
        delta = self.f1 - self.f2 > 0 # f1 > f2
        a = int(sqrt(self.f0))
        score = 'NA' if self.score is None else '{:.3f}'.format(self.score)
        print('score: {}, f0: {:.3f} f1: {:.3f} f2: {:.3f}, sum={:.3f}, f1 > f2? {}, f0 ~ {}**2 = {}, gen: {}'.format(score,
                                                                 self.f0,
                                                                 self.f1,
                                                                 self.f2,
                                                                 s,
                                                                 delta,
                                                                 a, 
                                                                 (a**2),
                                                                 self.generation))
        
    def evaluate(self):
        s = self.f0 + self.f1 + self.f2 # f0 + f1 + f2 has to be close to 10,000
        delta = self.f1 - self.f2 # f1 > f2
        delta_square = self.f0 - int(sqrt(self.f0))**2
        
        score = - abs(10000 - s) * 10  # has to be close to 0
        score += 1000 if delta > 0 else 0  # bonus if f1 > f2
        score += - delta_square / 1000  # has to be close to 0
        
        self.score = score
    
    def clone_and_mutate(self, generation):
        new_solution = Solution()
        new_solution.f0 = self.f0
        new_solution.f1 = self.f1
        new_solution.f2 = self.f2
        
        random_index = randint(0,2)
        if random_index == 0:
            new_solution.f0 = normal(new_solution.f0, new_solution.f0 * 0.2)
        elif random_index == 1:
            new_solution.f1 = random()*10000
        else:
            new_solution.f2 += max(0, random() * 1000 - 500)
        
        new_solution.generation = generation
        
        return new_solution
            
    def cross(self, another_solution, generation):
        new_solution = Solution()
        new_solution.f0 = self.f0              # f0 from first parent
        new_solution.f1 = another_solution.f1  # f1 and f2 from second parent
        new_solution.f2 = another_solution.f2
        
        new_solution.generation = generation
        
        return new_solution
    
class Population:
    def __init__(self, n_solutions, n_keep_best, limit=10000):
        self.n_solutions = n_solutions
        self.n_keep_best = n_keep_best
        
        self.solutions = [Solution(limit=limit) for i in range(self.n_solutions)]
        self.generations = 0
        
    def iterate(self):
        self.generations += 1
        
        # EVALUTATE
        for solution in self.solutions:
            solution.evaluate()
            
        # KEEP BEST
        self.solutions.sort(key=lambda x: x.score, reverse=True)
        self.solutions = self.solutions[:self.n_keep_best]

        # print new best one if any
        if self.solutions[0].generation == self.generations-1:
            self.solutions[0].print()
        
        # REPRODUCTION
        # one clone of each best
        self.solutions.extend([solution.clone_and_mutate(self.generations) for solution in self.solutions])
        # crossing
        while len(self.solutions) < self.n_solutions:
            first_parent_index = randint(0, self.n_keep_best-1)
            second_parent_index = randint(0, self.n_keep_best-1)
            while first_parent_index == second_parent_index:
                second_parent_index = randint(0, self.n_keep_best-1)
                
            self.solutions.append(
                self.solutions[first_parent_index].cross(
                    self.solutions[second_parent_index], self.generations)
            )
        
    def evolution(self, max_generation):
        generation = 0
        while generation < max_generation:
            generation += 1
            self.iterate()
        