import hashlib
import os
from getpass import getpass

user_file = "user_file.txt"
task_file = "task_file.txt"

def initialise_files():
    if not os.path.exists(user_file):
        open(user_file, 'w').close()
    if not os.path.exists(task_file):  
        open(task_file, 'w').close()
        
def hash_password(password):
    salt = "fixed_salt_123"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def user_reg():
    name = input("Enter your name: ")
    with open(user_file, 'r') as f:   
        existing_users = [line.split('|')[0].strip() for line in f]
        
    username = input("Enter username: ")
    if username in existing_users:
        print("Username already exists!")
        return False
    
    password = input("Enter your password: ")  
    confirm_password = input("Confirm your password: ")
    
    if password != confirm_password:
        print("Passwords don't match!")
        return False
    
    hashed_pw = hash_password(password)
    
    with open(user_file, 'a') as f:  
        f.write(f"{username}|{hashed_pw}|{name}\n")
    print("Registration successful!")
    return True
    
def user_login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hash_pw = hash_password(password)
    
    with open(user_file, 'r') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) >= 2:  
                stored_user, stored_pass = parts[0], parts[1]
                if username == stored_user and hash_pw == stored_pass:
                    print("Login successful!")
                    return username
                elif username == stored_user and hash_pw != stored_pass:
                    print("Incorrect password")
                    return None
    
    print("Invalid credentials")
    return None
            
def add_task(username):
    desp = input("Enter task description: ")
    max_id = 0
    try:
        with open(task_file, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[0] == username:
                    max_id = max(max_id, int(parts[1]))
    except FileNotFoundError:
        pass  
        
    new_id = max_id + 1
    with open(task_file, 'a') as file:  
        file.write(f"{username}|{new_id}|{desp}|Pending\n")
        
    print(f"Task added with ID {new_id}")
    
def view_task(username):
    print("\nYour tasks:")
    print("-" * 30)
    print("ID | Description | Status")
    print("-" * 30)
    
    tasks = []
    try:
        with open(task_file, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[0] == username:
                    tasks.append(parts)
    except FileNotFoundError:
        pass
        
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"{task[1]} | {task[2]} | {task[3]}")
        
def mark_task_complete(username):
    view_task(username)
    try:
        task_id = input("Enter the task ID to mark as completed: ")
        
        updated = False
        lines = []
        try:
            with open(task_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No tasks found")
            return
            
        with open(task_file, 'w') as file:
            for line in lines:
                parts = line.strip().split('|')
                if len(parts) >= 4 and parts[0] == username and parts[1] == task_id:
                    file.write(f"{parts[0]}|{parts[1]}|{parts[2]}|Completed\n")
                    updated = True
                else:
                    file.write(line)
                    
        if updated:
            print("Task marked as completed!")
        else:
            print("Task not found") 
    except Exception as e:
        print(f"Error: {e}")

def delete_task(username):
    view_task(username)
    try:
        task_id = input("Enter the task ID to delete: ")
        
        deleted = False
        lines = []
        try:
            with open(task_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No tasks found")
            return
            
        with open(task_file, 'w') as file:
            for line in lines:
                parts = line.strip().split('|')
                if not (len(parts) >= 2 and parts[0] == username and parts[1] == task_id):
                    file.write(line)
                else:
                    deleted = True
        
        if deleted:
            print("Task deleted!")
        else:
            print("Task not found!")
    except Exception as e:
        print(f"Error: {e}")
        
def menu(username):
    while True:
        print("\nTask Manager Menu")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Logout")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_task(username)
        elif choice == '2':
            view_task(username)
        elif choice == '3':
            mark_task_complete(username)
        elif choice == '4':
            delete_task(username)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")        
      
def main():
    initialise_files()
    while True:
        print("\n===== Task Manager =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
    
        try:
            choice = int(input("Enter your choice (1-3): "))
        except ValueError:
            print("Please enter a number")
            continue
            
        if choice == 1:
            user_reg()
        elif choice == 2:
            username = user_login()
            if username:
                menu(username)
        elif choice == 3:
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()