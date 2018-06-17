#!/usr/bin/env python
 
import sys, random, argparse, numpy as np
 
def main():
    parser = argparse.ArgumentParser(description='Genetic Algorithms')
    parser.add_argument('-question', type=int, help='No. of the question')
    parser.add_argument('-bits_x', type=str, help='Bit string X')
    parser.add_argument('-bits_y', type=str, help='Bit string Y')
    parser.add_argument('-population', type=str, help='Number of population')
    parser.add_argument('-k', type=int, help='Population size')
    parser.add_argument('-chi', type=float, help='chi')
    parser.add_argument('-repetitions', type=int, help='No of repetitions')
    parser.add_argument('-lambda', type=int, help='Population size')
    parser.add_argument('-n', type=int, help='bit string')
    args = parser.parse_args()
 
    def mutation(bitx):
        num = 0
        y = 0
        for x1 in bitx:
            if num == 0:
                num = 1
                ran = random.random()
                if ran < args.chi / len(bitx):
                    y = '1' if x1 == '0' else '0'
                else:
                    y = x1
            else:
                ran = random.random()
                if ran < args.chi / len(bitx):
                    y = y + '1' if x1 == '0' else y + '0'
                else:
                    y = y + x1
        return y
 
    def crossover(bitx, bity):
            num = 0
            for x1, y1 in zip(bitx, bity):
                if num == 0:
                    num = 1
                    if x1 == y1:
                        z = x1
                    else:
                        ran = random.random()
                        if ran < 0.5:
                            z = x1
                        else:
                            z = y1
                else:
                    if x1 == y1:
                        z = z + x1
                    else:
                        ran = random.random()
                        if ran < 0.5:
                            z = z + x1
                        else:
                            z = z + y1
            return z
 
    def onemax(incoming):
        total = 0
        for i in range(len(incoming)):
            total = total + int(incoming[i])
        return total
 
    def lam():
        for x in range(len(sys.argv)):
            if sys.argv[x] == '-lambda':
                return sys.argv[x+1]
 
    def tournament(pp, fit):
        index = np.random.randint(0, len(pp), args.k)
        max_value = max(fit[index])
        for i in range(len(fit)):
            if fit[i] == max_value:
                return pp[i]
#FIRST
    if args.question == 1:
        for x in range(0, args.repetitions):
            print mutation(args.bits_x)
#SECOND
    elif args.question == 2:
        for x in range(0, args.repetitions):
            print crossover(args.bits_x, args.bits_y)
 
#THIRD
    elif args.question == 3:
        print onemax(args.bits_x)
 
#FORTH
    elif args.question == 4:
        for rep in range(0, args.repetitions):
            pop = np.array(args.population.split(' '))
            fitness = np.array([onemax(x) for x in pop])
            print tournament(pop, fitness)
 
#FIFTH
    elif args.question == 5:
        for rep in range(0, args.repetitions):
            population = np.array([])
            fitness = np.array([])
            lm = lam()
            for x in range(0,int(lm)):
                num = random.randint(0, 2 ** args.n - 1)
                bin_num = bin(num)[2:].zfill(args.n)
                population = np.append(population, bin_num)
                fitness = np.append(fitness, [onemax(bin_num)])
 
            generation = 0
            while True:
                generation = generation + 1
                max_index = np.argmax(fitness)
                fbest = fitness[max_index]
                xbest = population[max_index]
                if fbest == args.n:
                    break
                if generation == 1000:
                    break
                newpop = np.array([])
                newfitness = np.array([])
                for x in range(0, int(lm)):
                    xparent = tournament(population,fitness)
                    yparent = tournament(population,fitness)
                    xnew = crossover(mutation(xparent),mutation(yparent))
                    newpop = np.append(newpop, xnew)
                    newfitness = np.append(newfitness,onemax(xnew))
                population = newpop
                fitness = newfitness
            print str(args.n) +'\t'+ str(args.chi) +'\t'+ str(lm) +'\t'+ str(args.k) +'\t'+ str(generation) +'\t'+ str(fbest) +'\t'+ str(xbest)
if __name__ == '__main__':
  main()
