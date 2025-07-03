import json
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

DATA_FILE = "todo_list.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
        
def display_tasks(tasks):
    if not tasks:
        print(Fore.YELLOW + "No tasks yet! Add some.")
        return
    print()
    for i, task in enumerate(tasks, 1):
        status = Fore.GREEN + "[Done]" if task["done"] else Fore.RED + "[To-do]"
        priority = f"Priority: {task['priority']}" if task["priority"] else "Priority: None"
        due = task["due_date"] if task["due_date"] else "No due date"
        print(f"{i}. {status} {task['description']} ({priority}, Due: {due})")
    print()

def add_task(tasks):
    desc = input("Enter task description: ").strip()
    if not desc:
        print(Fore.RED + "Description cannot be empty.")
        return
    priority = input("Enter priority (low/medium/high) or leave blank: ").strip().lower()
    if priority not in ("low", "medium", "high", ""):
        print(Fore.RED + "Invalid priority, set to None.")
        priority = None
    due_date = input("Enter due date (DD-MM-YYYY) or leave blank: ").strip()
    if due_date:
        try:
            datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            print(Fore.RED + "Invalid date format, due date cleared.")
            due_date = None
    else:
        due_date = None
        
    tasks.append({
        "description": desc,
        "done": False,
        "priority": priority if priority else None,
        "due_date": due_date,
    })
    print(Fore.GREEN + "Task added!")
    
def mark_task(tasks, done=True):
    if not tasks:
        print(Fore.YELLOW + "No tasks to update.")
        return
    display_tasks(tasks)
    try:
        num = int(input(f"Enter task number to mark as {'done' if done else 'undone'}: "))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = done
            print(Fore.GREEN + f"Task {num} marked as {'done' if done else 'undone'}.")
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")
        
def delete_task(tasks):
    if not tasks:
        print(Fore.YELLOW + "No tasks to delete.")
        return
    display_tasks(tasks)
    try:
        num = int(input("Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num-1)
            print(Fore.GREEN + f"Deleted task: {removed['description']}")
        else:
            print(Fore.RED + "Invalid task number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")
        
def main():
    tasks = load_tasks()
    
    while True:
        print(Style.BRIGHT + "\n|||CLI TO-DO LIST|||")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Mark task as undone")
        print("5. Delete task")
        print("6. Quit")
        
        choice = input("Choose an option: ").strip()
        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_task(tasks, True)
        elif choice == "4":
            mark_task(tasks, False)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            save_tasks(tasks)
            print(Fore.CYAN + "Tasks saved. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number 1-6.")
            
if __name__ == "__main__":
    main()