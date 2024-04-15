import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Define the tasks table schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        due_date DATE,
        priority INTEGER,
        tags TEXT,
        completed INTEGER DEFAULT 0,
        categories TEXT,
        notes TEXT
    )
""")
conn.commit()

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date_str = input("Enter due date (YYYY-MM-DD): ")
    priority = input("Enter priority (1: Low, 2: Medium, 3: High): ")
    tags = input("Enter tags (comma-separated): ")

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        priority = int(priority)
        if priority not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Invalid input. Please provide valid data.")
        return

    cursor.execute("""
        INSERT INTO tasks (title, description, due_date, priority, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, due_date, priority, tags))
    conn.commit()
    print("Task added successfully!")


def edit_task():
    task_id = input("Enter task ID to edit: ")

    # Retrieve the existing task details from the database
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()

    if not existing_task:
        print(f"Task with ID {task_id} not found.")
        return

    print(f"Editing Task {task_id}: {existing_task[1]}")
    print("Enter new details (leave blank to keep existing values):")

    new_title = input(f"Title ({existing_task[1]}): ") or existing_task[1]
    new_description = input(f"Description ({existing_task[2]}): ") or existing_task[2]
    new_due_date_str = input(f"Due date ({existing_task[3]} - YYYY-MM-DD): ") or existing_task[3]
    new_priority_str = input(f"Priority ({existing_task[4]} - 1: Low, 2: Medium, 3: High): ") or str(existing_task[4])
    new_tags = input(f"Tags ({existing_task[5]}): ") or existing_task[5]

    try:
        new_due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d").date()
        new_priority = int(new_priority_str)
        if new_priority not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Invalid input. Please use the correct format.")
        return

    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, priority = ?, tags = ?
        WHERE id = ?
    """, (new_title, new_description, new_due_date, new_priority, new_tags, task_id))
    conn.commit()
    print(f"Task {task_id} updated successfully!")

# Call this function wherever needed in your menu loop


def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks found.")
    else:
        print("All Tasks:")
        for task in tasks:
            status = "Completed" if task[6] else "Pending"
            print(f"Task {task[0]}: {task[1]} (Due: {task[3]}, Priority: {task[4]}, Status: {status})")


def complete_task():
    task_id = input("Enter task ID to mark as completed: ")
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    print("Task marked as completed!")


def delete_task():
    task_id = input("Enter task ID to delete: ")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print("Task deleted successfully!")


def generate_reports():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
    completed_tasks = cursor.fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Pending tasks: {pending_tasks}")


def search_tasks(keyword):
    cursor.execute("SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ? OR tags LIKE ?",
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    tasks = cursor.fetchall()
    if not tasks:
        print(f"No tasks found for keyword: {keyword}")
    else:
        print(f"Tasks matching '{keyword}':")
        for task in tasks:
            print(f"Task {task[0]}: {task[1]} (Due: {task[3]}, Priority: {task[4]})")

def main():
    
    while True:
        print("\nTask Manager Menu:")
        print("1. Add a new task")
        print("2. Edit an existing task")
        print("3. View all tasks")
        print("4. Mark a task as completed")
        print("5. Delete a task")
        print("6. Generate task reports")
        print("7. Search tasks")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            edit_task()
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            complete_task()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            generate_reports()
        elif choice == "7":
            keyword = input("Enter a keyword to search for tasks: ")
            search_tasks(keyword)
        elif choice == "8":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
