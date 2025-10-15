import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


valid_categories = ["Food", "Transport", "Shopping", "Bills", "Other"]

expenses = []

n = int(input("Enter number of expenses to record: "))

for i in range(n):
    print(f"\n--- Expense {i+1} ---")
    date = input("Enter date (YYYY-MM-DD): ")

    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print(" Amount must be positive. Try again.")
            else:
                break
        except ValueError:
            print(" Invalid input. Please enter a numeric value.")

    while True:
        category = input(f"Enter category {valid_categories}: ").capitalize()
        if category not in valid_categories:
            print(" Invalid category. Choose from the list.")
        else:
            break

    description = input("Enter description: ")

    expenses.append({
        "Date": date,
        "Amount": amount,
        "Category": category,
        "Description": description
    })


print("\n=== Expense Summary ===")
for exp in expenses:
    print(f"{exp['Date']} | ₹{exp['Amount']} | {exp['Category']} | {exp['Description']}")


class ExpenseTracker:
    def __init__(self, file_name='expenses.csv'):
        self.file_name = file_name
        try:
            self.data = pd.read_csv(self.file_name)
            print(f"Loaded data from {self.file_name}")
        except FileNotFoundError:
            print(f"{self.file_name} not found. Creating a new one.")
            self.data = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
            self.data.to_csv(self.file_name, index=False)

    def log_expense(self, date, amount, category, description):
        try:
            amount = float(amount)
            new_entry = pd.DataFrame([{
                "Date": date,
                "Amount": amount,
                "Category": category,
                "Description": description
            }])
            self.data = pd.concat([self.data, new_entry], ignore_index=True)
            self.data.to_csv(self.file_name, index=False)
            print("Expense added successfully!")
        except ValueError:
            print("Invalid input! Amount must be a number.")

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_name)
            print("Data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")

    def clean_data(self):
        before = len(self.data)
        self.data["Amount"] = pd.to_numeric(self.data["Amount"], errors='coerce')
        self.data["Date"] = pd.to_datetime(self.data["Date"], errors='coerce')
        self.data.dropna(subset=["Date", "Amount", "Category"], inplace=True)
        after = len(self.data)
        print(f"Removed {before - after} invalid entries.")
        self.data.to_csv(self.file_name, index=False)

    def get_summary(self):
        if self.data.empty:
            print("No data to summarize.")
            return
        
        total = self.data["Amount"].sum()
        avg = self.data["Amount"].mean()
        print("\n----- Expense Summary -----")
        print(f"Total Expenses: ₹{total:.2f}")
        print(f"Average Expense: ₹{avg:.2f}")
        print("\nCategory-wise Spending:")
        print(self.data.groupby("Category")["Amount"].sum())
        print("---------------------------")

    def filter_expenses(self, category=None, start_date=None, end_date=None):
        if self.data.empty:
            print("No data to filter.")
            return pd.DataFrame()
        
        filtered = self.data.copy()
        if category:
            filtered = filtered[filtered["Category"] == category]
        if start_date:
            filtered = filtered[pd.to_datetime(filtered["Date"]) >= pd.to_datetime(start_date)]
        if end_date:
            filtered = filtered[pd.to_datetime(filtered["Date"]) <= pd.to_datetime(end_date)]
        
        if filtered.empty:
            print("No expenses match the filter criteria.")
        return filtered

    def visualize_expenses(self):
        if self.data.empty:
            print("No data available for visualization.")
            return
        
        data_clean = self.data.copy()
        data_clean["Date"] = pd.to_datetime(data_clean["Date"], errors='coerce')
        data_clean["Amount"] = pd.to_numeric(data_clean["Amount"], errors='coerce')
        data_clean.dropna(subset=["Date", "Amount", "Category"], inplace=True)

        if data_clean.empty:
            print("No valid data to visualize.")
            return

        plt.figure(figsize=(10,6))
        sns.barplot(x="Category", y="Amount", data=data_clean, estimator=np.sum)
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(10,6))
        daily_sum = data_clean.groupby("Date")["Amount"].sum().reset_index()
        sns.lineplot(x="Date", y="Amount", data=daily_sum, marker='o')
        plt.title("Spending Trends Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8,6))
        cat_sum = data_clean.groupby("Category")["Amount"].sum()
        if cat_sum.sum() > 0:
            cat_sum.plot.pie(autopct='%1.1f%%')
            plt.title("Proportional Spending by Category")
            plt.ylabel("")
            plt.tight_layout()
            plt.show()
        else:
            print("No data to plot pie chart.")

        plt.figure(figsize=(8,6))
        sns.histplot(data_clean["Amount"], bins=10, kde=True)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    tracker = ExpenseTracker()
    while True:
        print("\n===== Smart Expense Tracker =====")
        print("1. Log New Expense")
        print("2. View Summary")
        print("3. Clean Data")
        print("4. Filter Expenses")
        print("5. Visualize Data")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.log_expense(date, amount, category, description)

        elif choice == "2":
            tracker.get_summary()

        elif choice == "3":
            tracker.clean_data()

        elif choice == "4":
            cat = input("Enter category (or press Enter to skip): ")
            sdate = input("Enter start date (or press Enter to skip): ")
            edate = input("Enter end date (or press Enter to skip): ")
            filtered = tracker.filter_expenses(cat or None, sdate or None, edate or None)
            if not filtered.empty:
                print(filtered)

        elif choice == "5":
            tracker.visualize_expenses()

        elif choice == "6":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")
