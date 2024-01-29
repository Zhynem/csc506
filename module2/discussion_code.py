# CSC 506 Module 2 Discussion
# Michael Luker

from dataclasses import dataclass
from datetime import datetime
from typing import List
from icecream import ic


@dataclass
class Task:
    name: str
    date: datetime.date
    tags: List[str]


def sequential_tag_search(tasks: List[Task], tag: str) -> List[Task]:
    results = []
    # Simple iteration over each task object to check if it has the tag or not
    for task in tasks:
        if tag in task.tags:
            results.append(task)
    print(f"Done searching {len(tasks)} tasks")
    return results


total_bsr_counter = 0


def binary_search_range(
    tasks: List[Task],
    min_date: datetime.date,
    max_date: datetime.date,
    counter: int = 0,
) -> List[Task]:
    # Base case: one task to check
    if len(tasks) == 1:
        # Curious, so keeping track of how many times we check a distinct task for being in the range
        global total_bsr_counter
        total_bsr_counter += 1
        if tasks[0].date >= min_date and tasks[0].date <= max_date:
            return tasks
        else:
            return []

    # Otherwise split the list in half to recurse
    mid = len(tasks) // 2
    mid_date = tasks[mid].date
    # If the mid point is below the min date, then we only need to search the right half
    if mid_date < min_date:
        print(
            f"Searching right half,   recursion depth: {counter} | list length was: {len(tasks)}"
        )
        return binary_search_range(tasks[mid:], min_date, max_date, counter + 1)
    # Similarly if it's above the max date, we only need to search the left half
    elif mid_date > max_date:
        print(
            f"Searching left half,   recursion depth: {counter} | list length was: {len(tasks)}"
        )
        return binary_search_range(tasks[:mid], min_date, max_date, counter + 1)
    # But if it spans the gap, we need to search both halves
    else:
        print(
            f"Searching both halves, recursion depth: {counter} | list length was: {len(tasks)}"
        )
        return binary_search_range(
            tasks[:mid], min_date, max_date, counter + 1
        ) + binary_search_range(tasks[mid:], min_date, max_date, counter + 1)


# Example list of tasks in the system
task_list = [
    Task(
        name="Deploy new server updates",
        date=datetime(2024, 1, 30),
        tags=["development", "urgent"],
    ),
    Task(
        name="Database backup and maintenance",
        date=datetime(2024, 2, 1),
        tags=["database", "maintenance"],
    ),
    Task(
        name="API development review",
        date=datetime(2024, 2, 3),
        tags=["development", "review"],
    ),
    Task(
        name="Team sprint planning",
        date=datetime(2024, 1, 27),
        tags=["team", "planning"],
    ),
    Task(
        name="Cybersecurity training session",
        date=datetime(2024, 2, 14),
        tags=["security", "training"],
    ),
    Task(
        name="Code refactoring for module X",
        date=datetime(2024, 1, 25),
        tags=["coding", "refactoring"],
    ),
    Task(
        name="User interface design meeting",
        date=datetime(2024, 1, 31),
        tags=["design", "meeting"],
    ),
    Task(
        name="Cloud infrastructure audit",
        date=datetime(2024, 2, 5),
        tags=["cloud", "audit"],
    ),
    Task(
        name="Optimize database queries",
        date=datetime(2024, 1, 29),
        tags=["database", "optimization"],
    ),
    Task(
        name="Front-end framework upgrade",
        date=datetime(2024, 2, 2),
        tags=["development", "upgrade"],
    ),
    Task(
        name="Weekly team sync-up",
        date=datetime(2024, 1, 28),
        tags=["team", "meetings"],
    ),
    Task(
        name="Implement new authentication protocol",
        date=datetime(2024, 2, 6),
        tags=["security", "development"],
    ),
    Task(
        name="Prepare cloud migration strategy",
        date=datetime(2024, 1, 26),
        tags=["cloud", "planning"],
    ),
    Task(
        name="Refine machine learning model",
        date=datetime(2024, 2, 4),
        tags=["AI", "development"],
    ),
    Task(
        name="UX/UI design brainstorming",
        date=datetime(2024, 1, 31),
        tags=["design", "creative"],
    ),
    Task(
        name="Automate deployment process",
        date=datetime(2024, 2, 7),
        tags=["automation", "maintenance"],
    ),
]

# Sort the tasks by their date field
task_list.sort(key=lambda x: x.date)

# Get a list of tasks between January 25 and January 30
search_tasks = binary_search_range(
    task_list, datetime(2024, 1, 25), datetime(2024, 1, 30)
)
print(f"Total binary search checks done: {total_bsr_counter}")
print("Tasks between January 25 and January 30:")
for task in search_tasks:
    ic(task)
print()

search_tasks = sequential_tag_search(task_list, "security")
print('Tasks containing the "security" tag:')
for task in search_tasks:
    ic(task)
