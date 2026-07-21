# To-Do List Application

tasks = []

def add_task():
    task = input("Enter task: ")
    tasks.append({"task": task, "status": "Pending"})
    print("Task added successfully!\n")

def view_tasks():
    if not tasks:
        print("No tasks available.\n")
        return

    print("\n===== TO-DO LIST =====")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['task']} [{task['status']}]")
    print()

def update_task():
    view_tasks()

    if not tasks:
        return

    try:
        index = int(input("Enter task number to update: ")) - 1

        if 0 <= index < len(tasks):
            new_task = input("Enter new task name: ")
            tasks[index]["task"] = new_task
            print("Task updated successfully!\n")
        else:
            print("Invalid task number.\n")

    except ValueError:
        print("Please enter a valid number.\n")

def mark_completed():
    view_tasks()

    if not tasks:
        return

    try:
        index = int(input("Enter task number completed: ")) - 1

        if 0 <= index < len(tasks):
            tasks[index]["status"] = "Completed"
            print("Task marked as completed!\n")
        else:
            print("Invalid task number.\n")

    except ValueError:
        print("Please enter a valid number.\n")

def delete_task():
    view_tasks()

    if not tasks:
        return

    try:
        index = int(input("Enter task number to delete: ")) - 1

        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(f"Deleted: {removed['task']}\n")
        else:
            print("Invalid task number.\n")

    except ValueError:
        print("Please enter a valid number.\n")

while True:
    print("===== TO-DO LIST MENU =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Mark Task Completed")
    print("5. Delete Task")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        update_task()

    elif choice == "4":
        mark_completed()

    elif choice == "5":
        delete_task()

    elif choice == "6":
        print("Thank you for using To-Do List!")
        break

    else:
        print("Invalid choice. Try again.\n")