import os
from datetime import datetime


f=open("expenses.txt",'w')
f.close()
expenses = []
budget = None
filename = "expenses.txt"
def loadExpenses():
    if not os.path.exists(filename):
        with open(filename,'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    print("Skipping malformed entry.")
                    continue
                date, category, amount_str, description = parts
                try:
                    amount = float(amount_str)
                    expenses.append({
                        'date': date,
                        'category': category,
                        'amount': amount,
                        'description': description
                    })
                except ValueError:
                    print("Skipping entry with invalid amount.")
def saveExpenses():
    with open(filename,'w')as file:
        for expense in expenses:
            line=f"{expense['date']}|{expense['category']}|{expense['amount']}|{expense['description']}\n"
        file.write(line)
        
def addExpense():
    date=input("enter date is YYYY-MM-DD format : ")
    try:
        datetime.strptime(date,"%Y-%m-%d")
    except ValueError:
        print("invalid date format")
        
    category=input("enter category : ")
    
    try:
        amount=input("enter the expense : ")
    except ValueError:
        print("invalid amount")
        return
    desc = input("Enter description : ")
    expense={
        'date': date,
        'category': category,
        'amount': amount,
        'description': desc
    }            
    expenses.append(expense)
    print("expence added")
    
def viewExpense():
    if not expenses:
        print("no expense to show")
        return
    print("-----all Expenses-----")
    for exp in expenses:
        if all(k in exp for k in ('date', 'category', 'amount', 'description')):
            print(f"{exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['description']}")
        else:
            print("incomplete data")

def setBudget():
    global budget
    try:
        budget=float(input("enter your budget"))
        print(f"the budget is{budget}")
    except ValueError:
        print("invalid budget")

def track_budget():
    if budget is None:
        print("Budget not set.")
        return
    total=sum(int(exp['amount'])for exp in expenses)
    print(f"\nTotal expenses: ₹{total}")
    if total > budget:
        print("You have exceeded your budget!")
    else:
        print(f"You have ₹{budget - total} left for the month.")

def menu():
    loadExpenses()
    while True:
        print("======Personal Expense Tracker=====")
        print("1. Add Expense ")
        print("2. View Expense")
        print("3. Set\Track Budget")
        print("4. Save Expense")
        print("5. Exit")
        choice=int(input("enter your choice : "))
        
        if choice==1:
            addExpense()
        elif choice==2:
            viewExpense()
        elif choice==3:
            if budget==None:
                setBudget()
            track_budget()
        elif choice==4:
            saveExpenses()
        elif  choice==5:
            saveExpenses()
            print("Expense Saving. Exiting....")
            break
        else:
            print("invalid choice. try again")

if __name__== "__main__":
    menu()
            
          
    