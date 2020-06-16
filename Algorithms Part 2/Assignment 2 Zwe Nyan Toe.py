import csv
from data_structures.unsorted_priority_queue import UnsortedPriorityQueue
from data_structures.unsorted_table_map import UnsortedTableMap


# ['id', 'name', 'host_id', 'host_name', 'neighbourhood_group', 'neighbourhood', 'latitude', 'longitude', 'room_type',
# 'price', 'minimum_nights', 'number_of_reviews', 'last_review', 'reviews_per_month', 'calculated_host_listings_count',
# 'availability_365']

# Loading data into a list of lists, since csv file contains all strings only, converted ints and floats to their
# correct types before appending.


# This is the reading file function, which has been slightly adapted from Assignment 1 since the second assignment will
# use the entire dataset.
def read_file():
    with open('AB_NYC_2019.csv') as csv_file:
        whole_file = csv.reader(csv_file, delimiter=",")
        data = []
        for row in whole_file:
            newRow = []
            for each in row:
                if each.isdigit():
                    newRow.append(int(each))
                else:
                    try:
                        newRow.append(float(each))
                    except ValueError:
                        newRow.append(each)
            data.append(newRow)

    return data


# Question 1 : What is the cheapest listing you can get given a minimum number of days?
# This is implemented using the unsorted priority queue from Chapter 9.
# The data structures used in this problem include a priority queue, list, list of lists and tuples. Additionally, the
# priority queue is used to create a sorted list of the listings with the lowest costs.

def best_price_given_stay(data):
    print(
        "Question 1 : This function will give you the listing with the lowest cost given a minimum length of stay.\n")

    # Ask the user for the minimum length of stay.

    while True:
        try:
            min_days = int(input("Please enter the minimum number of days you will stay. \n>>>"))
            break
        except ValueError:  # Validating that the input is a number.
            print("Please enter a valid number.")

    temp_arr = []  # Declaring a temporary array to put unsorted listings higher than length of stay.

    for element in data:
        try:
            if min_days < element[10]:
                temp_arr.append([element[9], element[0]])  # Adding a list of prices and ID.
        except TypeError:
            pass

    unsorted_pri_que = UnsortedPriorityQueue()  # Unsorted Priority Queue instance declaration.
    for each in temp_arr:
        unsorted_pri_que.add(each[0], each[1])  # Adding items into the priority queue from the array.

    sorted_temp_arr = []  # Declaring a temporary array with sorted listings.

    # In this function, the cost functions as the priority. Therefore, remove_min will remove the item with the
    # lowest cost and add it to the lowest_cost list, giving us a sorted list of reviews.

    for i in range(len(temp_arr)):
        sorted_temp_arr.append(unsorted_pri_que.remove_min())

    lowest_cost = []  # Searching for the correct listing.

    # If the user specifies a price range that contains no listings, the program throws an IndexError and moves on to
    # Question 2.

    try:
        for element in data:
            if element[0] == sorted_temp_arr[-1][1]:
                lowest_cost = element

        print("\n"
              "The cheapest listing for you with your length of stay is at ID {} in {}, {}.".format(lowest_cost[0],
                                                                                                    lowest_cost[5],
                                                                                                    lowest_cost[4]))
    except IndexError:
        print("\nThere are no houses in your given price range.\n")


# Question 2 : What is the average cost in each neighborhood group?
# This solution uses UnsortedTableMap, lists, lists of lists, tuples and the mergesort algorithm to provide a sorted
# list of all the prices in the neighborhood.

def average_cost_neighborhood_group(data):
    print("\nQuestion 2 : What is the average cost in each neighborhood group? \n")

    # Declaration of an UnsortedTableMap instance. This will store a map with keys as the areas, and the values as a
    # list containing the neighborhood and price.

    map_of_location_groups = UnsortedTableMap()

    # Whilst very syntactically confusing, what this function is doing is such:
    # - It checks if the key is already in the Map. If not, it throws a KeyError and adds a new key. Otherwise, it
    #   appends a value to an existing key.
    # - In the value, the value itself has a key-value pair. The key of the inner key is the area, while the value is
    #   the price.

    for element in data:
        try:
            if element[5] not in map_of_location_groups[element[4]]:
                new_list = [element[5], element[9]]
                map_of_location_groups[element[4]].append(new_list)
            else:
                map_of_location_groups[element[4]][1] += element[9]
        except KeyError:
            new_list = [element[5], element[9]]
            map_of_location_groups[element[4]] = [new_list]

    map_of_location_groups.pop("neighbourhood_group")  # Removing the description instance.

    # Another Unsorted Table Map to display the prices. This time, there is no location and all the prices get combined.
    # The code is functionally identical to the creation of the previous Unsorted table map. However, the inner
    # key-value pair stores the count as a key and total as value for calculating the average later.

    prices = UnsortedTableMap()

    for item in map_of_location_groups.values():
        for i in item:
            try:
                if i[0] not in prices.keys():
                    prices[i[0]].append([1, i[1]])
                else:
                    prices[i[0]][0] += 1
                    prices[i[0]][1] += i[1]
            except KeyError:
                prices[i[0]] = [1, i[1]]

    prices_by_location = []

    # This is a list of key-value pairs of places and prices. This can be implemented with a dictionary, but arrays save
    # space and accessing is easier.

    for item in prices.items():
        prices_by_location.append([item[0], item[1][1] / item[1][0]])

    # merge sort performed to order data correctly.

    merge_sort(prices_by_location)

    while True:
        try:
            choice = int(input("Would you like to see all the prices or just the prices for a particular location?\n"
                               "\t1. Prices for just one location.\n"
                               "\t2. All the prices for every location.\n"
                               "\tAny other choice will display every price.\n"
                               ">>>"))
            break
        except ValueError:
            print("Please enter a proper number.")

    if choice == 1:
        print("Which location would you like?")
        count = 0
        for each in prices_by_location:
            count += 1
            print(("\t{}. {}".format(count, each[0])))
        while True:
            try:
                loc = int(input("\n>>>"))
                break
            except ValueError:
                print("\nPlease enter a proper number.")
        print("\nThe average price for {} is ${:.2f}.".format(prices_by_location[loc - 1][0],
                                                              prices_by_location[loc - 1][1]))
    else:
        for each in prices_by_location:
            print("{:20s} : ${:5.2f}".format(each[0], each[1]))

    return prices_by_location


# Creation of the merge sort algorithm used in Question 2.


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2

        # Dividing the array into two halves.

        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursive merge sort on each half.

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Merge sort checks left half to see if values are smaller than right half, then adjusts.

        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] <= right_half[j][1]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1


def main():
    data = read_file()
    # best_price_given_stay(data)
    prices_sorted = average_cost_neighborhood_group(data)
    print(prices_sorted)


main()
