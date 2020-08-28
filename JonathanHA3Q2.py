# PConc A3Q2
# ICS3UI-01, Ms Harris
# Jonathan H
# Began: Nov 7, 2019
# Finished : Nov 11, 2019

'''
Take your dataset from question 1 and sort it using each of the sorts from class.
Record the length of time each sort took and display that to the screen
comparing the types of sort. Create an IPO chart and trace table for this
question. Hint: time in milliseconds, before you run the search and after.
'''

# I am going to be importing classes from JonathanHA3Q1 for convenience
# IMPORTANT: JonathanHA3Q1 must be in the same directory as this file
import time
from JonathanHA3Q1 import Country, DataLoader

# function to return the current time in milliseconds since the unix epoch
# this will be used to track time elapsed during sorts
def get_time():
    return time.time() * 1000

# each of the sorting functions below returns a tuple, first element is the sorted array, second is the time taken

# recursive bubble sort
def bubble_sort(arr):
    def recursive(array):
        # if the array is 1 element long then return
        if (len(array) < 2):
            return array
        else:
            # if no sorts happened on a run, then bubble sort is complete
            sorted = False
            for i in range(1, len(array)):
                current = array[i]
                prev = array[i - 1]
                #if right < left element
                if (current < prev):
                    # swap
                    sorted = True
                    array[i] = prev
                    array[i - 1] = current
            if (sorted):
                return recursive(array)
            else:
                return array
    # run bubble sort
    copy = arr.copy()
    start = get_time()
    recursive(copy)
    end = get_time() - start
    return (copy, end)

# optimized iterative merge sort
def merge_sort(arr):
    # merges two sorted arrays into one
    def merge(a1, a2):
        i, j = 0, 0
        merged = []
        while len(merged) < len(a1) + len(a2):
            # add smaller element of a1[i] and a2[j] into merged
            # if the end of either array is reached, then append the remaining elements from the other array into merged
            if a1[i] <= a2[j]:
                merged.append(a1[i])
                if i < len(a1) - 1:
                    i += 1
                else:
                    merged += a2[j:]
                    break
            else:
                merged.append(a2[j])
                if j < len(a2) - 1:
                    j += 1
                else:
                    merged += a1[i:]
                    break
        return merged

    def sort(array):
        # merge sort
        # breaks input array into arrays of size 1, by defn any size 1 array is already sorted
        arrays = [[x] for x in array]
        if len(arrays) <= 1:
            return array
        else:
            # repeat until all arrays are merged
            while len(arrays) > 1:
                # if there are an odd number of arrays, skip the last array
                max = len(arrays)
                # boolean to remember if the array is odd in length
                should_add = False
                if len(arrays) % 2 != 0:
                    max = len(arrays) - 1
                    should_add = True

                # iteratively merge
                new_arrays = []
                for i in range(1, max, 2):
                    new_arrays.append(merge(arrays[i], arrays[i-1]))
                if should_add:
                    new_arrays.append(arrays[len(arrays) - 1])
                arrays = new_arrays
            return arrays[0]

    # call merge sort
    copy = arr.copy()
    start = get_time()
    a = sort(copy)
    end = get_time() - start
    return(a, end)

# recursive quicksort
def quick_sort(array):
    # quicksort takes a pivot element
    # all elements less than pivot are put on the left, all elements greater than pivot are put on the right
    # this is then called recursively on both the left and right sides
    # quicksort requires all functions below to be impure

    # impure function to swap
    def swap(a, i, j):
        temp = a[i]
        a[i] = a[j]
        a[j] = temp

    # partition finds where pivot should go
    # sorts into halves, then returns pivot index
    def partition(a, high, low):
        pivot = a[high]
        # everything left of i is less than pivot
        i = low
        # j scans through the array
        for j in range(low, high):
            # if the element at j is <= pivot, then swap it with i
            if a[j] < pivot:
                swap(a, i, j)
                i += 1
        # swap pivot with i+1 so that pivot is now sandwiched between lower and higher halves
        swap(a, i, high)
        # return the pivot index
        return (i)

    # function to recursively quicksort
    def recursive(a, high, low):
        if low < high:
            # partition the array into two halves
            pivot_index = partition(a, high, low)
            #print("{} {} {}".format(a[:pivot_index], a[pivot_index], a[pivot_index + 1:]))

            # sort everything left of pivot index, sort everything right of pivot index
            recursive(a, pivot_index - 1, low)
            recursive(a, high, pivot_index + 1)

    # call quicksort
    # note quick_sort itself is a pure function
    copy = array.copy()
    start = get_time()
    recursive(copy, len(copy) - 1, 0)
    end = get_time() - start
    return (copy, end)

