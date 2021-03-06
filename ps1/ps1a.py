###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
import re


def load_cows(filename='ps1_cow_data.txt'):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    file = open(filename)
    arr = re.split('[,\n]', file.read())
    file.close()

    cows = {}
    for i in range(0, len(arr), 2):
        cow_name = arr[i]
        cow_weight = arr[i + 1]
        cows[cow_name] = int(cow_weight)

    return cows


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    trips = []
    filtered_cows = filter(lambda name: cows[name] <= limit, cows)
    new_cows = sorted(filtered_cows, key=cows.get, reverse=True)

    def greedy_iter():
        current_trip = []
        avail = limit

        for name in new_cows:
            cow_weight = cows[name]
            if cow_weight <= avail:
                current_trip.append(name)
                avail -= cow_weight
            elif avail == 0:
                break

        for name in current_trip:
            new_cows.remove(name)

        trips.append(current_trip[:])

        if len(new_cows) > 0:
            greedy_iter()

    greedy_iter()
    return trips


# Problem 3d
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    partitions = get_partitions(cows)
    best_partition = None

    for trips in partitions:
        for trip in trips:
            can_accommodate = True
            avail = limit
            for name in trip:
                cow_weight = cows[name]

                if cow_weight > avail:
                    can_accommodate = False
                    break
                else:
                    avail -= cow_weight

            if can_accommodate is False:
                break

        if can_accommodate is True:
            best_partition = trips
            break

    return best_partition


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows()

    start = time.time()
    greedy_cow_transport(cows)
    end = time.time()

    print('greedy_cow_transport:', end - start)

    start = time.time()
    brute_force_cow_transport(cows)
    end = time.time()

    print('brute_force_cow_transport:', end - start)
