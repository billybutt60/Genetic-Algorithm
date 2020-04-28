import numpy as np
import cv2
import random
import copy

POP_SIZE = 100
GENERATIONS = 100

def FitnessFunciton(population, finalState):
    fitness = np.empty(population.shape[0])
    for i in range(population.shape[0]):
        fitness[i] = np.sum(np.absolute(finalState - population[i]))
    return fitness

def Sort(population, fitness):
    global POP_SIZE
    for i in range(POP_SIZE-1):
        for j in range(POP_SIZE-2):
            if(fitness[j+1] < fitness[j]):
                temp1 = copy.deepcopy(fitness[j+1])
                temp2 = copy.deepcopy(fitness[j])

                fitness[j+1] = temp2
                fitness[j] = temp1

                temp11 = copy.deepcopy(population[j+1])
                temp22 = copy.deepcopy(population[j])
                population[j+1] = temp22
                population[j] = temp11

def replace(person1, person2):

    pivot = random.randrange(len(person1))
    for i in range(pivot):
        person1[i], person2[i] = person2[i], person1[i]


def Crossover(population, newPop):
    global POP_SIZE
    for i in range(int(POP_SIZE*25/100), POP_SIZE-1):
        r1 = random.randrange(int(POP_SIZE*25/100))
        r2 = random.randrange(int(POP_SIZE*25/100))
        first = copy.deepcopy(population[r1])
        second = copy.deepcopy(population[r2])

        replace(first, second)
        newPop[i] = first
        i += 1
        newPop[i] = second


def Mutation(population):
    global POP_SIZE
    for i in range(POP_SIZE-1):
        if(random.randrange(1000)%4 == 0):
            randindex = random.randrange(population.shape[1])
            population[i][randindex] = random.randrange(255)


def main():
    global POP_SIZE
    img = cv2.imread("face.bmp", 0)         #Final Image

    img = cv2.resize(img, (50, 50));
    npImg1 = np.array(img)
    npImg = npImg1.flatten()

    #Creating population
    population = np.array([np.random.randint(0,255,len(npImg)) for i in range(POP_SIZE)])        #Random population of size 1
    print(population.shape)

    #Calculating Fitness Value for population
    fitness = FitnessFunciton(population, npImg)
    fitness = fitness.astype('int32')

    result = 0
    generations = 0
    output = 1000000000
    while(result == 0):
        #Sorting Population on Fitness
        Sort(population, fitness)

        newPop = np.empty(population.shape)
        newPop[:] = population
        if(fitness[0]<output):

            output = fitness[0]
            print("Generation # "+ str(generations) + ", Value = " + str(fitness[0]))

        if(generations%500 == 0):
            image = population[0].reshape(npImg1.shape)
            image = image.astype(np.uint8)
            cv2.imwrite("hey"+str(generations) + ".bmp", image)
        if(fitness[0] == 0):

            print("Result found")
            break

        Crossover(population,newPop)
        Mutation(newPop)

        population = newPop

        fitness = FitnessFunciton(population, npImg)
        fitness = fitness.astype('int32')
        generations += 1















if __name__ == '__main__':
    main()