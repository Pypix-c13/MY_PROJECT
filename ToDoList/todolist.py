import os
TASK_DIR = "Task"

if not os.path.exists(TASK_DIR):
    os.makedirs(TASK_DIR)
if not os.path.isdir(TASK_DIR):
    print(f"{TASK_DIR} isn't folder!.\n")

def add_task(task_name:str):
    filename = f"{TASK_DIR}/{task_name}"
    with open(filename, "w") as file:
        pass

def remove_task(file_task_name:str):
    if os.path.exists(f"Task/{file_task_name}"):
        os.remove(f"Task/{file_task_name}")
    else:
        print("Error: File not found!.\n")

def scan_task():
    file = [i for i in os.listdir(TASK_DIR)]
    if not file:
        print("- ")
    
    for f in file:
        print("- ", f)

def main():
    while True:
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Scan Task")
        print("4. Quit")
        choice = input("Input: ")
        
        match choice:
            case "1":
                task = input("Enter Task Name: ")
                add_task(task)
            case "2":
                task = input("Enter Task to remove: ")
                remove_task(task)
            case "3":
                scan_task()
            case "4":
                break
            case _:
                print("Error: Unknown Numbers!.\n")
                break

main()