def selection_sort(array):
    # impure swap function
    def swap(a, i, j):
        temp = a[i]
        a[i] = a[j]
        a[j] = temp

    # recursive selection sort
    def recursive(arr, marker):
        # everything left of marker is sorted
        # loop through everything right of marker and find the smallest
        # once the end is reached and the smallest is found, swap smallest with marker
        # finishes when marker is the end
        if marker < len(arr):
            # smallest element found between marker and the end
            minimum = marker
            # loop from marker to the end of the array
            for i in range(marker, len(arr)):
                if arr[i] < arr[minimum]:
                    minimum = i
            # swap elements at marker and minimum
            swap(arr, minimum, marker)
            recursive(arr, marker + 1)

    # call selection sort
    copy = array.copy()
    start = get_time()
    recursive(copy, 0)
    end = get_time() - start
    return (copy, end)

def insertion_sort(array):
    # impure swap function
    def swap(a, i, j):
        temp = a[i]
        a[i] = a[j]
        a[j] = temp

    # keep swapping an element at index n to the left until it reaches its correct spot
    def swap_down(a, n):
        # i starts as the item left of n
        i = n - 1
        while i >= 0:
            # if the item is less than the item on the left, keep swapping
            if a[i + 1] < a[i]:
                swap(a, i, i + 1)
                # decrement both
                i -= 1
            else:
                break

    # iterative insertion sort
    def sort(arr):
        for i in range(len(arr)):
            swap_down(arr, i)

    # run insertion sort
    copy = array.copy()
    start = get_time()
    sort(copy)
    end = get_time() - start
    return (copy, end)

# sorting country data
# load in country data using DataLoader
countries = DataLoader.load_data_as_obj()

# reverse keymapping of pop to name
pop_to_name = {}
pop = []
for country in countries:
    c = countries[country]
    if 2016 not in c.yearly_populations:
        continue
    pop_to_name[c.pop_in(2016)] = c.name
    pop.append(c.pop_in(2016))

# handy function to get top X most populous
def get_top(arr, x):
    # use the global variables
    global pop_to_name

    names = []
    i = len(arr) - 1
    while i >= (len(arr) - 1) - x:
        names.append(pop_to_name[arr[i]])
        i -= 1
    return names

# some info text
print("This program sorts countries by their population in 2016.")
print("To keep the program output readable, only the 5 most populous countries will be printed, however over 200 countries are actually being sorted by the algorithms.")

# bubble sort
print("\nBubble Sort\n=============")
result = bubble_sort(pop)
print("Time elapsed: {}".format(result[1]))
print("Top 5 results from sort: {}".format(get_top(result[0], 5)))

# merge sort
print("\nMerge Sort\n=============")
result = merge_sort(pop)
print("Time elapsed: {}".format(result[1]))
print("Top 5 results from sort: {}".format(get_top(result[0], 5)))

# quick sort
print("\nQuick Sort\n=============")
result = quick_sort(pop)
print("Time elapsed: {}".format(result[1]))
print("Top 5 results from sort: {}".format(get_top(result[0], 5)))

# insertion sort
print("\nInsertion Sort\n=============")
result = insertion_sort(pop)
print("Time elapsed: {}".format(result[1]))
print("Top 5 results from sort: {}".format(get_top(result[0], 5)))

# selection sort
print("\nSelection Sort\n=============")
result = selection_sort(pop)
print("Time elapsed: {}".format(result[1]))
print("Top 5 results from sort: {}".format(get_top(result[0], 5)))
