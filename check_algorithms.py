from backend.algorithms.search_sort import (
    insertion_sort,
    binary_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


# 1. Empty list
records = []

insertion_sort(records, "value")

if records == []:
    print("PASS: insertion_sort empty list")
else:
    print("FAIL: insertion_sort empty list")


# 2. Single element
records = [{"value": 10}]

insertion_sort(records, "value")

if records == [{"value": 10}]:
    print("PASS: insertion_sort single element")
else:
    print("FAIL: insertion_sort single element")


# 3. Binary search first
records = [
    {"value": 10},
    {"value": 20},
    {"value": 30},
    {"value": 40},
    {"value": 50},
]

result = binary_search(records, 10, "value")

if result == 0:
    print("PASS: binary_search first index")
else:
    print("FAIL: binary_search first index")


# 4. Binary search last
result = binary_search(records, 50, "value")

if result == 4:
    print("PASS: binary_search last index")
else:
    print("FAIL: binary_search last index")


# 5. Binary search middle
result = binary_search(records, 30, "value")

if result == 2:
    print("PASS: binary_search middle index")
else:
    print("FAIL: binary_search middle index")


# 6. Binary search not found
result = binary_search(records, 99, "value")

if result == -1:
    print("PASS: binary_search not found")
else:
    print("FAIL: binary_search not found")


# 7. Insertion sort count
records = [
    {"value": 5},
    {"value": 2},
    {"value": 4},
    {"value": 1},
]

count = insertion_sort_count(records, "value")

expected = [
    {"value": 1},
    {"value": 2},
    {"value": 4},
    {"value": 5},
]

if records == expected:
    print("PASS: insertion_sort_count sorted result")
else:
    print("FAIL: insertion_sort_count sorted result")


if type(count) == int and count > 0:
    print("PASS: insertion_sort_count comparison count")
else:
    print("FAIL: insertion_sort_count comparison count")


# 8. Binary search count
records = [
    {"value": 10},
    {"value": 20},
    {"value": 30},
    {"value": 40},
    {"value": 50},
]

result = binary_search_count(records, 30, "value")

if (
    type(result) == dict
    and result["index"] == 2
    and type(result["comparison_count"]) == int
    and result["comparison_count"] > 0
):
    print("PASS: binary_search_count")
else:
    print("FAIL: binary_search_count")


# 9. Linear search count
result = linear_search_count(records, 99, "value")

if (
    type(result) == dict
    and result["index"] == -1
    and result["comparison_count"] == len(records)
):
    print("PASS: linear_search_count absent value")
else:
    print("FAIL: linear_search_count absent value")