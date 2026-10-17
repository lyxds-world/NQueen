import random

N = 4
MAX_PAIRS = N * (N - 1) // 2      # total pairs of queens = 6
CUT = 2                           # one-point crossover after 2nd bit
SEED = 29                         # fixed seed so the output is the same every time


def conflicts(state):
    """Count how many pairs of queens attack each other."""
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            same_row = state[i] == state[j]
            same_diag = abs(state[i] - state[j]) == abs(i - j)
            if same_row or same_diag:
                count += 1
    return count


def fitness(state):
    """Higher is better: pairs that are NOT attacking."""
    return MAX_PAIRS - conflicts(state)


def roulette_pick(population, probs):
    """Spin the wheel once and return the chosen parent."""
    r = random.random()
    cumulative = 0
    for i in range(len(population)):
        cumulative += probs[i]
        if r <= cumulative:
            return i, r
    return len(population) - 1, r


def crossover(p1, p2):
    """One-point crossover after the 2nd bit."""
    child1 = p1[:CUT] + p2[CUT:]
    child2 = p2[:CUT] + p1[CUT:]
    return child1, child2


def show_population(title, population):
    print(title)
    print("-" * 52)
    print(f"{'State':<10}{'Queens':<16}{'Conflicts':<12}{'Fitness'}")
    for i, s in enumerate(population, start=1):
        print(f"State-{i:<4}{str(s):<16}{conflicts(s):<12}{fitness(s)}")
    print()


random.seed(SEED)

population = [
    [2, 4, 3, 1],   # State-1
    [1, 2, 3, 4],   # State-2
    [2, 1, 3, 2],   # State-3
    [4, 3, 1, 1],   # State-4
]

show_population("Generation 0 (Initial Population)", population)

for gen in range(1, 3):                       # only 2 generations
    fits = [fitness(s) for s in population]
    total = sum(fits)
    probs = [f / total for f in fits]

    print(f"===== Making Generation {gen} =====")
    print("Fitness values   :", fits, " Total =", total)
    print("Probabilities    :", [round(p, 2) for p in probs])
    cum = 0
    cum_list = []
    for p in probs:
        cum += p
        cum_list.append(round(cum, 2))
    print("Cumulative       :", cum_list)
    print()

    new_population = []
    for pair in range(1, 3):                  # 2 pairs -> 4 children
        i1, r1 = roulette_pick(population, probs)
        i2, r2 = roulette_pick(population, probs)
        p1, p2 = population[i1], population[i2]
        c1, c2 = crossover(p1, p2)

        print(f"Pair {pair}:")
        print(f"  Random number 1 = {r1:.2f} -> Parent = State-{i1 + 1} {p1}")
        print(f"  Random number 2 = {r2:.2f} -> Parent = State-{i2 + 1} {p2}")
        print(f"  Crossover after bit {CUT}:")
        print(f"    Child 1 = {p1[:CUT]} + {p2[CUT:]} = {c1}")
        print(f"    Child 2 = {p2[:CUT]} + {p1[CUT:]} = {c2}")
        print()
        new_population += [c1, c2]

    population = new_population
    show_population(f"Generation {gen} (after crossover)", population)

    if any(conflicts(s) == 0 for s in population):
        print("A solution (0 conflicts) was found in this generation!\n")
