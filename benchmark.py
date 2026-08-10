from backend.algorithms.search_sort import (
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def make_records(size):
    records = []

    for i in range(size):
        records.append(
            {
                "title": f"Task {size - i}",
                "priority": ["low", "medium", "high"][i % 3],
                "due_date": "next friday",
            }
        )

    return records


sizes = [10, 500, 3000]


for size in sizes:
    print()
    print("=" * 50)
    print(f"DATA SIZE: {size}")
    print("=" * 50)

    # -----------------------------
    # Insertion Sort
    # -----------------------------
    records = make_records(size)

    insertion_count = insertion_sort_count(
        records,
        "title"
    )

    print(
        f"Insertion Sort comparisons: "
        f"{insertion_count}"
    )

    # -----------------------------
    # Binary Search
    # -----------------------------
    binary_records = make_records(size)

    insertion_sort_count(
        binary_records,
        "title"
    )

    target_title = f"Task {size // 2}"

    binary_result = binary_search_count(
        binary_records,
        target_title,
        "title"
    )

    print(
        f"Binary Search target: "
        f"{target_title}"
    )

    print(
        f"Binary Search index: "
        f"{binary_result['index']}"
    )

    print(
        f"Binary Search comparisons: "
        f"{binary_result['comparison_count']}"
    )

    # -----------------------------
    # Linear Search
    # -----------------------------
    linear_records = make_records(size)

    linear_result = linear_search_count(
        linear_records,
        target_title,
        "title"
    )

    print(
        f"Linear Search index: "
        f"{linear_result['index']}"
    )

    print(
        f"Linear Search comparisons: "
        f"{linear_result['comparison_count']}"
    )